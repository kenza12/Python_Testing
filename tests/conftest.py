import os
import sys

# Set the path to include the root directory for easy imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app as flask_app

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