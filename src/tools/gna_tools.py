import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool
def get_gna_cases(
    application: str,
    from_date: str,
    to_date: str,
    subscriber_identifier: str,
    timeout: int = 30
) -> dict:
    """Fetch Grievance and Appeals (GNA) cases for a given subscriber within a date range."""
    base_url = os.getenv("GNA_API_URL", "https://mock.api/cases")
    api_key = os.getenv("GNA_API_KEY", "mock_key")

    headers = {
        "x-api-key": api_key,
        "Accept": "application/json"
    }

    params = {
        "application": application,
        "fromDate": from_date,
        "toDate": to_date,
        "subscriberIdentifier": subscriber_identifier
    }

    try:
        response = requests.get(
            base_url,
            headers=headers,
            params=params,
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": "Failed to fetch cases, returning mock data",
            "mock_data": [
                {"case_id": "GNA-1001", "status": "In Progress", "type": "Appeal", "date": from_date}
            ]
        }

@tool
def get_case_details(case_id: str) -> dict:
    """Retrieve detailed information about a specific GNA case by its case_id."""
    url = f"https://uat.api.psgbd.ps.awsdsn.internal.das/gna-gateway/v2/gna/cases/{case_id}"
    headers = {
        "x-api-key": "B8kdzNaXgdMeeame5V21GQUCZdvJHO5Z",
        "application": "Compass"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch details for case {case_id}, returning mock details",
            "mock_data": {
                "case_id": case_id,
                "status": "In Review",
                "description": "Patient is appealing denial of out-of-network MRI claim.",
                "last_update": "2026-04-01"
            }
        }