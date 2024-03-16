from django.http import HttpResponse
from django.shortcuts import render
from core.models import *
from dateutil.relativedelta import relativedelta

# Create your views here.


def index(request):
    return render(request, "owner/index.html")


def viewAttendance(request):
    grade = request.GET.get("grade")
    attendance = Attendance.objects.all().filter(grade=grade).order_by("date")

    if len(attendance) == 0:
        return render(
            request,
            "owner/view.html",
            {"attendance": "<h1>No attendance has been marked for this class.</h1>"},
        )

    html = '<div class="row"><div class="fixed"><h3>Name</h3></div><div class="non-sticky">'

    dates = []

    for i in attendance:
        if i.date not in dates:
            dates.append(i.date)
            html += f"""
            <div class="flex">
                <h3>{i.date}</h3>
            </div>
            """

    html += "</div></div>"

    students = []

    for i in attendance:
        if i.student not in students:
            students.append(i.student)
            studentattendance = attendance.filter(student=i.student)
            html += f'<div class="row"><div class="fixed"><h3><a href="/owner/view/attendance/{i.student.jssid}/" target="_blank">{i.student.name}</a></h3></div><div class="non-sticky">'
            for j in studentattendance:
                html += f"""
                <div class="flex">
                    <h3>{"Present" if j.present else "Absent"}</h3>
                </div>
                """
            html += "</div></div>"

    return render(request, "owner/view.html", {"attendance": html})


def viewStudentAttendance(request, jssid):
    studentinst = Students.objects.get(jssid=jssid)
    attendance = Attendance.objects.all().filter(student=studentinst).order_by("date")

    filter = request.GET.get("month")


    if len(attendance) == 0:
        return render(
            request,
            "owner/view.html",
            {"attendance": "<h1>No attendance has been marked for this student.</h1>"},
        )

    html = '<div class="row"><div class="fixed"><h3>Name</h3></div><div class="non-sticky">'

    if filter:

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        month = months.index(filter) + 1

        for i in attendance:
            if i.date.month == month:
                html += f"""
            <div class="flex">
                <h3>{i.date}</h3>
            </div>
            """

        html += "</div></div>"

        students = []

        present = 0

        total = 0

        for i in attendance:
            if i.student not in students:
                students.append(i.student)
                studentattendance = attendance.filter(student=i.student)
                html += f'<div class="row"><div class="fixed"><h3><a href="/owner/view/attendance/{i.student.jssid}/" target="_blank">{i.student.name}</a></h3></div><div class="non-sticky">'
                for j in studentattendance:
                    if j.date.month == month:
                        total += 1
                        if j.present:
                            present += 1
                        html += f"""
                        <div class="flex">
                            <h3>{"Present" if j.present else "Absent"}</h3>
                        </div>
                        """
                html += "</div></div>"

        if total == 0:
            return render(
                request,
                "owner/view-student.html",
                {
                    "attendance": "<h2>No attendance has been marked for this month.</h2>",
                },
            )


        return render(
            request,
            "owner/view-student.html",
            {
                "attendance": html,
                "present": present,
                "total": total,
                "absent": total - present,
                "percentage": round(present / total, 2) * 100,
            },
        )

    for i in attendance:
        html += f"""
        <div class="flex">
            <h3>{i.date}</h3>
        </div>
        """

    html += "</div></div>"

    students = []

    present = 0

    for i in attendance:
        if i.student not in students:
            students.append(i.student)
            studentattendance = attendance.filter(student=i.student)
            html += f'<div class="row"><div class="fixed"><h3><a href="/owner/view/attendance/{i.student.jssid}/" target="_blank">{i.student.name}</a></h3></div><div class="non-sticky">'
            for j in studentattendance:
                if j.present:
                    present += 1
                html += f"""
            <div class="flex">
                <h3>{"Present" if j.present else "Absent"}</h3>
            </div>
            """
            html += "</div></div>"

    return render(
        request,
        "owner/view-student.html",
        {
            "attendance": html,
            "present": present,
            "total": len(attendance),
            "absent": len(attendance) - present,
            "percentage": round(present / len(attendance), 2) * 100,
        },
    )
