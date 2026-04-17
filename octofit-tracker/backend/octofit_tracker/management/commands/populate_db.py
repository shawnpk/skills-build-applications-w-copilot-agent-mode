
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        # Delete in order to avoid orphaned references

        # Drop collections directly with PyMongo to avoid Djongo delete errors
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.activity.drop()
        db.leaderboard.drop()
        db.workout.drop()
        db.user.drop()
        db.team.drop()

        # Create Teams
        marvel = Team.objects.create(name='marvel', description='Marvel Team')
        dc = Team.objects.create(name='dc', description='DC Team')

        # Create Users

        users = []
        users.append(User.objects.create(email='ironman@marvel.com', name='Iron Man', team='marvel', is_superhero=True))
        users.append(User.objects.create(email='captain@marvel.com', name='Captain America', team='marvel', is_superhero=True))
        users.append(User.objects.create(email='batman@dc.com', name='Batman', team='dc', is_superhero=True))
        users.append(User.objects.create(email='superman@dc.com', name='Superman', team='dc', is_superhero=True))

        # Create Activities
        Activity.objects.create(user=users[0], type='run', duration=30, date=timezone.now())
        Activity.objects.create(user=users[1], type='cycle', duration=45, date=timezone.now())
        Activity.objects.create(user=users[2], type='swim', duration=25, date=timezone.now())
        Activity.objects.create(user=users[3], type='yoga', duration=60, date=timezone.now())

        # Create Workouts
        Workout.objects.create(name='Pushups', description='Do 3 sets of 15 pushups', suggested_for='marvel')
        Workout.objects.create(name='Situps', description='Do 3 sets of 20 situps', suggested_for='dc')

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
