from django import forms
from django.core import validators
from django.forms import ModelForm
from .models import Experiment, Facility
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class CreateExperimentForm(forms.Form):
#     experiment_name = forms.CharField(label="Experiment name", max_length=200)
#     experiment_description = forms.CharField(max_length="10000")
#     experiment_start_date = forms.DateField()
#     experiment_end_date = forms.DateField()

#     def clean(self):
#         super().clean()

#         end_date = self.cleaned_data.get('experiment_end_date')
#         start_date = self.cleaned_data.get('experiment.start_date')

#         if start_date > end_date:
#             raise ValidationError(
#                 "Experiment cannot end before it begins."
#             )

class CreateExperimentForm(ModelForm):
    class Meta:
        model = Experiment
        fields = ["name", "description", "start_date", "end_date", "scientist"]

class EditFacilityForm(ModelForm):
    class Meta:
        model = Facility
        fields = ["name", "street", "town", "country", "postcode"]

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']