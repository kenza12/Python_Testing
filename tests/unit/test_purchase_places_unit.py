import pytest

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