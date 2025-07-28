from django.urls import path
from . import views

app_name = 'PSEvents'

urlpatterns = [
    path('', views.EventView.as_view(), name='home'),
]