from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from post.models import Post
from post.froms import CommentCreateFrom
from django.contrib import messages


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):
    form_class = CommentCreateFrom

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(
            Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])

        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id, post_slug):
        form = self.form_class()

        comments = self.post_instance.pcomments.filter(is_reply=False)

        return render(request, 'post/detail_post.html', {'post': self.post_instance, 'comments': comments, 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(
                request, 'Your comment submitted successfully', 'success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)
