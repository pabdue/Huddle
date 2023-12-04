from django.contrib import admin
from .models import Account, Task

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'username']
    search_fields = ['first_name', 'last_name', 'email', 'username']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'assigned_members', 'due_date')
