from django.db import models
from users.models import Classes, Faculty, Subjects, Faculty_Subject_Class, Student, User
from datetime import datetime, date
from faculty.models import Assignments


# Create your models here.
class Mid_marks(models.Model):
    faculty = models.ForeignKey(
        Faculty_Subject_Class, on_delete=models.CASCADE, related_name="faculty_subject")
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student")
    mid1 = models.CharField(max_length=10, blank=True, null=True)
    mid2 = models.CharField(max_length=10, blank=True, null=True)
    internals = models.CharField(max_length=10, blank=True, null=True)
    lab_marks = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = ("Mid_marks")
        verbose_name_plural = ("Mid_markss")

    def __str__(self):
        return str(self.faculty)+"  "+str(self.student)


class Submissions(models.Model):
    assignment_detail = models.ForeignKey(
        Assignments, on_delete=models.CASCADE, related_name="submissionids")
    faculty = models.CharField(max_length=20, null=False, blank=False)
    student_id = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    dateofsub = models.DateField(default=date.today)
    file_submit = models.FileField(
        upload_to="students/submissions", blank=False)
    givenmarks = models.CharField(max_length=10, null=True, blank=True)
    is_submitted = models.CharField(
        max_length=5, default=0, null=True, blank=True)
    is_awarded = models.CharField(
        max_length=5, default=0, null=True, blank=True)

    class Meta:
        verbose_name = ("Submissions")
        verbose_name_plural = ("Submissionss")

    def __str__(self):
        return str(self.assignment_detail)+"    "+str(self.student_id)+"    "
