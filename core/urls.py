from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('student/add/', addStudent, name="add-student"),
    path('attendance/mark/', markAttendance, name="mark-attendance"),
    path('attendance/get/', getAttendance,  name='get-attendance'),
    path('attendance/view/', viewAttendance, name= 'view-attendance'),
    path('notes/', notes, name="notes"),
    path('search/students/', search, name="search"),
    path('attendance/get/mobile/', mobileGetAttendance,  name='mobile-get-attendance'),
    path('attendance/mark/mobile/', mobileMarkAttendance, name="mobile-mark-attendance"),
    path('details/fetch/mobile/', mobileFetchDetails, name="mobile-fetch-details"),
    path('details/fetch/students/mobile/', mobileGetStudents, name="mobile-students-fetch-details"),
    path('notes/mobile/create/', mobileCreateNote, name="mobile-create-note"),
    path('notes/mobile/fetch/', fetchNotes, name="mobile-fetch-notes"),
    path('notes/mobile/delete/', deleteNote, name="mobile-delete-note")
]
