from django.contrib import admin
from .models import Category, Application

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'client__username']
    readonly_fields = ['created_at', 'updated_at']