# chat/urls.py
from django.urls import path

from .views import chat, room


urlpatterns = [
    path("", chat, name="chat"),
    path("/<str:room_name>/", room, name="room"),
]