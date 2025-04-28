from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('display_post/<int:post_id>/<slug:post_slug>/',
         views.PostDetailView.as_view(), name='post_detail'),
    path('reply/<int:post_id>/<int:comment_id>/',
         views.PostAddReplyView.as_view(), name='add_reply')
]
