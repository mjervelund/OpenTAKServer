import base64


def test_marti_api_clientendpoints(client):
    response = client.get("/Marti/api/clientEndPoints")
    assert response.status_code == 200


def test_mart_api_tls_config(auth):
    creds = base64.b64encode(b"TestUser:TestPass").decode("utf-8")
    response = auth.get(
        "/Marti/api/tls/config", headers={"Authorization": "Basic {}".format(creds)}
    )
    assert response.status_code == 200


def test_points(auth):
    response = auth.get("/api/point")
    assert response.status_code == 200


def test_me(auth):
    response = auth.get("/api/me")
    assert response.json["username"] == "TestUser"


def test_atak_qr_string_username_case(auth):
    # Usernames are looked up case insensitively, but the token must use the stored one
    response = auth.client.post(
        "/api/atak_qr_string", headers=auth.headers, json={"username": "testuser"}
    )
    assert response.status_code == 200
    assert "&username=TestUser&" in response.json["qr_string"]


def test_certificate_username_case(app, auth):
    from opentakserver.models.Certificate import Certificate

    response = auth.client.post(
        "/api/certificate", headers=auth.headers, json={"username": "testuser"}
    )
    assert response.status_code == 200

    with app.app_context():
        cert = Certificate.query.filter_by(common_name="TestUser").first()
        assert cert is not None
        assert cert.username == "TestUser"
