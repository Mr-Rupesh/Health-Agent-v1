from typing import Dict

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun


@tool
def bmi_calculator(weight_kg: float, height_cm: float) -> Dict:
    """
    Calculate BMI using weight in kilograms and height in centimeters.
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return {
        "bmi": round(bmi, 2),
        "category": category
    }


@tool
def symptom_search(query: str) -> str:
    """
    Search the web for symptom-related medical information.
    """
    search = DuckDuckGoSearchRun()
    return search.run(query)


@tool
def suggest_doctor(symptom_category: str) -> Dict:
    """
    Suggest an appropriate doctor specialty based on symptom category.
    Categories: fever, cold, cough, skin, heart, eye, ear, nose, throat,
    bone, joint, stomach, digestive, lung, breathing, brain, mental,
    kidney, urinary, women, child.
    """
    doctor_mapping = {
        "fever": "General Physician",
        "cold": "General Physician",
        "cough": "General Physician",
        "skin": "Dermatologist",
        "heart": "Cardiologist",
        "eye": "Ophthalmologist",
        "ear": "ENT Specialist",
        "nose": "ENT Specialist",
        "throat": "ENT Specialist",
        "bone": "Orthopedic",
        "joint": "Orthopedic",
        "stomach": "Gastroenterologist",
        "digestive": "Gastroenterologist",
        "lung": "Pulmonologist",
        "breathing": "Pulmonologist",
        "brain": "Neurologist",
        "mental": "Psychiatrist",
        "kidney": "Nephrologist",
        "urinary": "Urologist",
        "women": "Gynecologist",
        "child": "Pediatrician",
    }

    return {
        "symptom_category": symptom_category,
        "recommended_doctor": doctor_mapping.get(
            symptom_category.lower(),
            "General Physician"
        )
    }


tools_list = [
    bmi_calculator,
    symptom_search,
    suggest_doctor,
]