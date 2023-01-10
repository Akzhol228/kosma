from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('message/create', views.MessageCreateView.as_view(), name='message_create'),
]
