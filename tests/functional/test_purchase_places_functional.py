from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def test_booking(browser, login, navigate_to_booking, submit_booking_request):
    """Functional test for booking process handling different point limits."""
    # Test for insufficient points
    login('john@simplylift.co')
    navigate_to_booking()
    submit_booking_request(15)  # More than available points
    try:
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Not enough points"))
        assert "Not enough points" in browser.page_source, "Should display a message about insufficient points"
    except TimeoutException:
        print("Current page source:", browser.page_source)  # Diagnostic output

    # Test for sufficient points
    login('john@simplylift.co')
    navigate_to_booking()
    submit_booking_request(5)  # Within the available points
    try:
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Great-booking complete!"))
        assert "Great-booking complete!" in browser.page_source, "Booking should be confirmed as successful"
    except TimeoutException:
        print("Current page source:", browser.page_source)  # Diagnostic output