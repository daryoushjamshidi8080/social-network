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
