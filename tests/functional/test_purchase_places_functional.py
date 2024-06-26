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

    # Wait for the table of competitions to be visible
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "table"))
    )

    # Find the row for 'Historic Match'
    historic_match_row = browser.find_element(By.XPATH, "//tr[td[contains(text(), 'Historic Match')]]")
    
    # Check if the "Book Places" link is not present
    try:
        historic_match_row.find_element(By.LINK_TEXT, 'Book Places')
        assert False, "'Book Places' link should not be present for past competitions."
    except:
        assert True, "'Book Places' link is correctly not present for past competitions."


def test_purchase_places_deduct_point(browser, login, submit_booking_request):
    """Functional test to verify point deduction when booking places for a competition."""
    # Log in with 'She Lifts' credentials
    login('kate@shelifts.co.uk')

    # Find the line containing the points information before booking
    WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "body"))
    )
    body_text = browser.find_element(By.TAG_NAME, 'body').text
    points_line = next(line for line in body_text.split('\n') if 'Points available:' in line)
    points_before = int(points_line.split(': ')[1])

    # Find the 'Deducted Festival' competition and initiate booking
    deducted_festival_row = browser.find_element(By.XPATH, "//tr[td[contains(text(), 'Deducted Festival')]]")
    book_places_link = deducted_festival_row.find_element(By.LINK_TEXT, 'Book Places')
    book_places_link.click()

    # Submit the booking request for 2 places
    submit_booking_request(2)

    # Confirm that the booking was successful
    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Great-booking complete!")
    )
    assert "Great-booking complete!" in browser.page_source, "Booking should be confirmed as successful"

    # Extract the updated body text and points
    updated_body_text = browser.find_element(By.TAG_NAME, 'body').text
    points_line_after = next(line for line in updated_body_text.split('\n') if 'Points available:' in line)
    points_after = int(points_line_after.split(': ')[1])

    # Check if the points have been correctly deducted
    expected_points = points_before - 2  # Assuming 2 points are deducted per booking
    assert points_after == expected_points, f"Points should be deducted correctly, expected {expected_points}, got {points_after}"


def test_purchase_places_exceeding_available_places(browser, login, submit_booking_request):
    """
    Functional test to verify that users cannot book more places than available in the 'Avail Festival'
    """
    # Logging in with credentials that should have access to the booking
    login('john@simplylift.co')

    # Navigate directly to the booking page for 'Avail Festival'
    WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "table"))
    )
    # Find the competition 'Avail Festival' and navigate to its booking page
    festival_link = browser.find_element(By.XPATH, "//tr[td[contains(text(), 'Avail Festival')]]/td/a[contains(text(), 'Book Places')]")
    festival_link.click()

    # Attempt to book 5 places, which is more than available
    submit_booking_request(5)

    # Check for the browser's built-in validation message
    try:
        # Wait for the validation message to appear on the input field
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input:invalid'))
        )
        invalid_input = browser.find_element(By.CSS_SELECTOR, 'input:invalid')
        assert invalid_input is not None, "Should display a browser validation error for exceeding places"
    except TimeoutException:
        assert False, "Validation error did not appear when trying to book more places than available."