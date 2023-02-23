from django.urls import path
from .views import home_page, dash_board, inbox, profile, take_attendance, upload_assignment, profile, assignment_list, view_submissions, students_list, write_notice, change_password, faculty_time_table, confirm, profile_update, givemarks, detailattend


urlpatterns = [
    path('faculty_home/', home_page, name='faculty_home'),
    path('faculty_dashboard/', dash_board, name="faculty_dashboard"),
    path('faculty_inbox/', inbox, name="faculty_inbox"),
    path('faculty_profile/', profile, name="faculty_profile"),
    path('faculty_profile/profile_UPdate',
         profile_update, name="profile_update"),
    path('faculty_take_attendace/', take_attendance,
         name="faculty_take_attendace"),
    path('faculty_upload_assignment/', upload_assignment,
         name="faculty_upload_assignment"),
    path('faculty_assignment_list/', assignment_list,
         name="faculty_assignment_list"),
    path('faculty_view_submissions/', view_submissions,
         name="faculty_view_submissions"),
    path('faculty_student_list/', students_list, name="faculty_student_list"),
    path('faculty_write_Notice/', write_notice, name="faculty_write_Notice"),
    path('faculty_password_change/', change_password,
         name="faculty_password_change"),
    path('faculty_time_table/', faculty_time_table,
         name="faculty_time_table"),
    path('confirmation/<str:class_n>', confirm,
         name="confirm"),
    path(
        'givemarks/<str:assign_id>/<str:assign_stdid>', givemarks, name="givemarks"),
    path(
        'DetailAttendance/', detailattend, name="detailattend")


]
