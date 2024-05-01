import pytest
import server

@pytest.mark.parametrize("requested_places, expected_message, expected_status", [
    (5, 'Not enough points', 400),  # insufficient_points
    (2, 'Great-booking complete!', 200)  # sufficient_points
])
def test_booking(client, mock_iron_temple, requested_places, expected_message, expected_status):
    """
    Test to ensure that the booking process behaves correctly based on club points availability.
    """
    club_name = 'Iron Temple'
    competition_name = 'Spring Festival'

    # Perform POST request to purchase places
    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': requested_places
    })

    # Verify the response based on expected outcomes
    assert expected_message in response.get_data(as_text=True), f"Expected message '{expected_message}' not found"
    assert response.status_code == expected_status, f"Expected status code {expected_status}"


def test_purchase_places_limitation(client, mock_simply_lift):
    """
    Test to ensure that the booking process doesn't exceed 12 places.
    """

    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Fall Classic',
        'places': 13  # Requesting more than the allowed limit
    })

    assert 'Cannot book more than 12 places per competition' in response.get_data(as_text=True)
    assert response.status_code == 400, "Expected HTTP status code 400"


def test_purchase_places_past_competition(client, mock_iron_temple_with_past_competition):
    """Test that booking a place in a past competition should fail."""

    response = client.post('/purchasePlaces', data={
        'club': 'Iron Temple',
        'competition': 'Historic Match',  # Use past competition
        'places': 1
    })
    
    assert 'Cannot book places for past competitions' in response.get_data(as_text=True)
    assert response.status_code == 400  # Expected HTTP status code 400


def test_purchase_places_deduct_points(client, mock_energy_club, mock_load_clubs):
    """
    Verify that points are correctly deducted from a club's total when booking places for a competition.
    
    Args:
        client (Flask test client): The test client for making requests.
        mock_energy_club (fixture): Mocks the club data for Energy Club.
        mock_load_clubs (fixture): Mocks the loadClubs function to simulate updated club data.
    """
    club_name = 'Energy Club'
    competition_name = 'Energy Open'
    places_to_book = 5
    expected_points_after_booking = 10  # Expected points after booking 5 places

    # Perform the booking
    client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': places_to_book
    })

    # Fetch updated club data
    updated_clubs = server.loadClubs()
    club = next((c for c in updated_clubs if c['name'] == club_name), None)

    # Assert the points are deducted correctly
    assert club is not None, "The club should be found in the list."
    assert int(club['points']) == expected_points_after_booking, "The points should be deducted correctly after booking."


@pytest.mark.parametrize(
    "club_name, competition_name, requested_places, expected_status, expected_message",
    [
        # Happy Path: book less than available places
        ("Simply Lift", "Avail Festival", 3, 200, 'Great-booking complete!'),
        # Sad Path: book more than available places
        ("Simply Lift", "Avail Festival", 5, 400, 'Cannot book more places than are available.')
    ]
)
def test_purchase_places(client, mock_availability_limitation, club_name, competition_name, requested_places, expected_status, expected_message):
    """
    Test to ensure that the booking process behaves correctly when trying to book places, depending on the availability.
    """
    # Perform POST request to book places
    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': requested_places
    })

    # Check that the HTTP response and error message (if any) are correct
    assert response.status_code == expected_status
    assert expected_message in response.get_data(as_text=True), "The response message is not as expected"