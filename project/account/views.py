from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, EditeUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation


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

            user = authenticate(
                username=cd['username'], password=cd['password'])
            login(request, user)
            messages.success(request, 'You registered successfully', 'success')

            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next', None)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(
                username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)

                messages.success(request, 'Your successfully login', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')

            else:
                messages.error(
                    request, 'Username or Password is wrong', 'danger')
        return render(request, 'account/login.html', {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Your logged out successfully', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        is_following = False
        posts = Post.objects.filter(user_id=user_id)
        relation = Relation.objects.filter(
            from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'account/profile.html', {'user': user, 'posts': posts, 'user_id': user_id, 'is_following': is_following})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)

        relation = Relation.objects.filter(
            from_user=request.user.id, to_user=user.id)

        if relation.exists():
            messages.error(
                request, 'you are already following this user', 'danger')
        else:
            Relation.objects.create(
                from_user=request.user, to_user=user)
            messages.success(request, 'you followed this user', 'success')
        return redirect('account:user_profile', user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)

        relation = Relation.objects.filter(
            from_user=request.user.id, to_user=user.id)

        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user', 'success')
        else:
            messages.error(
                request, 'you are already unfollow this user', 'danger')

        return redirect('account:user_profile', user.id)


class EditeUserView(LoginRequiredMixin, View):
    form_class = EditeUserForm

    def get(self, request):

        form = self.form_class(instance=request.user.profile, initial={
                               'email': request.user.email})

        return render(request, 'account/edite_profile.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)

        if form.is_valid():
            profile = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = request.user
            user.email = email

            if password:
                user.set_password(password)

            user.save()

            return redirect('account:user_profile', user.id)
        return redirect(request, 'account/edite_profile.html', {'form': form})
