from django.urls import path
from .views import AlbumListApiView, AlbumDetailApiView

urlpatterns = [
    path('api/', AlbumListApiView.as_view()),
    path('api/<int:id>/', AlbumDetailApiView.as_view()),
]