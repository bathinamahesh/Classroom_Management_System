from django.contrib import admin
from .models import Upload_Notices, Assignments, StudentAttendance, Classes_Taken, messages

admin.site.register(Upload_Notices)
admin.site.register(Assignments)
admin.site.register(StudentAttendance)
admin.site.register(Classes_Taken)
admin.site.register(messages)
# Register your models here.
