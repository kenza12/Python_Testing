from flask import current_app, Flask, render_template, request, redirect, flash, url_for
import json

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

app = Flask(__name__)
app.secret_key = 'something_special'
app.debug = True

# Default paths for data files
app.config['CLUBS_DATA_PATH'] = 'clubs.json'
app.config['COMPETITIONS_DATA_PATH'] = 'competitions.json'

with app.app_context():
    competitions = loadCompetitions()
    clubs = loadClubs()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    """Show a summary for the selected club, if it exists."""
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    """Render booking page if both club and competition are found."""
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
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

    # Cannot book more than 12 places
    if placesRequired > 12:
        flash('Cannot book more than 12 places per competition', 'error')
        return render_template('welcome.html', club=club, competitions=competitions)

    # Cannot use more than points allowed
    if placesRequired > club_points:
        flash('Not enough points', 'error')
        return render_template('welcome.html', club=club, competitions=competitions)

    competition['numberOfPlaces'] = competition_places - placesRequired
    club['points'] = str(club_points - placesRequired)
    flash('Great-booking complete!')
    
    return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display

@app.route('/logout')
def logout():
    """Handle user logout and redirect to the main page."""
    return redirect(url_for('index'))