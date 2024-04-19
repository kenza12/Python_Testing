from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_valid_email_entry(browser):
    """
    Tests if entering a valid email shows the welcome message.
    """
    browser.get('http://127.0.0.1:5000')
    email_input = browser.find_element(By.NAME, 'email')
    email_input.send_keys('john@simplylift.co')
    email_input.send_keys(Keys.RETURN)
    # Wait for flash message to appear
    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Welcome")
    )
    assert "Welcome" in browser.page_source, "Expected 'Welcome' not found in the page source"

def test_invalid_email_entry(browser):
    """
    Tests if entering an invalid email shows the error message.
    """
    browser.get('http://127.0.0.1:5000')
    email_input = browser.find_element(By.NAME, 'email')
    email_input.send_keys('doesnotexist@test.com')
    email_input.send_keys(Keys.RETURN)
    # Wait for flash message to appear
    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "Sorry, that email wasn't found")
    )
    assert "Sorry, that email wasn't found" in browser.page_source, "Expected error message not found"
