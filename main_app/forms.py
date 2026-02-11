from django import forms
from .models import GymClass, WorkoutPlan, Exercise, MembershipPlan, MembershipPackage


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Username",
        # tis make pasword box hide letters n show "Enter password" inside, not just normal text
        widget=forms.TextInput(attrs={"placeholder": "Enter username"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Enter email"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}),
    )
    role = forms.ChoiceField(
        choices=[("trainer", "Trainer"), ("member", "Member")],
        label="Role",
    )


class GymClassForm(forms.ModelForm):
    class Meta:
        model = GymClass
        fields = ["name", "available_slots"]


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ["name"]


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["workout_name"]






# NEW MEMBERSHIP FORM
class ChooseMembershipForm(forms.Form):
    package = forms.ModelChoiceField(
        queryset=MembershipPackage.objects.none(),
        # I use RadioSelect here for show all packages like circle button and easy for member to slelct easyliy
        widget=forms.RadioSelect,
        empty_label=None,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["package"].queryset = MembershipPackage.objects.all()
