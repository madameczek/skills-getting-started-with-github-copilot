"""Pytest configuration and shared fixtures for test isolation."""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def reset_activities():
    """
    Fixture to reset activities to original state before each test.
    This ensures test isolation by providing a fresh copy of activities data.
    """
    # Store original activities data
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for intramural and tournament play",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in friendly matches",
            "schedule": "Saturdays, 10:00 AM - 11:30 AM",
            "max_participants": 10,
            "participants": ["james@mergington.edu", "lucas@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and various art techniques",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Ensemble": {
            "description": "Play instruments and perform in school concerts",
            "schedule": "Mondays, Wednesdays, Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 25,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
        }
    }
    
    # Clear existing activities
    activities.clear()
    
    # Reset with deep copy to avoid mutations affecting the original
    activities.update(copy.deepcopy(original_activities))
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


@pytest.fixture
def client(reset_activities):
    """
    Fixture to provide a TestClient instance for testing API endpoints.
    Depends on reset_activities to ensure clean state.
    """
    return TestClient(app)
