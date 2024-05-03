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

Each test type targets different aspects of the application:

- **Unit tests** focus on the smallest parts of code, like functions and methods.
- **Integration tests** verify that different modules or services used by your application interact well.
- **Functional tests** assess the system as a whole, simulating user behavior to see if functionalities meet the specified requirements.
- **Coverage tests** evaluate the percentage of the project's codebase that is executed when the tests run, helping identify untested parts of the application. It ensures that all functional aspects are covered by tests, enhancing confidence in the software's reliability.
- **Performance tests** simulate user behavior at scale to assess the application's responsiveness and stability under load. These tests are crucial for identifying bottlenecks and ensuring that the application can handle expected traffic volumes.

**Note:** Since the project includes functional tests with Selenium, it's important to restart the Flask server before running tests. This reset ensures that the application state is fresh, avoiding issues where tests might fail due to depleted resources like club points or competition places from previous test runs. This is crucial for ensuring that Selenium functional tests run correctly under a consistent starting state.

### Installation and Configuration

Before running the tests, create and activate the virtual environment, then install the dependencies:

```bash
virtualenv .
source bin/activate
pip install -r requirements.txt
```

To ensure that both the tests and the local Flask server function correctly, set the **FLASK_APP** environment variable to point to the main Flask application file.

```bash
# On Linux/MacOS:
export FLASK_APP=server.py

#On Windows:
set FLASK_APP=server.py
```

### Running Unit, Integration, and Functional Tests

Set the testing environment by configuring the **FLASK_ENV** variable to `testing`:

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

### Running Coverage Tests

To check code coverage of your tests, ensure the testing environment variable **FLASK_ENV** is set to `testing` and start the Flask server using `flask run --port 8943`.

To generate the coverage report, execute the following command from the root directory of the project:

```bash
pytest --cov=server --cov-report=html
```

This will run all the tests and generate a coverage report in HTML format. You can find the coverage report in `tests/coverage/htmlcov directory`. Open the `index.html` file within this directory in your web browser to view the detailed coverage report.

### Running Performance Tests with Locust

Before running performance tests, set the environment to `performance`  to ensure the application uses the correct configuration for using test data where the number of places and points are significantly increased to simulate realistic load scenarios:

```bash
# On Linux/MacOS:
export FLASK_ENV=performance
# On Windows:
set FLASK_ENV=performance
```

Ensure that your Flask application is running because Locust needs a live server to send requests to. You can start your Flask application using the following command:

```bash
flask run
```

Once the Flask server is active, you can proceed to run the Locust tests. Use the provided bash script to automate the testing process. This script ensures that performance data integrity is maintained by backing up and restoring data before and after the tests:

```bash
# from root directory
bash tests/performance/locust.sh 
```

This script performs the following operations:

- Backs up the current performance data.
- Runs Locust in headless mode, which does not require the Locust web interface.
- Generates a performance report in HTML format.
- Restores the original data after testing to ensure subsequent tests start with a consistent dataset.

Locust Command Options:

- `-f tests/performance/locust.py`: Specifies the file containing the Locust tasks.
- `--headless`: Runs Locust without its web interface.
- `-u 6`: Sets the number of simulated users to 6.
- `-r 1`: Specifies a hatch rate of 1 user per second.
- `--run-time 60s`: Limits the test duration to 60 seconds.
- `--html=tests/performance/performance_report.html`: Generates an HTML report named performance_report.html.

In the performance tests, clubs and competitions are selected randomly. This approach helps to simulate a variety of user interactions with the system, reflecting a more realistic usage pattern where different users may choose different clubs or competitions.

After running the performance tests, check the `performance_report.html` file in `tests/performance/` directory for a detailed report. This report includes statistics such as the number of requests, median response times, number of failures, and other relevant metrics that help in evaluating the application's performance under stress.
