def test_admin_can_post_official_update(client, admin_token):
    response = client.post(
        "/api/v1/admin/updates",
        json={
            "location_id": 1,
            "status": "OUTAGE",
            "message": "Fault confirmed. Restoration team dispatched.",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 201
    assert response.json()["status"] == "OUTAGE"

    dashboard_response = client.get(
        "/api/v1/admin/dashboard?location_id=1",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert dashboard_response.status_code == 200
    assert dashboard_response.json()["official_status"] == "OUTAGE"

