from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Post
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin


def post(request):
    return HttpResponse('hiii')


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Post Deleted successfully', 'success')
        else:
            messages.error(request, 'you cant delete this post', 'danger')

        return redirect('home:home')
