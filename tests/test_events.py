def test_list_events(client):
    response = client.get("/api/events")
    assert response.status_code == 200
    assert len(response.get_json()) >= 5

def test_create_event(client):
    response = client.post("/api/events", json={
        "title":"Test Event","start_time":"2026-12-01T10:00:00",
        "end_time":"2026-12-01T11:00:00","capacity":50
    })
    assert response.status_code == 201
    assert response.get_json()["title"] == "Test Event"

def test_get_missing_event(client):
    response = client.get("/api/events/99999")
    assert response.status_code == 404
