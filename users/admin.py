from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Classes, Student, Faculty, Subjects, Student_Class, Faculty_Subject_Class, Class_repr

admin.site.register(User)
admin.site.register(Classes)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Subjects)
admin.site.register(Class_repr)
admin.site.register(Student_Class)
admin.site.register(Faculty_Subject_Class)
# Register your models here.
