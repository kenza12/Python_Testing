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
    

def test_purchase_places_past_competition(browser, login, submit_booking_request):
    """test to attempt booking places for a past competition and expect to fail."""
    # Log in first
    login('admin@irontemple.com')

    # Wait for the entire list of competitions to be visible
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "ul"))
    )

    # Find the list item for 'Historic Match'
    historic_match_li = browser.find_element(By.XPATH, "//li[contains(., 'Historic Match')]")
    
    # Within this list item, click the 'Book Places' link
    book_places_link = historic_match_li.find_element(By.LINK_TEXT, 'Book Places')
    book_places_link.click()

    # Use the submit_booking_request to attempt booking one place
    submit_booking_request(1)

    # Check for the error message indicating booking cannot be made for past competitions
    try:
        WebDriverWait(browser, 5).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'body'), "Cannot book places for past competitions"
            )
        )
        assert "Cannot book places for past competitions" in browser.page_source, \
            "Should display a message about past competitions"
    except TimeoutException:
        print("TimeoutException caught. Error message did not appear.")
        assert False, "Error message did not appear within the expected time."
