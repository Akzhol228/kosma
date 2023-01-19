from django.urls import path
from . import views

app_name = 'manager_dashboard'

urlpatterns = [
    path('', views.DemandListView.as_view(), name='demand_list'),
    path('call_back/list', views.CallBackListView.as_view(), name='call_back_list'),
]
