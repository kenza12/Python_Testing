import os
import sys
from datetime import datetime

# Set the path to include the root directory for easy imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from server import app as flask_app
from flask_testing import LiveServerTestCase
from selenium import webdriver

# Test Server
BASE_URL = 'http://127.0.0.1:8943/'

class CustomLiveServerTestCase(LiveServerTestCase):
    """A customized live server test case class for handling integration tests with Selenium."""
    def create_app(self):
        """Set up application configuration specifically for testing."""
        flask_app.config.update({
            'TESTING': True,
            'LIVESERVER_PORT': 8943,
            'FLASK_ENV': 'testing',
            'SECRET_KEY': 'verysecret',
            'SERVER_NAME': 'localhost.localdomain:8943',
            'CLUBS_DATA_PATH': 'tests/data/test_clubs.json',
            'COMPETITIONS_DATA_PATH': 'tests/data/test_competitions.json'
        })
        return flask_app

    def setUp(self):
        """Initialize the WebDriver before each test."""
        self.driver = webdriver.Firefox()

    def tearDown(self):
        """Close the WebDriver after each test."""
        self.driver.quit()


@pytest.fixture(scope='function')
def app():
    """Fixture to configure the Flask application for tests without starting the server."""
    return CustomLiveServerTestCase().create_app()

@pytest.fixture(scope='function')
def client(app):
    """Provide a test client for the application configured for testing."""
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
def mock_iron_temple(mocker):
    """Prepare and inject mocked club (Iron Temple) and competition data (Spring Festival)"""
    mocked_clubs = [{'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': 4}]
    mocker.patch('server.clubs', new=mocked_clubs)

    mocked_competitions = [{'name': 'Spring Festival', 'numberOfPlaces': 5}]
    mocker.patch('server.competitions', new=mocked_competitions)

@pytest.fixture
def mock_simply_lift(mocker):
    """Prepare and inject mocked club (Simply Lift) and competition data (Fall Classic)"""
    mocked_clubs = [{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': 24}]
    mocker.patch('server.clubs', new=mocked_clubs)

    mocked_competitions = [{'name': 'Fall Classic', 'numberOfPlaces': 30}]
    mocker.patch('server.competitions', new=mocked_competitions)

@pytest.fixture
def mock_iron_temple_with_past_competition(mocker):
    """Prepare and inject mocked club (Iron Temple) and competition data with a past competition."""
    mocked_clubs = [{'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': 4}]
    mocker.patch('server.clubs', new=mocked_clubs)

    past_date = datetime(2020, 5, 15, 10, 0, 0)
    mocked_competitions = [
        {'name': 'Spring Festival', 'numberOfPlaces': 5, 'date': '2026-03-27 10:00:00'},
        {'name': 'Historic Match', 'numberOfPlaces': 10, 'date': past_date.strftime('%Y-%m-%d %H:%M:%S')}
    ]
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
        browser.get(BASE_URL)
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.NAME, 'email')))
        email_input = browser.find_element(By.NAME, 'email')
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
    return do_login