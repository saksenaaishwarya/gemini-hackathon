"""
Logging Tools
Tools for logging agent thinking and reasoning.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import time

from services.firestore_service import get_firestore_service


class ThinkingLogger:
    """Context manager for logging agent thinking."""
    
    def __init__(
        self,
        session_id: str,
        agent_name: str,
        input_text: str,
    ):
        self.session_id = session_id
        self.agent_name = agent_name
        self.input_text = input_text
        self.start_time = None
        self.tool_calls = []
        self.reasoning = None
        self.output_text = None
    
    async def __aenter__(self):
        self.start_time = time.time()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        duration_ms = int((time.time() - self.start_time) * 1000)
        
        firestore = get_firestore_service()
        await firestore.log_agent_thinking(
            session_id=self.session_id,
            agent_name=self.agent_name,
            input_text=self.input_text,
            output_text=self.output_text or "",
            reasoning=self.reasoning,
            tool_calls=self.tool_calls,
            duration_ms=duration_ms,
        )
    
    def add_tool_call(self, tool_name: str, args: Dict, result: Any):
        """Record a tool call."""
        self.tool_calls.append({
            "tool_name": tool_name,
            "arguments": args,
            "result": str(result)[:500],  # Truncate for storage
            "timestamp": datetime.utcnow().isoformat(),
        })
    
    def set_reasoning(self, reasoning: str):
        """Set the agent's reasoning/thinking."""
        self.reasoning = reasoning
    
    def set_output(self, output: str):
        """Set the final output."""
        self.output_text = output


async def log_thinking(
    session_id: str,
    agent_name: str,
    input_text: str,
    output_text: str,
    reasoning: Optional[str] = None,
    tool_calls: Optional[List[Dict]] = None,
    duration_ms: Optional[int] = None,
) -> Dict[str, Any]:
    """Log agent thinking/reasoning for transparency.
    
    Args:
        session_id: Session ID
        agent_name: Name of the agent
        input_text: Input provided to the agent
        output_text: Agent's output
        reasoning: Internal reasoning if available
        tool_calls: List of tool calls made
        duration_ms: Processing time
        
    Returns:
        Log entry info
    """
    firestore = get_firestore_service()
    
    log_id = await firestore.log_agent_thinking(
        session_id=session_id,
        agent_name=agent_name,
        input_text=input_text,
        output_text=output_text,
        reasoning=reasoning,
        tool_calls=tool_calls,
        duration_ms=duration_ms,
    )
    
    return {
        "status": "success",
        "log_id": log_id,
        "message": "Thinking logged successfully"
    }


async def get_thinking_logs(
    session_id: Optional[str] = None,
    agent_name: Optional[str] = None,
    limit: int = 100,
) -> Dict[str, Any]:
    """Retrieve agent thinking logs.
    
    Args:
        session_id: Filter by session
        agent_name: Filter by agent
        limit: Maximum results
        
    Returns:
        List of thinking logs
    """
    firestore = get_firestore_service()
    
    logs = await firestore.get_thinking_logs(
        session_id=session_id,
        agent_name=agent_name,
        limit=limit,
    )
    
    return {
        "status": "success",
        "logs": logs,
        "count": len(logs),
    }


async def get_session_trace(
    session_id: str,
) -> Dict[str, Any]:
    """Get complete trace of a session's agent interactions.
    
    Args:
        session_id: The session ID
        
    Returns:
        Complete session trace
    """
    firestore = get_firestore_service()
    
    # Get session info
    session = await firestore.get_session(session_id)
    if not session:
        return {
            "status": "error",
            "message": f"Session {session_id} not found"
        }
    
    # Get messages
    messages = await firestore.get_messages(session_id)
    
    # Get thinking logs
    logs = await firestore.get_thinking_logs(session_id=session_id)
    
    # Combine into timeline
    timeline = []
    
    for msg in messages:
        timeline.append({
            "type": "message",
            "role": msg.get("role"),
            "content": msg.get("content"),
            "agent_name": msg.get("agent_name"),
            "timestamp": msg.get("created_at"),
        })
    
    for log in logs:
        timeline.append({
            "type": "thinking",
            "agent_name": log.get("agent_name"),
            "input": log.get("input_text"),
            "output": log.get("output_text"),
            "reasoning": log.get("reasoning"),
            "tool_calls": log.get("tool_calls"),
            "duration_ms": log.get("duration_ms"),
            "timestamp": log.get("created_at"),
        })
    
    # Sort by timestamp
    timeline.sort(key=lambda x: x.get("timestamp", ""))
    
    return {
        "status": "success",
        "session_id": session_id,
        "session": session,
        "timeline": timeline,
        "message_count": len(messages),
        "thinking_log_count": len(logs),
    }


async def get_agent_statistics(
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Get statistics on agent usage and performance.
    
    Args:
        session_id: Filter by session (optional)
        
    Returns:
        Agent statistics
    """
    firestore = get_firestore_service()
    
    logs = await firestore.get_thinking_logs(
        session_id=session_id,
        limit=500,
    )
    
    # Aggregate statistics
    agent_stats = {}
    
    for log in logs:
        agent_name = log.get("agent_name", "unknown")
        
        if agent_name not in agent_stats:
            agent_stats[agent_name] = {
                "call_count": 0,
                "total_duration_ms": 0,
                "tool_calls": 0,
                "avg_duration_ms": 0,
            }
        
        stats = agent_stats[agent_name]
        stats["call_count"] += 1
        stats["total_duration_ms"] += log.get("duration_ms", 0)
        stats["tool_calls"] += len(log.get("tool_calls", []))
    
    # Calculate averages
    for agent_name, stats in agent_stats.items():
        if stats["call_count"] > 0:
            stats["avg_duration_ms"] = stats["total_duration_ms"] // stats["call_count"]
    
    # Overall stats
    total_calls = sum(s["call_count"] for s in agent_stats.values())
    total_duration = sum(s["total_duration_ms"] for s in agent_stats.values())
    total_tool_calls = sum(s["tool_calls"] for s in agent_stats.values())
    
    return {
        "status": "success",
        "agent_statistics": agent_stats,
        "overall": {
            "total_agent_calls": total_calls,
            "total_duration_ms": total_duration,
            "total_tool_calls": total_tool_calls,
            "avg_duration_per_call_ms": total_duration // total_calls if total_calls > 0 else 0,
        }
    }


async def log_error(
    session_id: str,
    agent_name: str,
    error_message: str,
    context: Optional[Dict] = None,
) -> Dict[str, Any]:
    """Log an error that occurred during agent processing.
    
    Args:
        session_id: Session ID
        agent_name: Agent where error occurred
        error_message: Error description
        context: Additional context
        
    Returns:
        Log entry info
    """
    firestore = get_firestore_service()
    
    log_id = await firestore.log_agent_thinking(
        session_id=session_id,
        agent_name=agent_name,
        input_text=f"ERROR: {error_message}",
        output_text="Error occurred during processing",
        reasoning=str(context) if context else None,
        tool_calls=[],
        duration_ms=0,
    )
    
    return {
        "status": "success",
        "log_id": log_id,
        "message": "Error logged"
    }


# Tool definitions for Gemini function calling
LOGGING_TOOLS = [
    {
        "name": "log_thinking",
        "description": "Log agent thinking and reasoning for transparency and debugging.",
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Current session ID"
                },
                "agent_name": {
                    "type": "string",
                    "description": "Name of the agent"
                },
                "input_text": {
                    "type": "string",
                    "description": "Input provided to the agent"
                },
                "output_text": {
                    "type": "string",
                    "description": "Agent's output"
                },
                "reasoning": {
                    "type": "string",
                    "description": "Internal reasoning process"
                },
                "tool_calls": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "tool_name": {"type": "string"},
                            "arguments": {"type": "object"},
                            "result": {"type": "string"}
                        }
                    },
                    "description": "List of tool calls made"
                },
                "duration_ms": {
                    "type": "integer",
                    "description": "Processing duration in milliseconds"
                }
            },
            "required": ["session_id", "agent_name", "input_text", "output_text"]
        },
        "handler": log_thinking
    },
    {
        "name": "get_thinking_logs",
        "description": "Retrieve agent thinking logs for review and debugging.",
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Filter by session ID"
                },
                "agent_name": {
                    "type": "string",
                    "description": "Filter by agent name"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results (default 100)"
                }
            }
        },
        "handler": get_thinking_logs
    },
    {
        "name": "get_session_trace",
        "description": "Get complete trace of a session including messages and agent thinking.",
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "The session ID to trace"
                }
            },
            "required": ["session_id"]
        },
        "handler": get_session_trace
    },
    {
        "name": "get_agent_statistics",
        "description": "Get usage and performance statistics for agents.",
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Filter by session ID (optional)"
                }
            }
        },
        "handler": get_agent_statistics
    },
    {
        "name": "log_error",
        "description": "Log an error that occurred during processing.",
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Session ID"
                },
                "agent_name": {
                    "type": "string",
                    "description": "Agent where error occurred"
                },
                "error_message": {
                    "type": "string",
                    "description": "Error description"
                },
                "context": {
                    "type": "object",
                    "description": "Additional context about the error"
                }
            },
            "required": ["session_id", "agent_name", "error_message"]
        },
        "handler": log_error
    }
]


def get_logging_tools() -> List[Dict[str, Any]]:
    """Get all logging tool definitions."""
    return LOGGING_TOOLS


# Export for tool registry
TOOL_DEFINITIONS = LOGGING_TOOLS
