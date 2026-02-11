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
]
