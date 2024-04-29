# gudlift-registration

## 1. Why

This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

## 2. Getting Started

This project uses the following technologies:

- **Python v3.x+**
- **[Flask](https://flask.palletsprojects.com/en/1.1.x/)**
  - Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need.
- **[Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)**
  - This ensures you'll be able to install the correct packages without interfering with Python on your machine.
  - Before you begin, please ensure you have this installed globally.

## 3. Installation

- After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.
- Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>
- Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>
- Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details
- You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

## 4. Current Setup

The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:

- **competitions.json** - list of competitions
- **clubs.json** - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

## 5. Testing

The GudLift registration project includes several types of automated tests to ensure the application functions as expected.

Each test type targets different layers of the application:

- **Unit tests** focus on the smallest parts of code, like functions and methods.
- **Integration tests** verify that different modules or services used by your application interact well.
- **Functional tests** assess the system as a whole, simulating user behavior to see if functionalities meet the specified requirements.

Before running the tests, create, activate the virtual environment and install the dependencies:

```bash
virtualenv .
source bin/activate
pip install -r requirements.txt
```

To ensure that both the tests and the local Flask server function correctly, you need to set the **FLASK_APP** environment variable to point to the main Flask application file.

```bash
# On Linux/MacOS:
export FLASK_APP=server.py

#On Windows:
set FLASK_APP=server.py
```

Also, set the testing environment by configuring the **FLASK_ENV** variable to `testing`:

```bash
# On Linux/MacOS:
export FLASK_ENV=testing

# On Windows:
set FLASK_ENV=testing
```

After setting up the environment, ensure the Flask application is running locally. Start the test server in a separate terminal using `flask run --port 8943`.

Then, run the following command from the root directory of the project:

```bash
pytest -sv tests/
```

**Note:** For functional tests involving Selenium, download the [GeckoDriver](https://github.com/mozilla/geckodriver/releases) that matches your browser's version and operating system. Place the downloaded geckodriver executable in the `tests/functional` directory. This is required for Selenium to interact with Firefox or other browser during tests.