from django.urls import path
from .views import GareListApiView, GareDetailApiView

urlpatterns = [
    path('api/', GareListApiView.as_view()),
    path('api/<int:id>/', GareDetailApiView.as_view()),
]