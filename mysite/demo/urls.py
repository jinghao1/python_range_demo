from django.urls import path
from . import views

urlpatterns = [
    path('get_open', views.index_get_r),
    path('post_open', views.index_post_r),
]