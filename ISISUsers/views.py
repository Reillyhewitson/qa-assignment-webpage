from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Facility, Experiment, FacilityUser
from .forms import CreateExperimentForm, EditFacilityForm
import datetime

def index(request):
    return render(request, "home/index.html")

@login_required(login_url="accounts/login/")
def user(request):
    facilityId = FacilityUser.objects.filter(user=request.user).first()
    facility = Facility.objects.get(pk=facilityId.facility.pk)
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("form_type") == "experiment":
            form = CreateExperimentForm(request.POST, request.FILES)
            form.save()
        if request.POST.get("form_type") == "facility":
            form = EditFacilityForm(request.POST, request.FILES, instance=facility)
            form.save()
    experiments = Experiment.objects.filter(scientist=request.user, end_date__gte=datetime.date.today()).order_by("start_date")
    facility_form = EditFacilityForm(instance=facility)
    context = {"username": request.user, "experiments": experiments, "experiment_form": CreateExperimentForm, "facility_form": facility_form}
    return render(request, "users/index.html", context)

def logout_view(request):
    logout(request)
    return redirect('home', permanent=True)