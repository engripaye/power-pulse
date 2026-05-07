def test_complaint_flow(client, user_token, admin_token):
    create_response = client.post(
        "/api/v1/complaints",
        json={"location_id": 1, "message": "Transformer has been down since morning."},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert create_response.status_code == 201
    complaint_id = create_response.json()["id"]

    list_response = client.get(
        "/api/v1/complaints",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    respond_response = client.patch(
        f"/api/v1/complaints/{complaint_id}",
        json={"status": "RESOLVED", "response": "A crew has restored the feeder."},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert respond_response.status_code == 200
    assert respond_response.json()["status"] == "RESOLVED"

