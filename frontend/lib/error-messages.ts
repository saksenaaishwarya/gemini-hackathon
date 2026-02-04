/**
 * Error Message Utilities
 * Maps HTTP status codes and API errors to user-friendly messages
 */

export const ERROR_MESSAGES: Record<number, string> = {
  400: 'Invalid request. Please check your input.',
  401: 'Authentication required. Please log in.',
  403: 'You don\'t have permission to access this resource.',
  404: 'Resource not found.',
  429: 'Too many requests. Please wait a moment and try again.',
  500: 'Server error. We\'re working on fixing it. Please try again later.',
  502: 'Service temporarily unavailable. Please try again soon.',
  503: 'Service maintenance in progress. Please try again shortly.',
  504: 'Request took too long to complete. Please try with a shorter message.',
};

/**
 * Get user-friendly error message
 * @param statusCode - HTTP status code
 * @param apiError - Optional API error message
 * @returns User-friendly error message
 */
export function getErrorMessage(statusCode: number, apiError?: string): string {
  // Use custom error message if provided
  if (apiError && apiError.length > 0 && !apiError.includes('Error:')) {
    return apiError;
  }

  // Fall back to status code mapping
  return ERROR_MESSAGES[statusCode] || 'Something went wrong. Please try again.';
}

/**
 * Format error response for display
 * @param response - Response object
 * @returns Formatted error message
 */
export function formatErrorResponse(response: any): string {
  if (typeof response === 'string') {
    return response;
  }

  if (response?.error) {
    return response.error;
  }

  if (response?.message) {
    return response.message;
  }

  if (response?.detail) {
    return response.detail;
  }

  return 'An unexpected error occurred. Please try again.';
}

/**
 * Handle chat API response
 * @param response - HTTP response object
 * @returns Parsed response or error message
 */
export async function handleChatResponse(response: Response) {
  const data = await response.json();

  if (!response.ok) {
    const errorMessage = getErrorMessage(response.status, data?.error || data?.detail);
    throw new Error(errorMessage);
  }

  if (!data.success) {
    throw new Error(data?.error || 'Failed to process message');
  }

  return data;
}
