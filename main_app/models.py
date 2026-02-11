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


class Exercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='exercises')
    workout_name = models.CharField(max_length=100)

    def __str__(self):
        return self.workout_name


# NEW MEMBERSHIP SYSTEM
class MembershipPackage(models.Model):
    name = models.CharField(max_length=50, unique=True)
    duration_months = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField()
    classes_per_week = models.IntegerField()
    personal_trainer = models.BooleanField(default=False)
    full_equipment_access = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    package = models.ForeignKey(MembershipPackage, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.package.name}"


class Enrollment(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'gym_class')

    def __str__(self):
        return f"{self.member.username} → {self.gym_class.name}"


# OLD MEMBERSHIP PLAN - KEEP FOR NOW (you can delete after migration)
class MembershipPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in months")
    price = models.IntegerField(help_text="Price in BHD")

    def __str__(self):
        return f"{self.name} ({self.user.username})"


# SIGNALS
# SIGNALS
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Default role 'member'
        Profile.objects.create(
            user=instance,
            role=getattr(instance, 'signup_role', 'member'),
            status='active' if getattr(instance, 'signup_role', 'member') == 'member' else None
        )

