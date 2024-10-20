from django.contrib import admin

from .models import Task, Comment


# Register the Task model
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
    'title', 'status', 'priority', 'due_date', 'assigned_to')  # Customize based on fields in your Task model
    search_fields = ('title', 'description')  # Optional: Add search functionality


# Register the Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'comment', 'created_at')  # Customize based on fields in your Comment model
    search_fields = ('content', 'user__username')  # Optional: Add search functionality
