from locust import HttpUser, task, between
import random


class UserBehaviorSimulation(HttpUser):
    """
    This class simulates user behavior for both loading and updating actions, ensuring realistic user flow and interaction.
    """
    wait_time = between(1, 3)
    host = "http://127.0.0.1:5000"
    user_data = [
        {"email": "john@simplylift.co", "club": "Simply Lift"},
        {"email": "admin@irontemple.com", "club": "Iron Temple"},
        {"email": "kate@shelifts.co.uk", "club": "She Lifts"},
        {"email": "jane@powerlifters.com", "club": "Power Lifters"},
        {"email": "max@maxmuscle.com", "club": "Max Muscle"},
        {"email": "league@lifleague.com", "club": "Lift League"}
    ]
    competitions = ["Spring Festival", "Fall Classic", "Avail Festival"]

    def on_start(self):
        """
        Simulates initial visit to the index page which displays a points table of all clubs, and used for user authentication.
        """
        self.client.get("/")
        self.user = random.choice(self.user_data)
        self.selected_competition = random.choice(self.competitions)

    @task(4)
    def show_summary(self):
        """
        Retrieves and displays a dynamic summary table of all competitions and the points tally of the logged-in club. 
        This view is shown immediately after a user logs in at the index page, providing a real-time update of available competitions and the club's current points.
        """
        self.client.post("/showSummary", data={"email": self.user['email']})

    @task(2)
    def display_competition(self):
        """
        Simulates viewing the booking page by accessing the specific competition details.
        This page displays available slots and allows users to decide on the number of places to book for a particular competition.
        """
        self.client.get(f"/book/{self.selected_competition}/{self.user['club']}")

    @task(1)
    def purchase_places(self):
        """
        Simulates booking places for a competition.
        This action is critical as it involves updating the database and is sensitive to performance issues.
        """
        places = random.randint(1, 2)
        self.client.post("/purchasePlaces", 
                         data={"club": self.user['club'], 
                               "competition": self.selected_competition, 
                               "places": str(places)})

    @task(1)
    def logout(self):
        """
        Simulates a user logging out of the system.
        """
        self.client.get("/logout")
