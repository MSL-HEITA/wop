from django.urls import path
from . import views

urlpatterns = [
    path('chatroom',views.stream,name="chatroom")
]