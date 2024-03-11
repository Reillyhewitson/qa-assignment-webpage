from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import BaseUserCreationForm, AuthenticationForm;
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Facility, Experiment, FacilityUser
from .forms import CreateExperimentForm, EditFacilityForm, CustomUserForm
import datetime

def index(request):
    context = {"username": request.user}
    return render(request, "home/index.html", context)

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

def login_view(request):
    
    if request.POST.get('form_type') == "user":
        customUserForm = CustomUserForm(request.POST)
        if customUserForm.is_valid():
            customUserForm.save()
            return redirect("createFacility")
        authenticationForm = AuthenticationForm()
    elif request.POST.get('form_type') == "login":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("user")
        authenticationForm = AuthenticationForm()
        customUserForm = CustomUserForm()
    else:
        authenticationForm = AuthenticationForm()
        customUserForm = CustomUserForm()
    context = {"form": authenticationForm, "createForm": customUserForm}
    return render(request, "registration/login.html", context)

def create_view(request):
    if request.method == "GET":
        return redirect('user')
    
def create_facility(request):
    if request.method == "POST":
        form = EditFacilityForm(request.POST)
        if form.is_valid():
            facility_obj = form.save()
            FacilityUser.objects.create(
                facility = Facility.objects.get(pk=facility_obj.pk), 
                user = User.objects.get(pk=request.user.pk)
            )
            return redirect("user")
    else:
        form = EditFacilityForm()
    context = {"facility_form": form}
    return render(request, "registration/facility.html", context)
