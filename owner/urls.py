from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="admin"),
    path("view/attendace/", viewAttendance, name="view-attendance"),
    path("view/attendance/<str:jssid>/", viewStudentAttendance, name="view-student-attendance")
]
