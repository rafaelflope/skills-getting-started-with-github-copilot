from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()


def test_signup_for_activity_success():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Ensure clean state
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_for_activity_duplicate_fails():
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"

    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 400


def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent Club/signup", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
