from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    # в разработке
    # path('profile/', views.user_profile, name='profile'),
    # path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
