from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('search/<video_id>/', views.search_videos, name='search_videos'),
    path('search2/<video_id>/', views.search_videos2, name='search_videos2'),
    path('', views.video_list, name='video_list'),
    path('play_video/<video_id>/', views.play_video, name='play_video'),
]
