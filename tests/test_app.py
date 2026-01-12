import pytest
from src.app import activities


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success(client):
    # Test signing up for an activity with available spots
    response = client.post("/activities/Basketball%20Team/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up test@mergington.edu for Basketball Team" in data["message"]

    # Verify the participant was added
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" in data["Basketball Team"]["participants"]


def test_signup_for_activity_not_found(client):
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_for_activity_already_signed_up(client):
    # First sign up
    client.post("/activities/Basketball%20Team/signup?email=duplicate@mergington.edu")
    # Try to sign up again
    response = client.post("/activities/Basketball%20Team/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_unregister_from_activity_success(client):
    # First sign up
    client.post("/activities/Soccer%20Club/signup?email=unregister@mergington.edu")
    # Then unregister
    response = client.delete("/activities/Soccer%20Club/unregister?email=unregister@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered unregister@mergington.edu from Soccer Club" in data["message"]

    # Verify the participant was removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@mergington.edu" not in data["Soccer Club"]["participants"]


def test_unregister_from_activity_not_found(client):
    response = client.delete("/activities/Nonexistent%20Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_from_activity_not_signed_up(client):
    response = client.delete("/activities/Chess%20Club/unregister?email=notsignedup@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student is not signed up for this activity"