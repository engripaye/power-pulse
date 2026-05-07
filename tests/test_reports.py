def test_report_outage_and_view_status(client, user_token):
    response = client.post(
        "/api/v1/reports",
        json={"location_id": 1, "status": "OUTAGE"},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 201
    assert response.json()["status"] == "OUTAGE"

    status_response = client.get("/api/v1/status/1")

    assert status_response.status_code == 200
    payload = status_response.json()
    assert payload["community_status"] == "OUTAGE"
    assert payload["outage_reports_last_hour"] == 1

