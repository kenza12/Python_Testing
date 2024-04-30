from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_valid_email_entry(browser, login):
    """
    Tests if entering a valid email shows the welcome message.
    """
    login('john@simplylift.co')
    # Wait for flash message to appear
    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Welcome")
    )
    assert "Welcome" in browser.page_source, "Expected 'Welcome' not found in the page source"


def test_invalid_email_entry(browser, login):
    """
    Tests if entering an invalid email shows the error message.
    """
    login('doesnotexist@test.com')
    # Wait for flash message to appear
    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Sorry, that email was not found.")
    )
    assert "Sorry, that email was not found." in browser.page_source, "Expected error message not found"
