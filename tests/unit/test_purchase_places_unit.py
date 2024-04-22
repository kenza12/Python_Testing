import pytest

@pytest.mark.parametrize("requested_places, expected_message, expected_status", [
    (5, 'Not enough points', 200),  # insufficient_points
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

    # Perform POST request to purchase 13 places
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Fall Classic',
        'places': 13
    })
    
    assert 'Cannot book more than 12 places per competition' in response.get_data(as_text=True)