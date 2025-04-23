from django.urls import path
from . import views


app_name = 'post'

urlpatterns = [
    path('delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update')
]
