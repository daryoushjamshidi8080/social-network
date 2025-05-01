from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


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


class UserLoginForm(forms.Form):

    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class EditeUserForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        required=False, widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('age', 'bio')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        comfirm_password = cleaned_data.get('confirm_password')

        if comfirm_password != password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
