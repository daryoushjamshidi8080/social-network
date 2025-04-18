from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your username'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Your Email..'}))
    password = forms.CharField(
        label='password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your password ..'}))

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your Confirm password ..'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()

        if user:
            raise ValidationError('This email already exists')

        return email

    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).exists()

        if user:
            raise ValidationError('This username already exists')

        return username

    def clean(self):
        cd = super().clean()

        password = cd.get('password')
        confirm_password = cd.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Password must match')
