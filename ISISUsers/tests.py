from django.test import TestCase, Client
from .models import *
from .forms import *
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

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
        self.assertEqual(experiment.created_by.id, self.user_alt.id)
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

class NotLoggedInTest(TestCase):
    fixtures = ["data.json"]
    client = Client()

    def test_user_access_not_logged_in(self):
        response = self.client.get(reverse('user'))
        self.assertEqual(response.status_code, 302)

class ExperimentFormTest(TestCase):
    fixtures = ["data.json"]
    client = Client()
    user = None
    
    def setUp(self):
        self.user = User.objects.get(
            username="test"
        )
        self.client.force_login(self.user)

    def test_user_access_logged_in(self):
        response = self.client.get(reverse('user'))
        self.assertEqual(response.status_code, 200)

    def test_create_new_experiment(self):
        experiment = {"name": "test_test",
                      "description": "test",
                      "start_date": "10/12/2024",
                      "end_date": "11/12/2024",
                      "created_by": "2",
                      "scientist": "2",
                      "form_type": "experiment"
                      }
        response = self.client.post(reverse('user'), experiment)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(Experiment.objects.get(name="test_test"), Experiment)

    def test_create_new_experiment_start_before_end(self):
        experiment = {"name": "test_test",
                      "description": "test",
                      "start_date": "11/12/2024",
                      "end_date": "10/12/2024",
                      "created_by": "2",
                      "scientist": "2"
                      }
        form = CreateExperimentForm(experiment)
        with self.assertRaises(ValidationError):
            form.save()