from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_logout(browser, login):
    """
    Test to verify that the logout process correctly logs out the user and redirects to the home page.
    This test checks for the specific title on the home page to confirm redirection.
    """
    # Login first
    login('john@simplylift.co')

    # Wait for the footer to be visible which indicates the page has loaded
    WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "footer"))
    )

    # Navigate to the logout link
    logout_link = browser.find_element(By.LINK_TEXT, 'Logout')
    logout_link.click()

    # Wait for the redirection to the home page
    WebDriverWait(browser, 5).until(
        EC.title_is("Welcome | GUDLFT Registration")
    )

    # Verify the title to ensure it's the home page
    assert browser.title == "Welcome | GUDLFT Registration", "Did not redirect to the expected home page after logout"