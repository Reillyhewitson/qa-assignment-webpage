from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Facility(models.Model):
    """Model representing the facility the User works at"""
    name = models.CharField(
        max_length=200,
        help_text="Enter the name of the Facility you work at."
    )
    street = models.CharField(max_length=1000)
    town = models.CharField(max_length=1000)
    postcode = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)

class Experiment(models.Model):
    name = models.CharField(
        max_length=200,
        help_text = "Enter the name of the experiment you want to perform"
    )
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    scientist = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)

class FacilityUser(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    facility = models.OneToOneField(Facility, on_delete = models.CASCADE)


# facility = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False)