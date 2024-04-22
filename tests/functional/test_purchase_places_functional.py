from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def test_booking(browser, login, navigate_to_booking, submit_booking_request):
    """Functional test for booking process handling different point limits."""

    # Test for insufficient points
    login('admin@irontemple.com')
    navigate_to_booking()
    submit_booking_request(5)  # More than available points
    try:
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Not enough points"))
        assert "Not enough points" in browser.page_source, "Should display a message about insufficient points"
    except TimeoutException:
        print("TimeoutException caught. Not enough points message did not appear.")
        assert False, "Not enough points message did not appear within the expected time."

    # Test for sufficient points
    login('admin@irontemple.com')
    navigate_to_booking()
    submit_booking_request(3)  # Within the available points
    try:
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Great-booking complete!"))
        assert "Great-booking complete!" in browser.page_source, "Booking should be confirmed as successful"
    except TimeoutException:
        print("TimeoutException caught. Great-booking complete message did not appear.")
        assert False, "Great-booking complete message did not appear within the expected time."


def test_purchase_places_limitation(browser, login, navigate_to_booking, submit_booking_request):
    """
    Test to verify that the system properly displays an error when trying to book more than 12 places.
    """
    login('john@simplylift.co')
    navigate_to_booking()

    # Attempt to book 13 places
    submit_booking_request(13)

    # Check for the presence of an error message
    try:
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Cannot book more than 12 places per competition"))
        assert "Cannot book more than 12 places per competition" in browser.page_source, "Should display a message about the places limit"
    except TimeoutException:
        print("TimeoutException caught. Error message did not appear.")
        assert False, "Error message did not appear within the expected time."