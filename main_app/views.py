from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import GymClass, WorkoutPlan, Exercise, Membership, MembershipPackage, Enrollment
from .forms import SignUpForm, GymClassForm, WorkoutPlanForm, ExerciseForm, ChooseMembershipForm


# landing page, if user login go home, else login page
def landing(request):
    return redirect("home") if request.user.is_authenticated else redirect("login")


# helper that safely get profile without try/except
def get_profile(user):
    return getattr(user, "profile", None) if user.is_authenticated else None
