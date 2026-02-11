from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    #role chocie of if the user is trainer or member
    ROLE_CHOICES = (
        ('trainer', 'Trainer'),
        ('member', 'Member'),
    )


# here is the status choice of if the member is active or not
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class GymClass(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # trainer
    available_slots = models.IntegerField()

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    name = models.CharField(max_length=100)
    gym_class = models.ForeignKey(
        GymClass,
        on_delete=models.CASCADE,
        related_name='workout_plans'
    )

    def __str__(self):
        return self.name



    