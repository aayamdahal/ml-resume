"""
Utility functions for Resume Ranking System
"""
import logging
import re
from typing import List, Dict, Any
from config import MAX_RESUMES_PER_REQUEST

# Setup logging


def setup_logging():
    """Configure logging for the application"""
    # Use StreamHandler for AWS Lambda (logs to CloudWatch)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


def validate_request(data: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate incoming API request

    Args:
        data: Request JSON data

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not data:
        return False, "Request body is empty"

    if 'job_description' not in data:
        return False, "Missing 'job_description' field"

    if 'resumes' not in data:
        return False, "Missing 'resumes' field"

    job_description = data['job_description']
    if not isinstance(job_description, str) or len(job_description.strip()) == 0:
        return False, "Job description must be a non-empty string"

    if len(job_description) < 50:
        return False, "Job description is too short (minimum 50 characters)"

    resumes = data['resumes']
    if not isinstance(resumes, list):
        return False, "'resumes' must be a list"

    if len(resumes) == 0:
        return False, "No resumes provided"

    if len(resumes) > MAX_RESUMES_PER_REQUEST:
        return False, f"Too many resumes (maximum {MAX_RESUMES_PER_REQUEST})"

    # Validate each resume
    for idx, resume in enumerate(resumes):
        if not isinstance(resume, dict):
            return False, f"Resume at index {idx} is not a valid object"

        if 'file_base64' not in resume:
            return False, f"Resume at index {idx} missing 'file_base64' field"

        if not resume['file_base64']:
            return False, f"Resume at index {idx} has empty 'file_base64'"

    return True, ""


def clean_text(text: str) -> str:
    """
    Clean and normalize text

    Args:
        text: Raw text

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove special characters but keep important punctuation
    text = re.sub(r'[^\w\s\.\,\@\+\-\(\)]', '', text)

    return text.strip()


def extract_years_of_experience(text: str) -> float:
    """
    Extract years of experience from text

    Args:
        text: Resume text

    Returns:
        Estimated years of experience
    """
    patterns = [
        r'(\d+)\+?\s*years?\s+of\s+experience',
        r'(\d+)\+?\s*yrs?\s+experience',
        r'experience\s*:\s*(\d+)\+?\s*years?',
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            try:
                return float(match.group(1))
            except:
                pass

    # Try to estimate from work history dates
    year_pattern = r'\b(19|20)\d{2}\b'
    years = re.findall(year_pattern, text)
    if len(years) >= 2:
        try:
            years_int = [int(y) for y in years]
            return max(years_int) - min(years_int)
        except:
            pass

    return 0.0


def format_error_response(error_message: str, status_code: int = 400) -> tuple:
    """
    Format error response

    Args:
        error_message: Error message
        status_code: HTTP status code

    Returns:
        Tuple of (response_dict, status_code)
    """
    return {
        "error": error_message,
        "success": False
    }, status_code


def format_success_response(ranked_resumes: List[Dict], total_processed: int) -> Dict:
    """
    Format success response

    Args:
        ranked_resumes: List of ranked resume data
        total_processed: Total number of resumes processed

    Returns:
        Response dictionary
    """
    return {
        "success": True,
        "total_resumes_processed": total_processed,
        "top_candidates": len(ranked_resumes),
        "ranked_resumes": ranked_resumes
    }
