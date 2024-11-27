from django.test import TestCase
from .models import *

# Create your tests here.

class ExperimentsTestCaseDifferentUser(TestCase):
    user = None
    user_alt = None
    def setUp(self):
        self.user = User.objects.create(
            name="test_user"
        )
        self.user_alt = User.objects.create(
            name="alt_test_user"
        )
        Experiment.objects.create(
            name="New test Experiment",
            scientist=self.user.id,
            created_by=self.user_alt.id,
        )
    
    def test_experiment_has_user(self):
        """User has been correctly defined"""
        experiment = Experiment.objects.get(name="New test Experiment")
        self.assertEqual(experiment.created_by, self.user_alt.id)
        self.assertEqual(experiment.scientist, self.user.id)