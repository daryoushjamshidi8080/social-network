from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from post.models import Post, Comment
from post.froms import CommentCreateFrom, CommentReplyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):
    form_class = CommentCreateFrom
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(
            Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])

        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id, post_slug):

        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        form = self.form_class()
        comments = self.post_instance.pcomments.filter(is_reply=False)

        return render(request, 'post/detail_post.html', {'post': self.post_instance, 'comments': comments, 'form': form, 'reply_form': self.form_class_reply(), 'can_like': can_like})

    @method_decorator(login_required)
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


class PostAddReplyView(LoginRequiredMixin, View):
    from_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)

        form = self.from_class(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()

            messages.success(
                request, 'Your reply submitted successfully', 'success')

        return redirect('home:post_detail', post.id, post.slug)
