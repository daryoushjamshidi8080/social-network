from django.shortcuts import render, get_object_or_404
from django.views import View
from post.models import Post


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)

        return render(request, 'post/detail_post.html', {'post': post})
