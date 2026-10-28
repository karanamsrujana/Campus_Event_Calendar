def test_attendance_report(client):
    response=client.get("/api/reports/attendance")
    assert response.status_code == 200
    assert "attendance_percentage" in response.get_json()[0]

def test_csv_export(client):
    response=client.get("/api/reports/attendance/csv")
    assert response.status_code == 200
    assert "event_id" in response.get_data(as_text=True)
    assert "text/csv" in response.content_type
