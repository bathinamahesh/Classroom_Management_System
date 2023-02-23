from distutils.command.upload import upload
from pydoc import classname
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_id = models.CharField(max_length=30, blank=False, primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    user_status = models.CharField(max_length=500, blank=True)
    gender_choices = (("Male", "Male"), ("Female", "Female"))
    sex = models.CharField(
        max_length=10, choices=gender_choices, default="not_known")
    roll = models.IntegerField(default=1, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="faculty/profiles", blank=True,
                                    default="faculty/profiles/download.png")  # default=

# Student DAtabase


class Student(models.Model):
    studentname = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='student_name', primary_key=True)

    class Meta:
        verbose_name = ("Student")
        verbose_name_plural = ("Students")

    def __str__(self):
        return self.studentname.username

# Faculty Database


class Faculty(models.Model):
    facultyname = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='faculty', primary_key=True)
    '''classroom = models.ForeignKey(
        Classes, on_delete=models.CASCADE, related_name='classnames')
    subject_teach = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, related_name="teaching_subject")'''

    class Meta:
        verbose_name = ("Faculty")
        verbose_name_plural = ("Faculty")

    def __str__(self):
        return self.facultyname.username

# Subjects


class Subjects(models.Model):
    subject = models.CharField(
        max_length=30, null=False, blank=False, primary_key=True)

    class Meta:
        verbose_name = ("Subjects")
        verbose_name_plural = ("Subjectss")

    def __str__(self):
        return self.subject


class Classes(models.Model):

    '''classrepr = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='class_member')'''
    classname = models.CharField(
        max_length=10, default="CSE", primary_key=True, null=False, blank=False)

    class Meta:
        verbose_name = ("Class")
        verbose_name_plural = ("Classes")

    def __str__(self):
        return self.classname


# -Student CLass relation

class Student_Class(models.Model):
    student_id = models.OneToOneField(Student,
                                      on_delete=models.CASCADE, related_name="Std_class_relation", primary_key=True)
    class_name = models.ForeignKey(Classes,
                                   on_delete=models.CASCADE, related_name="std_class_name")

    class Meta:
        verbose_name = ("Student_Class")
        verbose_name_plural = ("Student_Classs")
        '''constraints = [
            models.UniqueConstraint(
                fields=['migration', 'host'], name='unique_migration_host_combination'
            )]'''

    def __str__(self):
        return str(self.student_id.studentname)+"__"+str(self.class_name.classname)

# class - Representative


class Class_repr(models.Model):
    repr_name = models.OneToOneField(
        Student, on_delete=models.CASCADE, related_name="cls_reprs")
    class_name = models.ForeignKey(
        Classes, on_delete=models.CASCADE, related_name="class_name_rel"
    )

    class Meta:
        verbose_name = ("Class_repr")
        verbose_name_plural = ("Class_reprs")

    def __str__(self):
        return str(self.repr_name)


# Faculty_Subject_class

class Faculty_Subject_Class(models.Model):
    faculty_name = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name="rel_faculty_name")
    subject_name = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, related_name="rel_subject_name")
    class_name = models.ForeignKey(
        Classes, on_delete=models.CASCADE, related_name="rel_class_name")

    class Meta:
        verbose_name = ("Faculty_Subject_Class")
        verbose_name_plural = ("Faculty_Subject_Classs")
        constraints = [
            models.UniqueConstraint(
                fields=['subject_name', 'class_name'], name='unique_migration_host_combination'
            )]

    def __str__(self):
        return str(self.faculty_name.facultyname)+"-"+str(self.subject_name.subject)+"-"+str(self.class_name.classname)


# Create your models here
