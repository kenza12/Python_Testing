def test_logout(client):
    """
    Test that the logout endpoint issues a redirect to the home page.
    """
    # Send a request to the logout route without following redirects
    response = client.get('/logout')
    
    # Check that a 302 redirect response is returned
    assert response.status_code == 302, "Logout should issue a redirect response."
    
    # Check if the redirect location is home
    assert response.headers['Location'] == "/", "The redirect location should be the home page URL."