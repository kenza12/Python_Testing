#!/bin/bash

# Location of the performance data files
PERFORMANCE_CLUBS_PATH="./tests/data/test_perf_clubs.json"
PERFORMANCE_COMPETITIONS_PATH="./tests/data/test_perf_competitions.json"

# Backup the current data
echo "Backing up performance data..."
cp $PERFORMANCE_CLUBS_PATH "${PERFORMANCE_CLUBS_PATH}.bak"
cp $PERFORMANCE_COMPETITIONS_PATH "${PERFORMANCE_COMPETITIONS_PATH}.bak"

# Function to restore data
restore_data() {
    echo "Restoring original data..."
    mv "${PERFORMANCE_CLUBS_PATH}.bak" $PERFORMANCE_CLUBS_PATH
    mv "${PERFORMANCE_COMPETITIONS_PATH}.bak" $PERFORMANCE_COMPETITIONS_PATH
    echo "Data restored."
}

# Ensure data is restored even if the script exits prematurely
trap restore_data EXIT

echo "Starting performance tests with Locust..."
# Execute the performance tests with Locust in headless mode
locust -f ./tests/performance/locust.py --headless -u 6 -r 1 --run-time 60s --html=./tests/performance/performance_report.html

echo "Performance tests completed. Check the 'performance_report.html' for the report."
