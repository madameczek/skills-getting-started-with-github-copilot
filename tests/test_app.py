"""
API endpoint tests using Arrange-Act-Assert (AAA) pattern.

Each test follows the structure:
- Arrange: Set up test data and preconditions
- Act: Execute the endpoint being tested
- Assert: Verify the response and side effects
"""

import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to the static index.html page.
        
        Arrange: TestClient is ready
        Act: Make GET request to root endpoint
        Assert: Status code is 307 (temporary redirect) with correct location
        """
        # Arrange
        # (client fixture is already set up)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers.get("location", "")


class TestGetActivitiesEndpoint:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all available activities.
        
        Arrange: TestClient is ready with initial activities
        Act: Make GET request to /activities
        Assert: Response contains all activities with correct structure
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Ensemble",
            "Debate Team",
            "Science Club"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert all(activity in activities for activity in expected_activities)

    def test_get_activities_returns_correct_structure(self, client):
        """
        Test that each activity has the required fields.
        
        Arrange: TestClient is ready
        Act: Make GET request to /activities and inspect structure
        Assert: Each activity has description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert all(field in activity_data for field in required_fields)
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_student_success(self, client):
        """
        Test successful signup of a new student for an activity.
        
        Arrange: TestClient ready, new email address prepared
        Act: POST signup request with activity name and email
        Assert: Status 200, success message returned, participant added to activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]
        
        # Verify participant was added to activity
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client):
        """
        Test signup fails when activity doesn't exist.
        
        Arrange: TestClient ready, non-existent activity name
        Act: POST signup request with fake activity name
        Assert: Status 404, error message indicates activity not found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_student_fails(self, client):
        """
        Test that duplicate signup for same student fails.
        
        Arrange: TestClient ready, student already in activity
        Act: POST signup request with email already in participants
        Assert: Status 400, error indicates already signed up
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_multiple_students_same_activity(self, client):
        """
        Test that multiple different students can sign up for same activity.
        
        Arrange: TestClient ready, two different new emails
        Act: POST signup requests for two different students
        Assert: Both signup successfully, both appear in participants
        """
        # Arrange
        activity_name = "Chess Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"

        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]

    def test_signup_increments_participant_count(self, client):
        """
        Test that participant count increases after successful signup.
        
        Arrange: TestClient ready, get initial participant count
        Act: POST signup request
        Assert: Participant count increased by 1
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count + 1


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_existing_student_success(self, client):
        """
        Test successful unregistration of an existing student.
        
        Arrange: TestClient ready, student is in activity
        Act: DELETE unregister request with existing student email
        Assert: Status 200, success message, participant removed from activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_activity_not_found(self, client):
        """
        Test unregister fails when activity doesn't exist.
        
        Arrange: TestClient ready, non-existent activity name
        Act: DELETE unregister request with fake activity name
        Assert: Status 404, error message indicates activity not found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_student_not_registered(self, client):
        """
        Test unregister fails when student is not in activity.
        
        Arrange: TestClient ready, student not in activity
        Act: DELETE unregister request with email not in participants
        Assert: Status 400, error indicates student not registered
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notstudent@mergington.edu"  # Not in Chess Club

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]

    def test_unregister_decrements_participant_count(self, client):
        """
        Test that participant count decreases after successful unregister.
        
        Arrange: TestClient ready, get initial participant count
        Act: DELETE unregister request
        Assert: Participant count decreased by 1
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count - 1

    def test_signup_then_unregister_sequence(self, client):
        """
        Test complete signup-unregister workflow.
        
        Arrange: TestClient ready
        Act: 1) Signup student 2) Verify participant added 3) Unregister student
        Assert: All operations succeed, final state matches initial
        """
        # Arrange
        activity_name = "Chess Club"
        email = "tempstudent@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity_name]["participants"]

        # Act - Step 1: Signup
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert - Step 1
        assert signup_response.status_code == 200

        # Act - Step 2: Verify added
        check_response = client.get("/activities")
        participants_after_signup = check_response.json()[activity_name]["participants"]

        # Assert - Step 2
        assert email in participants_after_signup
        assert len(participants_after_signup) == len(initial_participants) + 1

        # Act - Step 3: Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert - Step 3
        assert unregister_response.status_code == 200
        
        final_response = client.get("/activities")
        final_participants = final_response.json()[activity_name]["participants"]
        assert email not in final_participants
        assert len(final_participants) == len(initial_participants)
