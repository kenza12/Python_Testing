def test_index_club_points_display(client, mock_load_clubs):
    """
    Test to ensure that the index page correctly displays the list of clubs and their points.
    This test checks if the rendered page contains the expected points for each club after they have been possibly updated.
    """
    # Fetch the index page
    response = client.get('/')
    assert response.status_code == 200, "Expected HTTP status 200 for the index page"

    # Expected data from mock_load_clubs
    expected_clubs = mock_load_clubs.return_value

    # Check if the response contains the expected points for each club
    page_content = response.get_data(as_text=True)
    for club in expected_clubs:
        assert club['name'] in page_content, f"Club name {club['name']} not found in the response"
        assert str(club['points']) in page_content, f"Club points {club['points']} for {club['name']} not found in the response"