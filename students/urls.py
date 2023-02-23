from django.urls import path
from .views import home_page, dash_board, std_assignments, std_change, std_inbox, std_marks, std_message, std_profile, teachers_list, std_notice, std_profile_update, file_upload


urlpatterns = [
    path('student_home/', home_page, name='student_home'),
    path('student_dashboard/', dash_board, name="student_dashboard"),
    path('student_inbox/', std_inbox, name='student_inbox'),
    path('student_profile/', std_profile, name="student_profile"),
    path('student_marks/', std_marks, name='student_marks'),
    path('student_assignments/', std_assignments, name="student_assignments"),
    path('student_teachers_list/', teachers_list, name='student_teachers_list'),
    path('student_message/', std_message, name="student_message"),
    path('student_changep/', std_change, name='student_changep'),
    path('student_notice/', std_notice, name='student_notice'),
    path('student_profile/student_profile_update', std_profile_update,
         name="student_profile_update"),
    path('assignupload/<str:assign_id>', file_upload,
         name="file_upload"),

]
