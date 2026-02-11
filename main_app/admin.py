from django.contrib import admin
from .models import Profile, GymClass, WorkoutPlan, Exercise, MembershipPlan, Membership

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'status')
    list_filter = ('role', 'status')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'status')
    list_filter = ('status',)

admin.site.register(GymClass)
admin.site.register(WorkoutPlan)
admin.site.register(Exercise)
admin.site.register(MembershipPlan)
