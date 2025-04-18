from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def get(self, request):
        form = self.form_class()

        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)
        print('hi')

        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                cd['username'], cd['email'], cd['password'])
            messages.success(request, 'You registered successfully', 'success')

            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        pass
