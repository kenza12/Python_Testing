
from flask import url_for


def test_show_summary_valid_email(client):
    """Test the /showSummary route with a valid email."""
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert 'Welcome' in response.data.decode()


def test_show_summary_invalid_email(client):
    """Test the /showSummary route with an invalid email."""

    response = client.post('/showSummary', data={'email': 'nonexistentemail@test.com'})
    assert response.status_code == 400
    assert "Sorry, that email was not found." in response.get_data(as_text=True), "Expected error message not found"