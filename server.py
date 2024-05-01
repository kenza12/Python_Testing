from flask import current_app, Flask, render_template, request, redirect, flash, url_for, make_response
import json
from datetime import datetime
import os


def loadClubs():
    """Load club data from the JSON file"""
    with open(current_app.config['CLUBS_DATA_PATH']) as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

def loadCompetitions():
    """Load competition data from the JSON file"""
    with open(current_app.config['COMPETITIONS_DATA_PATH']) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

def save_data(clubs, competitions):
    """Save updated clubs and competitions data to their respective JSON files."""
    with open(current_app.config['CLUBS_DATA_PATH'], 'w') as c:
        json.dump({'clubs': clubs}, c, indent=4)
    
    with open(current_app.config['COMPETITIONS_DATA_PATH'], 'w') as c:
        json.dump({'competitions': competitions}, c, indent=4)

app = Flask(__name__)
app.secret_key = 'something_special'
app.debug = True

# Set paths for data files based on the environment
if os.getenv('FLASK_ENV') == 'testing':
    app.config['CLUBS_DATA_PATH'] = 'tests/data/test_clubs.json'
    app.config['COMPETITIONS_DATA_PATH'] = 'tests/data/test_competitions.json'
else:
    app.config['CLUBS_DATA_PATH'] = 'clubs.json'
    app.config['COMPETITIONS_DATA_PATH'] = 'competitions.json'

with app.app_context():
    competitions = loadCompetitions()
    clubs = loadClubs()

@app.route('/')
def index():
    """Render the main page with the club points table."""
    clubs = loadClubs()
    return render_template('index.html', clubs=clubs)

@app.route('/showSummary',methods=['POST'])
def showSummary():
    """Show a summary for the selected club, if it exists."""
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        return make_response(render_template('index.html', clubs=clubs, error="Sorry, that email was not found."), 400)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    """Render booking page if both club and competition are found."""
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    """Handle place purchase requests, enforcing limits on the number of places and club points."""
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    placesRequired = int(request.form['places'])
    club_points = int(club['points'])
    competition_places = int(competition['numberOfPlaces'])

    # Cannot book places for past competitions
    if 'date' in competition:
        competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        if competition_date < datetime.now():
            return make_response(render_template('booking.html', club=club, competition=competition, error='Cannot book places for past competitions'), 400)

    # Cannot book more places than available
    if placesRequired > competition_places:
        error_message = "Cannot book more places than are available."
        return make_response(render_template('booking.html', club=club, competition=competition, error=error_message), 400)

    # Cannot book more than 12 places
    if placesRequired > 12:
        response = make_response(render_template('booking.html', club=club, competition=competition, error='Cannot book more than 12 places per competition'), 400)
        return response

    # Cannot use more than points allowed
    if placesRequired > club_points:
        response = make_response(render_template('booking.html', club=club, competition=competition, error='Not enough points'), 400)
        return response

    # All checks passed, proceed with booking
    competition['numberOfPlaces'] = competition_places - placesRequired
    club['points'] = str(club_points - placesRequired)

    # Save updates
    save_data(clubs, competitions)
    
    flash('Great-booking complete!')
    
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/logout')
def logout():
    """Handle user logout and redirect to the main page."""
    return redirect(url_for('index'))