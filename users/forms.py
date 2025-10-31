from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(label="Full Name",)
    agree_to_term = forms.BooleanField(label="Agreed to Term")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'agree_to_term')


    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match("^[A-Za-z ]+$", full_name):
            raise forms.ValidationError("Full name must contain only letters, numbers, dots and dashes")
        return full_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match("^[A-Za-z ]+$", username):
            raise forms.ValidationError("Username must contain only letters, numbers, dots and dashes")
        return username