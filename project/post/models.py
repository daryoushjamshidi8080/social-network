from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-body',)

    def __str__(self):
        return f' {self.slug}  "{self.update}"'

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))

    def likes_count(self):
        return self.pvotes.count()

    def user_can_like(self, user):
        user_like = user.uvotes.filter(post=self)
        if user_like.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='pcomments')
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}  - {self.body[:30]} - post {self.post.slug[:10]}'


class Vote(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='uvotes')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='pvotes')

    def __str__(self):
        return f'{self.user} - linked {self.post.slug}'
