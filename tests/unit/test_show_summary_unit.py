from flask import url_for


def test_show_summary_valid_email(client, mocker):
    """
        Test the '/showSummary' route with a valid email.
        This test ensures that if a valid email is provided, the server responds with a 200 status code
        and the expected 'Welcome' message is found in the response.
    """
    # Mock 'clubs' to return a list with a valid club
    mocked_clubs = [{'email': 'john@simplylift.co', 'name': 'Simply Lift', 'points': 13}]
    mocker.patch('server.clubs', new=mocked_clubs)
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert 'Welcome' in response.get_data(as_text=True), "Welcome message not found in response"


def test_show_summary_invalid_email(client):
    """
    Test the '/showSummary' route with an invalid email.
    This test checks that the server correctly redirects the user to the index page
    when an invalid email is submitted, responding with a 302 status code.
    """
    with client.application.app_context():
        response = client.post('/showSummary', data={'email': 'nonexistentemail@test.com'})
        assert response.status_code == 302, "Expected HTTP 302 redirect"
        assert url_for('index') in response.headers['Location'], "Redirection to 'index' not found"

