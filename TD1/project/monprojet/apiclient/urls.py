from django.urls import path
from .views import ClientListApiView, ClientDetailApiView

urlpatterns = [
    path('api/', ClientListApiView.as_view()),
    path('api/<int:id>/', ClientDetailApiView.as_view()),
]