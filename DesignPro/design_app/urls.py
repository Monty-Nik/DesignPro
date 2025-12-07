from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/', views.user_profile, name='profile'),
    path('room-plan/create/', views.create_room_plan, name='create_room_plan'),
    path('room-plan/delete/<int:plan_id>/', views.delete_room_plan, name='delete_room_plan'),


    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/application/<int:plan_id>/', views.edit_application, name='edit_application'),
    path('admin-dashboard/categories/', views.manage_categories, name='manage_categories'),
]