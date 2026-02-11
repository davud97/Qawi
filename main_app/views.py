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

# create class only trainer
@login_required
@user_passes_test(is_trainer)
def create_class(request):
    if request.method == "POST":
        form = GymClassForm(request.POST)
        if form.is_valid():
            gym_class = form.save(commit=False)
            gym_class.user = request.user
            gym_class.save()
            messages.success(request, f'Class "{gym_class.name}" created')
            return redirect("home")
    else:
        form = GymClassForm()

    return render(request, "create_class.html", {"form": form})

# add workout plan trainer only
@login_required
@user_passes_test(is_trainer)
def add_workout_plan(request, class_id):
    gym_class = get_object_or_404(GymClass, id=class_id)

    if request.method == "POST":
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            workout_plan = form.save(commit=False)
            workout_plan.gym_class = gym_class
            workout_plan.save()
            messages.success(request, f'Workout plan "{workout_plan.name}" added')
            return redirect("class_detail", class_id=gym_class.id)
    else:
        form = WorkoutPlanForm()

    return render(request, "add_workout_plan.html", {"form": form, "gym_class": gym_class})


# add exercise trainer only
@login_required
@user_passes_test(is_trainer)
def add_exercise(request, workout_id):
    workout = get_object_or_404(WorkoutPlan, id=workout_id)

    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.workout_plan = workout
            exercise.save()
            messages.success(request, f'Exercise "{exercise.workout_name}" added')
            return redirect("workout_detail", workout_id=workout.id)
    else:
        form = ExerciseForm()

    return render(request, "add_exercise.html", {"form": form, "workout": workout})

# choose membership only member can because trainer are not for memebrshiip


@login_required
@user_passes_test(is_member)
def choose_membership(request):
    existing = Membership.objects.filter(user=request.user).first()
    if existing:
        messages.error(request, "Membership already submitted")
        return redirect("profile")

    if request.method == "POST":
        form = ChooseMembershipForm(request.POST)
        if form.is_valid():
            package = form.cleaned_data["package"]
            Membership.objects.create(user=request.user, package=package, status="pending")
            messages.success(
                request,
                "Your membership request has been submitted successfully. Our team will contact you shortly.",
            )
            return redirect("profile")
    else:
        form = ChooseMembershipForm()

    packages = MembershipPackage.objects.all()
    return render(request, "choose_membership.html", {"packages": packages, "form": form})


# profile page
@login_required
def profile(request):
    user = request.user
    profile_obj = get_profile(user)

    membership = None
    enrolled_classes = []
    my_classes = []
    total_classes = total_workout_plans = total_exercises = 0

    if profile_obj and profile_obj.role == "member":
        membership = Membership.objects.filter(user=user).order_by("-id").first()
        enrolled_classes = Enrollment.objects.filter(member=user).select_related("gym_class")

    if profile_obj and profile_obj.role == "trainer":
        my_classes = GymClass.objects.filter(user=user).prefetch_related("workout_plans__exercises")
        total_classes = my_classes.count()
        total_workout_plans = sum(c.workout_plans.count() for c in my_classes)
        total_exercises = sum(
            wp.exercises.count()
            for c in my_classes
            for wp in c.workout_plans.all()
        )

    return render(
        request,
        "profile.html",
        {
            "profile": profile_obj,
            "membership": membership,
            "enrolled_classes": enrolled_classes,
            "my_classes": my_classes,
            "total_classes": total_classes,
            "total_workout_plans": total_workout_plans,
            "total_exercises": total_exercises,
        },
    )

# enroll class member only when they want to enroll but membership is must
@login_required
@user_passes_test(is_member)
def enroll_class(request, class_id):
    gym_class = get_object_or_404(GymClass, id=class_id)

    membership = Membership.objects.filter(user=request.user).order_by("-id").first()
    if not membership or membership.status != "approved":
        messages.error(request, "Need approved membership")
        return redirect("home")

    if Enrollment.objects.filter(member=request.user, gym_class=gym_class).exists():
        messages.warning(request, "Already enrolled")
        return redirect("home")

    Enrollment.objects.create(member=request.user, gym_class=gym_class)
    messages.success(request, "Enrolled successfully")
    return redirect("home")

# unenroll class member only
@login_required
@user_passes_test(is_member)
def unenroll_class(request, class_id):
    gym_class = get_object_or_404(GymClass, id=class_id)

    Enrollment.objects.filter(member=request.user, gym_class=gym_class).delete()
    messages.success(request, f'Unenrolled from "{gym_class.name}"')
    return redirect("home")

#crud below

# edit class trainer only
@login_required
@user_passes_test(is_trainer)
def edit_class(request, class_id):
    gym_class = get_object_or_404(GymClass, id=class_id)

    if request.method == "POST":
        form = GymClassForm(request.POST, instance=gym_class)
        if form.is_valid():
            form.save()
            messages.success(request, f'Class "{gym_class.name}" updated')
            return redirect("class_detail", class_id=gym_class.id)
    else:
        form = GymClassForm(instance=gym_class)

    return render(request, "create_class.html", {"form": form, "edit": True})

# delete class trainer only
@login_required
@user_passes_test(is_trainer)
def delete_class(request, class_id):
    gym_class = get_object_or_404(GymClass, id=class_id)
    gym_class.delete()
    messages.success(request, "Class deleted")
    return redirect("home")


# edit workout plan trainer only
@login_required
@user_passes_test(is_trainer)
def edit_workout_plan(request, workout_id):
    workout = get_object_or_404(WorkoutPlan, id=workout_id)

    if request.method == "POST":
        form = WorkoutPlanForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, f'Workout plan "{workout.name}" updated')
            return redirect("class_detail", class_id=workout.gym_class.id)
    else:
        form = WorkoutPlanForm(instance=workout)

    return render(
        request,
        "add_workout_plan.html",
        {"form": form, "gym_class": workout.gym_class, "edit": True},
    )

