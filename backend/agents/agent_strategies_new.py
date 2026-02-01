"""
LegalMind Agent Strategies
Agent selection and orchestration logic for legal analysis.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .agent_definitions_new import (
    CONTRACT_PARSER_AGENT,
    LEGAL_RESEARCH_AGENT,
    COMPLIANCE_CHECKER_AGENT,
    RISK_ASSESSMENT_AGENT,
    LEGAL_MEMO_AGENT,
    ASSISTANT_AGENT,
)


class QueryType(Enum):
    """Types of user queries."""
    CONTRACT_ANALYSIS = "contract_analysis"
    LEGAL_RESEARCH = "legal_research"
    COMPLIANCE_CHECK = "compliance_check"
    RISK_ASSESSMENT = "risk_assessment"
    DOCUMENT_GENERATION = "document_generation"
    GENERAL_QUESTION = "general_question"


@dataclass
class AgentSelection:
    """Result of agent selection."""
    agent_name: str
    confidence: float
    reason: str


# Keywords for query classification
QUERY_KEYWORDS = {
    QueryType.CONTRACT_ANALYSIS: [
        "analyze contract", "parse contract", "extract", "what does the contract say",
        "contract terms", "parties", "effective date", "termination", "clauses",
        "obligations", "what are the", "contract type", "key dates",
        "review contract", "contract details", "read contract"
    ],
    QueryType.LEGAL_RESEARCH: [
        "research", "case law", "precedent", "legal meaning", "what is",
        "explain", "jurisdiction", "law says", "regulation", "statute",
        "court ruling", "legal definition", "is it legal", "legal implications"
    ],
    QueryType.COMPLIANCE_CHECK: [
        "compliance", "gdpr", "hipaa", "ccpa", "sox", "regulation",
        "compliant", "privacy", "data protection", "audit", "framework",
        "requirements", "is this compliant", "check compliance"
    ],
    QueryType.RISK_ASSESSMENT: [
        "risk", "risks", "liability", "exposure", "dangerous", "concern",
        "problematic", "unfavorable", "one-sided", "assess risk", "risk score",
        "potential issues", "red flags", "evaluate"
    ],
    QueryType.DOCUMENT_GENERATION: [
        "generate", "create", "write", "memo", "report", "summary",
        "document", "brief", "draft", "prepare", "produce"
    ],
}


def classify_query(query: str) -> QueryType:
    """Classify a user query into a query type.
    
    Args:
        query: The user's message
        
    Returns:
        QueryType indicating the type of query
    """
    query_lower = query.lower()
    
    # Score each query type based on keyword matches
    scores = {}
    for query_type, keywords in QUERY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        scores[query_type] = score
    
    # Get the type with highest score
    best_type = max(scores, key=scores.get)
    
    # If no keywords matched, return general question
    if scores[best_type] == 0:
        return QueryType.GENERAL_QUESTION
    
    return best_type


def get_agent_for_query_type(query_type: QueryType) -> str:
    """Get the appropriate agent for a query type.
    
    Args:
        query_type: The classified query type
        
    Returns:
        Agent name to handle the query
    """
    mapping = {
        QueryType.CONTRACT_ANALYSIS: CONTRACT_PARSER_AGENT,
        QueryType.LEGAL_RESEARCH: LEGAL_RESEARCH_AGENT,
        QueryType.COMPLIANCE_CHECK: COMPLIANCE_CHECKER_AGENT,
        QueryType.RISK_ASSESSMENT: RISK_ASSESSMENT_AGENT,
        QueryType.DOCUMENT_GENERATION: LEGAL_MEMO_AGENT,
        QueryType.GENERAL_QUESTION: ASSISTANT_AGENT,
    }
    return mapping.get(query_type, ASSISTANT_AGENT)


def select_agent(query: str, context: Optional[Dict[str, Any]] = None) -> AgentSelection:
    """Select the best agent to handle a user query.
    
    Args:
        query: The user's message
        context: Optional context including chat history, active contract, etc.
        
    Returns:
        AgentSelection with agent name and confidence
    """
    query_type = classify_query(query)
    agent_name = get_agent_for_query_type(query_type)
    
    # Calculate confidence based on keyword matches
    query_lower = query.lower()
    keywords = QUERY_KEYWORDS.get(query_type, [])
    matches = sum(1 for kw in keywords if kw in query_lower)
    confidence = min(1.0, matches / 3) if matches > 0 else 0.3
    
    return AgentSelection(
        agent_name=agent_name,
        confidence=confidence,
        reason=f"Query classified as {query_type.value}"
    )


def get_agent_sequence(query: str, context: Optional[Dict[str, Any]] = None) -> List[str]:
    """Get the sequence of agents for a complex query.
    
    For comprehensive analyses, multiple agents may need to work together.
    
    Args:
        query: The user's message
        context: Optional context
        
    Returns:
        List of agent names in execution order
    """
    query_lower = query.lower()
    
    # Check for comprehensive analysis requests
    if any(kw in query_lower for kw in ["full analysis", "comprehensive", "complete review", "analyze everything"]):
        return [
            CONTRACT_PARSER_AGENT,
            COMPLIANCE_CHECKER_AGENT,
            RISK_ASSESSMENT_AGENT,
            LEGAL_MEMO_AGENT,
        ]
    
    # Check for compliance + risk
    if "compliance" in query_lower and "risk" in query_lower:
        return [
            COMPLIANCE_CHECKER_AGENT,
            RISK_ASSESSMENT_AGENT,
            LEGAL_MEMO_AGENT,
        ]
    
    # Check for contract analysis with report
    if ("analyze" in query_lower or "review" in query_lower) and "report" in query_lower:
        return [
            CONTRACT_PARSER_AGENT,
            RISK_ASSESSMENT_AGENT,
            LEGAL_MEMO_AGENT,
        ]
    
    # Single agent for simple queries
    selection = select_agent(query, context)
    return [selection.agent_name]


class AgentOrchestrator:
    """Orchestrates agent execution for multi-agent workflows."""
    
    def __init__(self):
        """Initialize the orchestrator."""
        self.current_sequence: List[str] = []
        self.current_index: int = 0
        self.context: Dict[str, Any] = {}
        self.results: Dict[str, Any] = {}
    
    def start_workflow(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Start a new workflow for a query.
        
        Args:
            query: User's message
            context: Optional context
            
        Returns:
            First agent to execute
        """
        self.current_sequence = get_agent_sequence(query, context)
        self.current_index = 0
        self.context = context or {}
        self.results = {}
        
        return self.current_sequence[0] if self.current_sequence else ASSISTANT_AGENT
    
    def get_next_agent(self) -> Optional[str]:
        """Get the next agent in the sequence.
        
        Returns:
            Next agent name or None if complete
        """
        self.current_index += 1
        if self.current_index < len(self.current_sequence):
            return self.current_sequence[self.current_index]
        return None
    
    def record_result(self, agent_name: str, result: Any):
        """Record the result from an agent.
        
        Args:
            agent_name: Name of the agent
            result: Agent's output
        """
        self.results[agent_name] = result
    
    def is_complete(self) -> bool:
        """Check if the workflow is complete.
        
        Returns:
            True if all agents have executed
        """
        return self.current_index >= len(self.current_sequence)
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get a summary of the workflow execution.
        
        Returns:
            Dict with workflow details
        """
        return {
            "sequence": self.current_sequence,
            "completed": self.current_index,
            "total": len(self.current_sequence),
            "results": self.results,
            "is_complete": self.is_complete(),
        }


def should_handoff(
    current_agent: str,
    message: str,
    context: Optional[Dict[str, Any]] = None
) -> Optional[str]:
    """Determine if the current agent should hand off to another.
    
    Used for dynamic agent handoff based on the agent's response.
    
    Args:
        current_agent: Currently active agent
        message: Agent's response or user's follow-up
        context: Optional context
        
    Returns:
        Agent to hand off to, or None to continue with current
    """
    message_lower = message.lower()
    
    # Contract Parser handoffs
    if current_agent == CONTRACT_PARSER_AGENT:
        if any(kw in message_lower for kw in ["check compliance", "is it compliant"]):
            return COMPLIANCE_CHECKER_AGENT
        if any(kw in message_lower for kw in ["what are the risks", "assess risk"]):
            return RISK_ASSESSMENT_AGENT
    
    # Compliance Checker handoffs
    if current_agent == COMPLIANCE_CHECKER_AGENT:
        if any(kw in message_lower for kw in ["generate report", "create memo"]):
            return LEGAL_MEMO_AGENT
        if "assess risk" in message_lower:
            return RISK_ASSESSMENT_AGENT
    
    # Risk Assessment handoffs
    if current_agent == RISK_ASSESSMENT_AGENT:
        if any(kw in message_lower for kw in ["generate report", "create memo", "document"]):
            return LEGAL_MEMO_AGENT
    
    # Research handoffs
    if current_agent == LEGAL_RESEARCH_AGENT:
        if any(kw in message_lower for kw in ["check contract", "apply to contract"]):
            return CONTRACT_PARSER_AGENT
    
    return None


# Workflow templates for common scenarios
WORKFLOW_TEMPLATES = {
    "contract_review": {
        "name": "Contract Review",
        "description": "Comprehensive contract review with compliance and risk analysis",
        "agents": [
            CONTRACT_PARSER_AGENT,
            COMPLIANCE_CHECKER_AGENT,
            RISK_ASSESSMENT_AGENT,
            LEGAL_MEMO_AGENT,
        ],
    },
    "compliance_audit": {
        "name": "Compliance Audit",
        "description": "Check contract compliance against multiple frameworks",
        "agents": [
            CONTRACT_PARSER_AGENT,
            COMPLIANCE_CHECKER_AGENT,
            LEGAL_MEMO_AGENT,
        ],
    },
    "risk_analysis": {
        "name": "Risk Analysis",
        "description": "Comprehensive risk assessment of contract terms",
        "agents": [
            CONTRACT_PARSER_AGENT,
            RISK_ASSESSMENT_AGENT,
            LEGAL_MEMO_AGENT,
        ],
    },
    "quick_summary": {
        "name": "Quick Summary",
        "description": "Get a quick overview of contract key terms",
        "agents": [
            CONTRACT_PARSER_AGENT,
        ],
    },
    "legal_research": {
        "name": "Legal Research",
        "description": "Research legal questions and find precedents",
        "agents": [
            LEGAL_RESEARCH_AGENT,
        ],
    },
}


def get_workflow_template(template_name: str) -> Optional[Dict[str, Any]]:
    """Get a workflow template by name.
    
    Args:
        template_name: Name of the template
        
    Returns:
        Template dict or None
    """
    return WORKFLOW_TEMPLATES.get(template_name)


def list_workflow_templates() -> List[Dict[str, Any]]:
    """List all available workflow templates.
    
    Returns:
        List of template summaries
    """
    return [
        {
            "id": key,
            "name": template["name"],
            "description": template["description"],
            "agent_count": len(template["agents"]),
        }
        for key, template in WORKFLOW_TEMPLATES.items()
    ]
