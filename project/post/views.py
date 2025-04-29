from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Post, Vote
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from .froms import PostUpdateForm, PostCreateForm
from django.utils.text import slugify


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
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
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])

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


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'post/create.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            body = form.cleaned_data['body']
            new_post = Post.objects.create(
                body=body,
                slug=slugify(body[:30]),
                user=request.user
            )
            messages.success(request, 'You created this post', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        link = Vote.objects.filter(user=request.user, post=post)

        if link.exists():
            messages.error(
                request, 'You have already linked this post', 'danger')

        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'You liked this post', 'success')

        return redirect('home:post_detail', post.id, post.slug)
