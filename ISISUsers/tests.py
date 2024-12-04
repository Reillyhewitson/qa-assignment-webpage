from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your tests here.

class ExperimentsTestCaseDifferentUser(TestCase):
    fixtures = ["data.json"]
    user = None
    user_alt = None
    def setUp(self):
        self.user = User.objects.get(
            username="test"
        )
        self.user_alt = User.objects.get(username="test2")
        Experiment.objects.create(
            name="New test Experiment",
            scientist=self.user,
            created_by=self.user_alt,
            description = "test",
            start_date = datetime.now() - timedelta(weeks=2),
            end_date = datetime.now()
        )
    
    def test_experiment_has_user(self):
        """User has been correctly defined"""
        experiment = Experiment.objects.get(name="New test Experiment")
        self.assertEqual(experiment.created_by.id, self.user.id)
        self.assertEqual(experiment.scientist.id, self.user.id)

class ExperimentsTestCaseSameUser(TestCase):
    fixtures = ["data.json"]
    user = None
    def setUp(self):
        self.user = User.objects.get(
            username="test"
        )
        Experiment.objects.create(
            name="New test Experiment",
            scientist=self.user,
            created_by=self.user,
            description = "test",
            start_date = datetime.now() - timedelta(weeks=2),
            end_date = datetime.now()
        )
    
    def test_experiment_has_user(self):
        """User has been correctly defined"""
        experiment = Experiment.objects.get(name="New test Experiment")
        self.assertEqual(experiment.created_by.id, self.user.id)
        self.assertEqual(experiment.scientist.id, self.user.id)

# class ExperimentFormTest