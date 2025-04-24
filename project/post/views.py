from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Post
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from .froms import PostUpdateForm
from django.utils.text import slugify


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


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_id'])

        if not post.user.id == request.user.id:
            messages.error(request, 'You cant update this post', 'danger')
            return redirect('home:home')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'post/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance

        # get new form of user
        form = self.form_class(request.POST, instance=post)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'you update this post', 'success')
            return redirect('home:post_detail', post.id, post.slug)
