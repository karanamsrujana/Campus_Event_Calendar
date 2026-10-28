def test_rsvp_success(client):
    response = client.post("/api/events/1/rsvp", json={
        "student_name":"Test Student","student_email":"test@example.com","student_id":"T001"
    })
    assert response.status_code == 201
    assert response.get_json()["event"]["rsvp_count"] >= 1

def test_duplicate_rsvp_rejected(client):
    payload={"student_name":"Test","student_email":"duplicate@example.com","student_id":"T002"}
    assert client.post("/api/events/1/rsvp", json=payload).status_code == 201
    assert client.post("/api/events/1/rsvp", json=payload).status_code == 409
