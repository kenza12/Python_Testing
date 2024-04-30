from flask import url_for


def test_show_summary_valid_email(client, mock_simply_lift):
    """
        Test the '/showSummary' route with a valid email.
        This test ensures that if a valid email is provided, the server responds with a 200 status code
        and the expected 'Welcome' message is found in the response.
    """
    # Make the request with a valid email
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert 'Welcome' in response.get_data(as_text=True), "Welcome message not found in response"


def test_show_summary_invalid_email(client, mock_simply_lift):
    """
    Test the /showSummary route with an invalid email.
    """
    # Make the request with an invalid email
    response = client.post('/showSummary', data={'email': 'nonexistentemail@test.com'})
    assert response.status_code == 400
    assert "Sorry, that email was not found." in response.get_data(as_text=True), "Expected error message not found"
