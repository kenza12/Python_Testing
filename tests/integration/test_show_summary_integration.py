
from flask import url_for


def test_show_summary_valid_email(client):
    """Test the /showSummary route with a valid email."""
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert 'Welcome' in response.data.decode()


def test_show_summary_invalid_email(client):
    """Test the /showSummary route with an invalid email."""
    with client.application.app_context():
        response = client.post('/showSummary', data={'email': 'nonexistentemail@test.com'})
        assert response.status_code == 302
        assert url_for('index') in response.headers['Location'], "Redirection to 'index' not found"