from django.contrib import admin
from .models import Category, UserProfile, RoomPlan

# Регистрируем модели для доступа через /superadmin/

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'user_type', 'agreement')
    list_filter = ('user_type', 'agreement')
    search_fields = ('full_name', 'user__username')
    raw_id_fields = ('user',)

@admin.register(RoomPlan)
class RoomPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'upload_date', 'assigned_to')
    list_filter = ('status', 'category', 'upload_date')
    search_fields = ('title', 'user__username', 'description')
    raw_id_fields = ('user', 'assigned_to')
    list_editable = ('status', 'category', 'assigned_to')
    date_hierarchy = 'upload_date'
