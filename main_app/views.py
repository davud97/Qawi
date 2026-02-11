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


# check if user is trainer
def is_trainer(user):
    profile = get_profile(user)
    return profile is not None and profile.role == "trainer"


# check if user is member
def is_member(user):
    profile = get_profile(user)
    return profile is not None and profile.role == "member"

# home page show classes, mark enrolled if member
def home(request):
    classes = GymClass.objects.all()

    membership = None
    if request.user.is_authenticated:
        membership = Membership.objects.filter(user=request.user).order_by("-id").first()

    enrolled_class_ids = []
    profile = get_profile(request.user)
    if profile and profile.role == "member":
        enrolled_class_ids = list(
            Enrollment.objects.filter(member=request.user).values_list("gym_class_id", flat=True)
        )

    return render(
        request,
        "home.html",
        {"classes": classes, "enrolled_class_ids": enrolled_class_ids, "membership": membership},
    )



# show class detail and workouts
def class_detail(request, class_id):
    cls = get_object_or_404(GymClass, id=class_id)
    workout_plans = cls.workout_plans.all()
    return render(request, "class_detail.html", {"class": cls, "workout_plans": workout_plans})


# show workout and exercises
def workout_detail(request, workout_id):
    workout = get_object_or_404(WorkoutPlan, id=workout_id)
    exercises = workout.exercises.all()
    return render(request, "workout_detail.html", {"workout": workout, "exercises": exercises})


# signup page
def signup(request):
    error_message = ""

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )


            user.signup_role = form.cleaned_data["role"]
            user.save()

            login(request, user)
            messages.success(request, f"Welcome {user.username}! Account created")
            return redirect("home")

        error_message = "Signup info invalid, try again"
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form, "error_message": error_message})
