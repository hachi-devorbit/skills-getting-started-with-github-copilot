from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_adds_student_to_activity():
    # Arrange
    activity_name = "Art Studio"
    email = "new.student@mergington.edu"
    client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_rejects_duplicate_student():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_rejects_unknown_activity():
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_student_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in response.json()["participants"]

    repeat_response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert repeat_response.status_code == 404


def test_unregister_rejects_student_not_in_activity():
    # Arrange
    activity_name = "Soccer Team"
    email = "not-a-member@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
