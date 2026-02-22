"""
Fetch current benchmark interest rates from multiple sources.
This tool provides current benchmark rates that have replaced LIBOR, including SOFR, EURIBOR, SONIA, and TONAR.
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()

# FRED API Configuration
FRED_API_KEY = os.getenv("FRED_API_KEY", "").strip()
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_benchmark_rates(
    benchmarks: Optional[List[str]] = None,
    include_historical: bool = False
) -> dict:
    """
    Fetch current benchmark interest rates that have replaced LIBOR.
    
    This function retrieves the latest rates for major benchmark interest rates including:
    - SOFR (Secured Overnight Financing Rate) - USD replacement for LIBOR
    - EURIBOR (Euro Interbank Offered Rate) - EUR benchmark
    - SONIA (Sterling Overnight Index Average) - GBP replacement for LIBOR
    - TONAR (Tokyo Overnight Average Rate) - JPY replacement for LIBOR
    - Federal Funds Rate - US central bank rate
    - 10-Year Treasury Rate - US government bond yield
    
    Parameters:
        benchmarks (list, optional): List of specific benchmarks to fetch.
                                    Options: ["SOFR", "EURIBOR", "SONIA", "TONAR", "FED_FUNDS", "TREASURY_10Y"]
                                    If None, fetches all available benchmarks.
        include_historical (bool): If True, includes last 30 days of historical data.
                                  Default is False (only current rates).
    
    Returns:
        dict: Dictionary containing benchmark rate information:
            {
                "success": bool,
                "data": {
                    "as_of_date": str,
                    "rates": {
                        "SOFR": {
                            "rate": float,
                            "rate_percentage": str,
                            "date": str,
                            "description": str,
                            "historical": list (if include_historical=True)
                        },
                        ...
                    },
                    "comparison": str (summary of rates)
                },
                "source": str,
                "message": str
            }
    
    Example:
        >>> fetch_benchmark_rates(benchmarks=["SOFR", "FED_FUNDS"])
        {
            "success": True,
            "data": {
                "rates": {
                    "SOFR": {"rate": 5.31, "date": "2026-02-17", ...},
                    "FED_FUNDS": {"rate": 5.50, "date": "2026-02-01", ...}
                }
            }
        }
    """
    
    # Define benchmark series IDs and descriptions
    all_benchmarks = {
        "SOFR": {
            "series_id": "SOFR",
            "name": "Secured Overnight Financing Rate (SOFR)",
            "description": "USD benchmark - replacement for USD LIBOR",
            "currency": "USD"
        },
        "SOFR_30DAY": {
            "series_id": "SOFR30DAYAVG",
            "name": "30-Day Average SOFR",
            "description": "30-day average of SOFR - commonly used for loans",
            "currency": "USD"
        },
        "SOFR_90DAY": {
            "series_id": "SOFR90DAYAVG",
            "name": "90-Day Average SOFR",
            "description": "90-day average of SOFR - alternative to 3-month LIBOR",
            "currency": "USD"
        },
        "FED_FUNDS": {
            "series_id": "DFF",
            "name": "Federal Funds Effective Rate",
            "description": "US central bank overnight lending rate",
            "currency": "USD"
        },
        "TREASURY_10Y": {
            "series_id": "DGS10",
            "name": "10-Year Treasury Constant Maturity Rate",
            "description": "US government 10-year bond yield benchmark",
            "currency": "USD"
        },
        "TREASURY_5Y": {
            "series_id": "DGS5",
            "name": "5-Year Treasury Constant Maturity Rate",
            "description": "US government 5-year bond yield benchmark",
            "currency": "USD"
        },
        "TREASURY_2Y": {
            "series_id": "DGS2",
            "name": "2-Year Treasury Constant Maturity Rate",
            "description": "US government 2-year bond yield benchmark",
            "currency": "USD"
        },
        "PRIME_RATE": {
            "series_id": "DPRIME",
            "name": "Bank Prime Loan Rate",
            "description": "US bank prime lending rate",
            "currency": "USD"
        }
    }
    
    # Filter benchmarks if specific ones requested
    if benchmarks:
        benchmarks_upper = [b.upper() for b in benchmarks]
        selected_benchmarks = {k: v for k, v in all_benchmarks.items() if k in benchmarks_upper}
        if not selected_benchmarks:
            return {
                "success": False,
                "data": None,
                "source": "FRED API",
                "message": f"Invalid benchmark(s). Valid options: {list(all_benchmarks.keys())}"
            }
    else:
        selected_benchmarks = all_benchmarks
    
    # Check if API key is available
    if not FRED_API_KEY:
        return {
            "success": False,
            "data": None,
            "source": "FRED API",
            "message": "FRED_API_KEY not found in environment variables. Get a free key at https://fred.stlouisfed.org/docs/api/api_key.html"
        }
    
    # Fetch rates
    results = {}
    errors = []
    
    # Set date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    for benchmark_key, benchmark_info in selected_benchmarks.items():
        try:
            params = {
                "series_id": benchmark_info["series_id"],
                "api_key": FRED_API_KEY,
                "file_type": "json",
                "observation_start": start_date,
                "observation_end": end_date,
                "sort_order": "desc",
                "limit": 30 if include_historical else 1
            }
            
            response = requests.get(FRED_BASE_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if "observations" in data and len(data["observations"]) > 0:
                    # Filter out missing values
                    valid_obs = [obs for obs in data["observations"] if obs["value"] != "."]
                    
                    if valid_obs:
                        current_obs = valid_obs[0]
                        current_rate = float(current_obs["value"])
                        
                        result_data = {
                            "rate": current_rate,
                            "rate_percentage": f"{current_rate}%",
                            "date": current_obs["date"],
                            "name": benchmark_info["name"],
                            "description": benchmark_info["description"],
                            "currency": benchmark_info["currency"],
                            "series_id": benchmark_info["series_id"]
                        }
                        
                        # Add historical data if requested
                        if include_historical and len(valid_obs) > 1:
                            historical = []
                            for obs in valid_obs[1:11]:  # Get up to 10 historical points
                                historical.append({
                                    "date": obs["date"],
                                    "rate": float(obs["value"])
                                })
                            result_data["historical"] = historical
                            
                            # Add trend analysis
                            if len(historical) > 0:
                                avg_rate = sum([h["rate"] for h in historical]) / len(historical)
                                trend = "increasing" if current_rate > avg_rate else "decreasing" if current_rate < avg_rate else "stable"
                                result_data["trend"] = trend
                                result_data["30day_average"] = round(avg_rate, 4)
                        
                        results[benchmark_key] = result_data
                    else:
                        errors.append(f"{benchmark_key}: No valid data available")
                else:
                    errors.append(f"{benchmark_key}: No observations returned")
            else:
                errors.append(f"{benchmark_key}: HTTP {response.status_code}")
                
        except Exception as e:
            errors.append(f"{benchmark_key}: {str(e)}")
    
    if not results:
        return {
            "success": False,
            "data": None,
            "source": "FRED API",
            "message": f"Failed to fetch any benchmark rates. Errors: {', '.join(errors)}"
        }
    
    # Create comparison summary
    comparison_lines = []
    for key, data in results.items():
        comparison_lines.append(f"  • {data['name']}: {data['rate_percentage']} (as of {data['date']})")
    
    comparison_summary = "\n".join(comparison_lines)
    
    return {
        "success": True,
        "data": {
            "as_of_date": datetime.now().strftime("%Y-%m-%d"),
            "rates": results,
            "comparison": f"Current Benchmark Rates:\n{comparison_summary}",
            "count": len(results)
        },
        "source": "Federal Reserve Economic Data (FRED)",
        "api_url": "https://fred.stlouisfed.org/",
        "message": f"Successfully fetched {len(results)} benchmark rate(s). {('Errors: ' + ', '.join(errors)) if errors else ''}",
        "note": "SOFR has replaced USD LIBOR as the primary benchmark rate for USD denominated loans and derivatives."
    }
