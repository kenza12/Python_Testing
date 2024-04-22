import pytest


@pytest.mark.parametrize("requested_places, expected_message, expected_status", [
    (5, 'Not enough points', 200),  # insufficient_points
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
    assert response.status_code == 200, "Expected HTTP status code 200"