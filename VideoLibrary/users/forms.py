from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'profile_picture', 'password']

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Override username field with email
