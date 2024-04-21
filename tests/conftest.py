import os
import sys

# Set the path to include the root directory for easy imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app as flask_app
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope='module')
def app():
    """Creates and configures a new app instance for testing."""
    flask_app.config.update({
        'TESTING': True,
        'DEBUG': True,
        'FLASK_ENV': 'development',
        'SECRET_KEY': 'verysecret',
        'SERVER_NAME': 'localhost.localdomain:5000'
    })
    return flask_app

@pytest.fixture(scope='module')
def client(app):
    """Provides a test client for the Flask application."""
    return app.test_client()

@pytest.fixture(scope='module')
def browser():
    """
    Provides a WebDriver instance for Selenium tests.
    """
    from selenium import webdriver
    driver = webdriver.Firefox()
    yield driver
    driver.quit()

@pytest.fixture
def mock_competition_and_clubs(mocker):
    """Prepare and inject mocked club and competition data into the server context."""
    mocked_clubs = [{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': 10}]
    mocker.patch('server.clubs', new=mocked_clubs)

    mocked_competitions = [{'name': 'Spring Festival', 'numberOfPlaces': 5}]
    mocker.patch('server.competitions', new=mocked_competitions)

@pytest.fixture
def navigate_to_booking(browser):
    """Navigates to the booking page after logging in."""
    def _navigate():
        WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Book Places')))
        browser.find_element(By.LINK_TEXT, 'Book Places').click()
    return _navigate

@pytest.fixture
def submit_booking_request(browser):
    """
    Provides a function to submit a booking request for a specified number of places.
    """
    def _submit(places):
        WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.NAME, 'places')))
        place_input = browser.find_element(By.NAME, 'places')
        place_input.clear()
        place_input.send_keys(str(places))
        place_input.send_keys(Keys.RETURN)
    return _submit

@pytest.fixture
def login(browser):
    """
    This fixture simplifies the process of logging into the site by navigating to the home page,
    waiting for the email input to be present, entering the provided email, and submitting the form.
    """
    def do_login(email):
        browser.get('http://127.0.0.1:5000')
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.NAME, 'email')))
        email_input = browser.find_element(By.NAME, 'email')
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
    return do_login