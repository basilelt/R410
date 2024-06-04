from django.urls import path
from .views import CommentaireListApiView, CommentaireDetailApiView

urlpatterns = [
    path('api/', CommentaireListApiView.as_view()),
    path('api/<int:id>/', CommentaireDetailApiView.as_view()),
]