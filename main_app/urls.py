from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Landing page is login if not authenticated
    path('', views.landing, name='landing'),

    # Home page (after login)
    path('home/', views.home, name='home'),

    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),


    # Classes & Workouts
    path('classes/<int:class_id>/', views.class_detail, name='class_detail'),
    path('workouts/<int:workout_id>/', views.workout_detail, name='workout_detail'),
    path('classes/create/', views.create_class, name='create_class'),
    path('classes/<int:class_id>/add_workout/', views.add_workout_plan, name='add_workout_plan'),
    path('workouts/<int:workout_id>/add_exercise/', views.add_exercise, name='add_exercise'),
    # Profile & Membership
    path('profile/', views.profile, name='profile'),
    path('membership/', views.choose_membership, name='choose_membership'),

        # Edit & Delete
    path('classes/<int:class_id>/edit/', views.edit_class, name='edit_class'),
    path('classes/<int:class_id>/delete/', views.delete_class, name='delete_class'),
    path('workouts/<int:workout_id>/edit/', views.edit_workout_plan, name='edit_workout_plan'),
    path('workouts/<int:workout_id>/delete/', views.delete_workout_plan, name='delete_workout_plan'),
    path('exercises/<int:exercise_id>/edit/', views.edit_exercise, name='edit_exercise'),
    path('exercises/<int:exercise_id>/delete/', views.delete_exercise, name='delete_exercise'),
    path("membership/", views.choose_membership, name="choose_membership"),
    path('classes/<int:class_id>/enroll/', views.enroll_class, name='enroll_class'),
    path('classes/<int:class_id>/unenroll/', views.unenroll_class, name='unenroll_class'),



]
