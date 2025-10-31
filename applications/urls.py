from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_application, name='create_application'),
    path('my/', views.my_applications, name='my_applications'),
]