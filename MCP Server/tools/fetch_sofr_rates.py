"""
Fetch SOFR (Secured Overnight Financing Rate) data from Federal Reserve Economic Data (FRED) API.
SOFR is the benchmark interest rate for dollar-denominated derivatives and loans.
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# FRED API Configuration
FRED_API_KEY = os.getenv("FRED_API_KEY", "").strip()
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_sofr_rates(
    period: str = "overnight",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> dict:
    """
    Fetch SOFR (Secured Overnight Financing Rate) from the Federal Reserve.
    
    SOFR is administered by the Federal Reserve Bank of New York and represents 
    the cost of borrowing cash overnight collateralized by Treasury securities.
    
    Parameters:
        period (str): The SOFR period. Options:
            - "overnight" (default): Overnight SOFR
            - "30day": 30-Day Average SOFR
            - "90day": 90-Day Average SOFR
            - "180day": 180-Day Average SOFR
        start_date (str, optional): Start date in YYYY-MM-DD format. 
                                   Defaults to 30 days ago.
        end_date (str, optional): End date in YYYY-MM-DD format. 
                                 Defaults to today.
    
    Returns:
        dict: Dictionary containing SOFR rate information with the following structure:
            {
                "success": bool,
                "data": {
                    "rate_type": str,
                    "current_rate": float,
                    "rate_date": str,
                    "historical_data": list of dict with "date" and "rate",
                    "average_rate": float,
                    "min_rate": float,
                    "max_rate": float
                },
                "source": str,
                "message": str
            }
    
    Example:
        >>> fetch_sofr_rates(period="overnight")
        {
            "success": True,
            "data": {
                "rate_type": "Overnight SOFR",
                "current_rate": 5.31,
                "rate_date": "2026-02-17",
                ...
            }
        }
    """
    
    # Map period to FRED series ID
    period_mapping = {
        "overnight": ("SOFR", "Overnight SOFR"),
        "30day": ("SOFR30DAYAVG", "30-Day Average SOFR"),
        "90day": ("SOFR90DAYAVG", "90-Day Average SOFR"),
        "180day": ("SOFR180DAYAVG", "180-Day Average SOFR"),
    }
    
    if period.lower() not in period_mapping:
        return {
            "success": False,
            "data": None,
            "source": "FRED API",
            "message": f"Invalid period '{period}'. Valid options: {list(period_mapping.keys())}"
        }
    
    series_id, rate_name = period_mapping[period.lower()]
    
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    # Check if API key is available
    if not FRED_API_KEY:
        return {
            "success": False,
            "data": None,
            "source": "FRED API",
            "message": "FRED_API_KEY not found in environment variables. Please get a free API key from https://fred.stlouisfed.org/docs/api/api_key.html"
        }
    
    try:
        # Fetch data from FRED API
        params = {
            "series_id": series_id,
            "api_key": FRED_API_KEY,
            "file_type": "json",
            "observation_start": start_date,
            "observation_end": end_date,
            "sort_order": "desc"
        }
        
        response = requests.get(FRED_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if "observations" not in data or len(data["observations"]) == 0:
            return {
                "success": False,
                "data": None,
                "source": "FRED API",
                "message": "No SOFR data available for the specified date range."
            }
        
        # Process observations
        observations = data["observations"]
        rates = []
        
        for obs in observations:
            if obs["value"] != ".":  # Filter out missing data
                rates.append({
                    "date": obs["date"],
                    "rate": float(obs["value"])
                })
        
        if not rates:
            return {
                "success": False,
                "data": None,
                "source": "FRED API",
                "message": "No valid SOFR rate data found in the response."
            }
        
        # Calculate statistics
        rate_values = [r["rate"] for r in rates]
        current_rate = rates[0]["rate"]
        current_date = rates[0]["date"]
        
        result = {
            "success": True,
            "data": {
                "rate_type": rate_name,
                "current_rate": current_rate,
                "rate_date": current_date,
                "current_rate_percentage": f"{current_rate}%",
                "historical_data": rates[:10],  # Return last 10 observations
                "average_rate": round(sum(rate_values) / len(rate_values), 4),
                "min_rate": min(rate_values),
                "max_rate": max(rate_values),
                "data_points": len(rates),
                "period_analyzed": f"{start_date} to {end_date}"
            },
            "source": "Federal Reserve Economic Data (FRED)",
            "api_url": "https://fred.stlouisfed.org/",
            "message": f"Successfully fetched {rate_name} data."
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "data": None,
            "source": "FRED API",
            "message": f"Error fetching SOFR data from FRED API: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "source": "FRED API",
            "message": f"Unexpected error: {str(e)}"
        }
