from django.contrib import admin
from .models import Facility, Experiment, FacilityUser

# Register your models here.

admin.site.register(Facility)
admin.site.register(Experiment)
admin.site.register(FacilityUser)