from typing import Dict
from langchain_core.tools import tool

NORMAL_RANGES = {
    "hemoglobin": (13.5, 17.5),      # g/dL
    "fasting_sugar": (70, 100),      # mg/dL
    "bp_systolic": (90, 120),        # mmHg
    "bp_diastolic": (60, 80),        # mmHg
    "cholesterol": (0, 200),         # mg/dL
    "creatinine": (0.6, 1.3),        # mg/dL
    "wbc_count": (4000, 11000),      # cells/µL
}


def analyze_report(report: dict) -> dict:
    """
    Analyze lab report values against normal ranges.
    """

    analysis = {}

    for test_name, value in report.items():

        if test_name not in NORMAL_RANGES:
            analysis[test_name] = {
                "value": value,
                "status": "Unknown Test",
                "normal_range": "N/A"
            }
            continue

        low, high = NORMAL_RANGES[test_name]

        if value < low:
            status = "Low"
        elif value > high:
            status = "High"
        else:
            status = "Normal"

        analysis[test_name] = {
            "value": value,
            "status": status,
            "normal_range": f"{low}-{high}"
        }

    return analysis

@tool
def analyze_health_report(
    hemoglobin: float = None,
    fasting_sugar: float = None,
    bp_systolic: float = None,
    bp_diastolic: float = None,
    cholesterol: float = None,
    creatinine: float = None,
    wbc_count: float = None,
) -> Dict:
    """
    Analyze common health report values and identify whether each value
    is Low, Normal, or High compared to standard reference ranges.
    Only pass the values the user actually provided — skip the rest.
    """
    report = {
        "hemoglobin": hemoglobin,
        "fasting_sugar": fasting_sugar,
        "bp_systolic": bp_systolic,
        "bp_diastolic": bp_diastolic,
        "cholesterol": cholesterol,
        "creatinine": creatinine,
        "wbc_count": wbc_count,
    }
    report = {k: v for k, v in report.items() if v is not None}
    return analyze_report(report)