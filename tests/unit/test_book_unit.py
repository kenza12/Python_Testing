import pytest


@pytest.mark.parametrize(
    "competition, club, expected_status, expected_message",
    [
        ("Spring Festival", "Iron Temple", 200, "Book"),  # Known club and competition
        ("Unknown Festival", "Unknown Club", 200, "Something went wrong-please try again")  # Unknown club and competition
    ]
)


def test_book_page_access(client, mock_iron_temple, competition, club, expected_status, expected_message):
    """
    Test to verify that the booking page responds correctly based on whether the specified club and competition exist or not.
    """
    response = client.get(f'/book/{competition}/{club}')
    assert response.status_code == expected_status
    assert expected_message in response.get_data(as_text=True), "The response did not contain the expected message"