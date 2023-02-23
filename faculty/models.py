from django.db import models
from users.models import Classes, Faculty, Subjects, Faculty_Subject_Class
from datetime import datetime, date


# Create your models here.

# Give Assignments

class Assignments(models.Model):
    assignment_id = models.CharField(max_length=10, unique=True)
    assignment_title = models.CharField(max_length=50, null=False, blank=False)
    assignment_marks = models.CharField(max_length=20, default=40)
    assignment_desc = models.CharField(max_length=100, null=False, blank=False)
    assignment_class = models.ForeignKey(
        Classes, on_delete=models.CASCADE, related_name="given_class")
    assignment_due = models.DateField(default=date.today)
    assignment_created = models.DateTimeField(auto_now_add=True, blank=True)
    assignment_file = models.FileField(
        upload_to="faculty/assignments", blank=False)
    assignment_faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, null=False, blank=False, related_name="assigned_Faculty")
    assignmentsubject = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = ("Assignments")
        verbose_name_plural = ("Assignmentss")

    def __str__(self):
        return str(self.assignment_title)+" "+str(self.assignment_faculty)


# Notice Uploads

class Upload_Notices(models.Model):
    faculty_name_notice = models.ForeignKey(
        Faculty, on_delete=models.CASCADE)
    notice_class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    notice_subject_name = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, null=True, blank=True)
    notice_id = models.CharField(max_length=10, primary_key=True, blank=False)
    notice_title = models.CharField(max_length=30, blank=False, null=False)
    notice_description = models.TextField(
        max_length=150, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name = ("Upload_Notices")
        verbose_name_plural = ("Upload_Noticess")

    def __str__(self):
        return self.notice_id


# Attendance

class Classes_Taken(models.Model):
    faculty_taken = models.ForeignKey(
        Faculty_Subject_Class, on_delete=models.CASCADE, related_name="Teacher_taken_class")
    taken_at = models.DateField(default=date.today)
    attendance_status = models.BooleanField(default=True)
    taken_attendance = models.CharField(max_length=10, default="present")

    class Meta:
        verbose_name = ("Classes_Taken")
        verbose_name_plural = ("Classes_Takens")

    def __str__(self):
        return str(self.faculty_taken)+"  "+str(self.taken_at)


class StudentAttendance(models.Model):
    class_taken = models.ForeignKey(
        Classes_Taken, on_delete=models.CASCADE, related_name="For_which_class")
    studentid = models.CharField(max_length=20, null=False, blank=False)
    studentroll = models.IntegerField(default=1, null=True, blank=True)
    presentorabsent = models.CharField(max_length=10, default="present")
    date = models.DateField(default=date.today)

    class Meta:
        verbose_name = ("StudentAttendance")
        verbose_name_plural = ("StudentAttendances")

    def __str__(self):
        return str(self.class_taken.faculty_taken)+" "+str(self.studentid)+"  "+str(self.studentroll)+" "+str(self.date)


class messages(models.Model):
    sender = models.CharField(max_length=20, blank=False, null=False)
    sender_name = models.CharField(max_length=20, blank=True, null=True)
    receive = models.CharField(max_length=30, blank=False, null=False)
    #title = models.CharField(max_length=20, blank=False, null=False)
    sendmessage = models.CharField(max_length=20, blank=False, null=False)
    posted_at = models.DateField(default=date.today)
    #msg_created = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name = ("messages")
        verbose_name_plural = ("messagess")

    def __str__(self):
        return str(self.sender)+" "+str(self.receive)+" "+str(self.sendmessage)
