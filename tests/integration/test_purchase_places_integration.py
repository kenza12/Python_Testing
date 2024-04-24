import pytest
from server import loadClubs

@pytest.mark.parametrize("requested_places, expected_message, expected_status", [
    (5, 'Not enough points', 400),  # insufficient_points
    (2, 'Great-booking complete!', 200)  # sufficient_points
])

def test_booking(client, requested_places, expected_message, expected_status):
    """
    Test integration of the booking process, checking both under and over point limit scenarios.
    """
    club_name = 'Iron Temple'
    competition_name = 'Spring Festival'

    # Perform POST request to purchase places
    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': requested_places
    })

    # Verify the response
    assert expected_message in response.get_data(as_text=True), f"Expected message '{expected_message}' not found"
    assert response.status_code == expected_status, f"Expected status code {expected_status}"


def test_purchase_places_limitation(client):
    """
    Verify that the application does not allow a booking of more than 12 places.
    """
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Fall Classic',
        'places': 13  # Requesting more than the allowed limit
    })

    assert 'Cannot book more than 12 places per competition' in response.get_data(as_text=True)
    assert response.status_code == 400, "Expected HTTP status code 400"


def test_purchase_places_for_past_competition(client):
    """
    Verify that the application does not allow a booking of past competition.
    """
    response = client.post('/purchasePlaces', data={
        'club': 'Iron Temple',
        'competition': 'Historic Match',
        'places': '5'
    })

    # Check that the booking was not allowed
    assert 'Cannot book places for past competitions' in response.get_data(as_text=True), "Booking for past competition should not be allowed"
    assert response.status_code == 400, "Expected status code 400 for booking past competition"



def test_purchase_places_deduct_points(client, app_context):
    """
    Verify that points are correctly deducted from a club's total when booking places for a competition in an integration test setting.
    This test checks the 'She Lifts' club booking places for the 'Deducted Festival'.
    """
    club_name = 'She Lifts'
    competition_name = 'Deducted Festival'
    places_to_book = 2
    initial_points = 12  # Updated to reflect the actual points from 'She Lifts' club data

    # Fetch initial state for debug
    initial_clubs = loadClubs()
    initial_club = next((c for c in initial_clubs if c['name'] == club_name), None)
    print(f"Initial points (before booking): {initial_club['points']}")

    # Perform the booking
    client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': str(places_to_book)  # Ensure the data type matches expected input
    })

    # Fetch updated state, assume direct access to club data from a reloaded source
    updated_clubs = loadClubs()
    updated_club = next((c for c in updated_clubs if c['name'] == club_name), None)

    # Print updated points for debug
    print(f"Updated points (after booking): {updated_club['points']}")

    # Calculate expected points after booking
    expected_points_after_booking = initial_points - places_to_book
    
    # Assert the points are deducted correctly
    assert updated_club is not None, "The club should be found in the list."
    assert int(updated_club['points']) == expected_points_after_booking, "The points should be deducted correctly after booking."

