from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Teachers)

class TeachersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']
    ordering = ['id']
    search_fields = ['name', 'email']


@admin.register(Students)

class StudentsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "jssid", "grade"]
    ordering = ["id"]
    search_fields = ["name", "jssid", "grade"]
    list_filter = ["grade"]


@admin.register(Attendance)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "grade", "date", "present"]
    ordering = ["id"]
    search_fields = ["student", "date", "grade"]
    list_filter = ["grade"]


@admin.register(Notes)

class NotesAdmin(admin.ModelAdmin):
    list_display = ["id", "teacher", "date"]
    ordering = ["id"]
    search_fields = ["teacher", "date"]
    list_filter = ["date"]


@admin.register(Notification)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "sent_by", "received_by", "date", "seen"]
    ordering = ["id"]
    search_fields = ["date"]
