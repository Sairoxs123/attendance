from django.db import models

# Create your models here.

class Teachers(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    name = models.CharField("Name", max_length=50)
    email = models.EmailField("Email", max_length=50)
    password = models.CharField("Password", max_length=100)
    ct = models.BooleanField("Class Teacher")
    teaches = models.CharField("Class", max_length=3, null=True, blank=True)

    def __str__(self):
        return self.name

class Students(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    name = models.CharField("Name", max_length=50)
    jssid = models.CharField("JSSID", max_length=11)
    grade = models.CharField("Class", max_length=3)

    def __str__(self):
        return f"{self.name}"


class Attendance(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    grade = models.CharField("Class", max_length=3)
    date = models.DateField("Date")
    present = models.BooleanField("Present")
    sick = models.BooleanField("Sick", default=False)
    ct = models.BooleanField("Class Teacher")
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)


class Notes(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    title = models.CharField("Title", max_length=256)
    description = models.CharField("Description", max_length=1024)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    students = models.ManyToManyField(Students, related_name="notes_students")
    date = models.DateField("Date")


class Notification(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    sent_by = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name="sent_by")
    received_by = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name="recieved_by")
    date = models.DateField("Date")
    message = models.CharField("Message", max_length=2048)
    seen = models.BooleanField("Seen", default=False)
