from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_updates_activity_participants_immediately():
    activity_name = "Art Studio"
    email = "new.student@mergington.edu"

    client.delete(f"/activities/{activity_name}/signup?email={email}")

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200

    activity = client.get("/activities").json()[activity_name]
    assert email in activity["participants"]


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name.replace(' ', '%20')}/signup?email={email}"
    )

    assert response.status_code == 200
    assert email not in response.json()["participants"]

    repeat_response = client.delete(
        f"/activities/{activity_name.replace(' ', '%20')}/signup?email={email}"
    )
    assert repeat_response.status_code == 404
