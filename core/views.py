import json
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.


def index(request):

    if not request.session.get("logged-in"):
        return redirect("/account/login")

    email = request.session.get("email")

    inst = Teachers.objects.get(email=email)

    if inst.ct:
        return render(
            request,
            "core/index.html",
            {"class": inst.teaches, "today": str(datetime.date.today())},
        )

    return render(request, "core/index.html")


def addStudent(request):

    if request.method == "POST":
        name = request.POST.get("name")
        jssid = "JSSPS" + request.POST.get("jssid")
        grade = request.POST.get("class")

        results = Students.objects.all().filter(Q(name=name) | Q(jssid=jssid))

        if len(results) > 0:
            return render(request, "core/add.html", {"error": "exists"})

        Students(name=name, jssid=jssid, grade=grade).save()

        return render(request, "core/add.html", {"success": True})

    return render(request, "core/add.html")


def getAttendance(request):
    date = request.GET.get("date")
    grade = request.GET.get("grade")

    attendance = Attendance.objects.all().filter(grade=grade).filter(date=date)

    if len(attendance) > 0:
        return JsonResponse(
            {"students": "<h1>Attendance has been marked for today.</h1>"}
        )

    students = Students.objects.all().filter(grade=grade).order_by("name")

    start = 1

    for i in students:
        i.id = start
        start += 1

    html = """
    <table border="2">
    <tr>
        <th>Roll No.</th>
        <th>Name</th>
        <th>Attendance</th>
    </tr>
    """

    for i in students:
        html += f"""
        <tr id="{ i.id }">
            <td>{ i.id }</td>
            <td>{ i.name }</td>
            <td>
                <input type="radio" name="{ i.name }" value="1" form="form" required>Present
                <input type="radio" name="{ i.name }" value="0" form="form">Absent
            </td>
        </tr>
        """

    html += """
    </table>

    <br><br>

    <button type="submit" form="form">Mark Attendance</button>
    """

    return JsonResponse({"students": html})


@csrf_exempt
def markAttendance(request):
    grade = request.POST.get("class")
    date = request.POST.get("date")

    students = Students.objects.all().filter(grade=grade)

    for i in students:
        x = request.POST.get(i.name)
        Attendance(student=i, date=date, grade=grade, present=x).save()

    return redirect("/")


def viewAttendance(request):
    grade = request.GET.get("grade")
    date = request.GET.get("date")

    today = datetime.date.today()

    dates = [today]

    for i in range(1, 15):
        dates.append(today - datetime.timedelta(days=i))

    if grade and date:
        return

    return render(request, "core/view.html", {"dates": dates})


def notes(request):
    students = Students.objects.all()
    return render(request, "core/notes.html", {"students": students})


def search(request):
    name = request.GET.get("name")
    filtered = Students.objects.filter(name__contains=name)

    students = []

    for i in filtered:
        students.append(
            f"""
            <input type="checkbox" value="{ i.id }" id="{ i.id }" oninput="selectStudents(`{ i.id }`, `{ i } - { i.grade }`)">{ i } - { i.grade }
        """.strip()
        )

    return JsonResponse({"students": students})


# MOBILE
###########################################
###########################################
###########################################
###########################################
###########################################
###########################################


def mobileGetAttendance(request):
    date = request.GET.get("date")
    grade = request.GET.get("grade")
    teacheremail = request.GET.get("teacher")

    teacherinst = Teachers.objects.get(email=teacheremail)

    attendance = (
        Attendance.objects.all()
        .filter(grade=grade)
        .filter(date=date)
        .filter(teacher=teacherinst)
    )

    if len(attendance) > 0:
        return JsonResponse(
            {
                "students": "Attendance has already been marked by you for the selected date."
            }
        )

    students = Students.objects.all().filter(grade=grade).order_by("name")

    studentsList = []

    for i in students:
        studentsList.append({"id": i.id, "name": i.name})

    return JsonResponse({"students": studentsList})


@csrf_exempt
def mobileMarkAttendance(request):
    data = request.body.decode()
    jsdata = json.loads(data)
    date = jsdata["date"]
    grade = jsdata["grade"]
    attendance = jsdata["attendance"]
    email = jsdata["email"]

    teacherinst = Teachers.objects.get(email=email)

    if teacherinst.ct and teacherinst.teaches == grade:
        for i in attendance:
            student = Students.objects.get(id=i["id"])
            if i["present"] == "Sick":

                Attendance(
                    student=student,
                    date=date,
                    grade=grade,
                    present=False,
                    sick=True,
                    ct=True,
                    teacher=teacherinst,
                ).save()

            else:

                Attendance(
                    student=student,
                    date=date,
                    grade=grade,
                    present=i["present"],
                    ct=True,
                    teacher=teacherinst,
                ).save()

    else:
        for i in attendance:
            student = Students.objects.get(id=i["id"])
            if i["present"] == "Sick":

                Attendance(
                    student=student,
                    date=date,
                    grade=grade,
                    present=False,
                    sick=True,
                    ct=False,
                    teacher=teacherinst,
                ).save()


            else:
                Attendance(
                    student=student,
                    date=date,
                    grade=grade,
                    present=i["present"],
                    ct=False,
                    teacher=teacherinst,
                ).save()

    different = []

    ct = Teachers.objects.get(teaches=grade)

    ctattendance = (
        Attendance.objects.all()
        .filter(grade=grade)
        .filter(teacher=ct)
        .filter(date=date)
        .order_by("student")
    )

    markedattendance = (
        Attendance.objects.all()
        .filter(grade=grade)
        .filter(teacher=teacherinst)
        .filter(date=date)
        .order_by("student")
    )

    checker = lambda present: "Present" if present else "Absent"

    for i in range(len(ctattendance)):
        if ctattendance[i].present != markedattendance[i].present:
            different.append(
                f"The attendance for student {ctattendance[i].student.name} has been changed from {checker(ctattendance[i].present)} to {checker(markedattendance[i].present)}."
            )

    if len(different) > 0:
        return JsonResponse({"changed": different, "date": date, "id":ct.email})

    return JsonResponse({"marked": True})


def mobileFetchDetails(request):
    grade = request.GET.get("grade")
    date = request.GET.get("date")
    notesinst = Notes.objects.all().filter(date=date)
    students = Students.objects.all().filter(grade=grade)
    teacher = Teachers.objects.get(teaches=grade)

    note = []

    if len(notesinst) == 0:
        note = "No notes for today."

    else:
        for i in notesinst:
            for j in students:
                if j in students:
                    mentioned = []
                    for k in i.students.all():
                        mentioned.append({"name": k.name, "grade": k.grade})
                    note.append(
                        {
                            "id": i.id,
                            "title": i.title,
                            "teacher": i.teacher.name,
                            "description": i.description,
                            "mentioned": mentioned,
                        }
                    )
                    break

    attendance = (
        Attendance.objects.all()
        .filter(grade=grade)
        .filter(date=date)
        .filter(teacher=teacher)
    )

    marked = []

    if len(attendance) == 0:
        marked = "Attendance has not been marked for the selected date."

    else:
        for i in attendance:
            marked.append({"name": i.student.name, "present": i.present})

    return JsonResponse({"note": note, "attendance": marked})


def mobileGetStudents(request):
    temp = Students.objects.all().order_by("name").order_by("grade")
    students = []

    for i in temp:
        students.append({"label": f"{i.name} {i.grade}", "value": i.jssid})

    return JsonResponse({"students": students})


@csrf_exempt
def mobileCreateNote(request):
    data = request.body.decode()
    jsdata = json.loads(data)
    name = jsdata["name"]
    date = jsdata["date"]
    title = jsdata["title"]
    description = jsdata["description"]
    students = jsdata["students"]

    teacher = Teachers.objects.get(name=name)

    try:
        lid = Notes.objects.last().id + 1

    except:
        lid = 1

    Notes(
        id=lid, teacher=teacher, title=title, description=description, date=date
    ).save()

    noteisnt = Notes.objects.get(id=lid)

    for i in students:
        student = Students.objects.get(jssid=i)
        noteisnt.students.add(student)

    noteisnt.save()

    return JsonResponse({"created": "Note has created successfully."})


def fetchNotes(request):
    name = request.GET.get("name").strip()
    teacher = Teachers.objects.get(name=name)
    notes = []
    today = datetime.date.today()

    notesinst = Notes.objects.all().filter(teacher=teacher)

    for i in notesinst:
        if i.date >= today:
            mentioned = []
            for j in i.students.all():
                mentioned.append({"name": j.name, "grade": j.grade})
            notes.append(
                {
                    "id": i.id,
                    "title": i.title,
                    "date": i.date,
                    "description": i.description,
                    "mentioned": mentioned,
                }
            )

    if len(notes) == 0:
        return JsonResponse({"notes": "You have no active notes."})

    return JsonResponse({"notes": notes})


def deleteNote(request):
    noteid = request.GET.get("id")

    Notes.objects.get(id=noteid).delete()

    return JsonResponse({"deleted": True})


#@csrf_exempt
def createNotification(request):
    sent = request.GET.get("sent")
    received = request.GET.get("received")
    date = request.GET.get("date")
    message = request.GET.get("message")

    sentinst = Teachers.objects.get(email=sent)
    receivedinst = Teachers.objects.get(email=received)

    Notification(
        sent_by=sentinst,
        received_by=receivedinst,
        date=date,
        message=message,
        seen=False,
    ).save()

    return JsonResponse({"created": True})


def notificationMarkAsRead(request):
    id = request.GET.get("id")
    notification = Notification.objects.get(id=id)
    notification.seen = True

    notification.save()

    return JsonResponse({"marked": True})


def getUnseenNotificationsCount(request):
    email = request.GET.get("email")
    teacher = Teachers.objects.get(email=email)

    notifications = (
        Notification.objects.all().filter(received_by=teacher).filter(seen=False)
    )

    return JsonResponse({"unseen": len(notifications)})


def getNotifications(request):
    email = request.GET.get("email")
    teacher = Teachers.objects.get(email=email)

    notifications = (
        Notification.objects.all().filter(received_by=teacher)
    )

    unseen = []
    seen = []

    for i in notifications:
        if i.seen:
            seen.append(
                {"id": i.id, "sent_by":i.sent_by.name, "date":i.date, "message":str(i.message).split(",")}
            )

        else:
            unseen.append(
                {"id": i.id, "sent_by":i.sent_by.name, "date":i.date, "message":str(i.message).split(",")}
            )

    return JsonResponse({"unseen":unseen, "seen":seen})
