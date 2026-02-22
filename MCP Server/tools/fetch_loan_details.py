"""
Fetch loan details for a user by calling the backend loan details API.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

LOAN_API_BASE_URL = os.getenv("LOAN_API_BASE_URL", "http://localhost:8080").strip()


def fetch_loan_details(userId: str, loanId: str) -> dict:
    """
    Fetch loan details for a given user and loan.

    Args:
        userId (str): User ID
        loanId (str): Loan ID / Upload ID

    Returns:
        dict: Loan details response from backend API
    """

    if not userId or not userId.strip():
        return {
            "success": False,
            "message": "userId is required",
            "data": None,
        }

    if not loanId or not loanId.strip():
        return {
            "success": False,
            "message": "loanId is required",
            "data": None,
        }

    url = f"{LOAN_API_BASE_URL}/api/loans/{userId}/uploaded/{loanId}"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        response_text = ""
        try:
            response_text = e.response.text
        except Exception:
            response_text = str(e)

        return {
            "success": False,
            "message": f"HTTP error fetching loan details: {response_text}",
            "userId": userId,
            "loanId": loanId,
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Error connecting to loan details API: {str(e)}",
            "userId": userId,
            "loanId": loanId,
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "userId": userId,
            "loanId": loanId,
        }
