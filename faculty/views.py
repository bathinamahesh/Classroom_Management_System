
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Classes, Student_Class, Faculty_Subject_Class, Faculty
from .models import Upload_Notices, Assignments, Subjects, Classes_Taken, StudentAttendance, messages
from students.models import Mid_marks, Submissions
from django.db.models.query import QuerySet
from datetime import datetime, date
from .forms import UserUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from django.contrib import messages as msg

User = get_user_model()


@login_required
def home_page(request):
    return render(request, 'faculty/faculty_main.html')


@login_required
def dash_board(request):
    return render(request, 'faculty/faculty_dashboard.html')


@login_required
def inbox(request):
    if request.method == "POST":
        userid = request.user.user_id
        username = request.user.first_name
        msgto = request.POST.get("get_name")
        print("__"*20, msgto)
        msg = request.POST.get("textmessage")
        objmsg = messages(sender=userid, receive=msgto,
                          sender_name=username, sendmessage=msg,)
        objmsg.save()
    curruser = request.user.user_id
    inboxmsg = messages.objects.filter(receive=str(curruser))
    return render(request, 'faculty/faculty_inbox.html', context={"inboxmsg": inboxmsg})


@login_required
def profile(request):
    if request.method == 'POST':
        curruser = request.user.username
        data = User.objects.get(user_id=curruser)
        return render(request, 'faculty/faculty_profile_update.html', context={"userprofile": data})
    curruser = request.user.username
    data = User.objects.get(user_id=curruser)
    return render(request, 'faculty/faculty_profile.html', context={"basicdata": data})


@login_required
def take_attendance(request):
    if request.method == 'POST':
        class_nam = request.POST.get('select_student_class')
        # print("-_"*50, class_nam)
        selecting_students = Student_Class.objects.filter(class_name=class_nam)
        l = []
        for i in selecting_students:
            l.append(i.student_id)
        final_list = []
        for i in l:
            final_list.append(User.objects.get(username=i))
        faculty_named = request.user.user_id
        total_class_obj = Faculty_Subject_Class.objects.filter(
            faculty_name=Faculty.objects.get(facultyname=faculty_named))
        return render(request, 'faculty/faculty_take_attendance.html', context={"students_list_test": final_list, "classroom_name": class_nam, "total_classes": total_class_obj})
    faculty_named = request.user.user_id
    total_class_obj = Faculty_Subject_Class.objects.filter(
        faculty_name=Faculty.objects.get(facultyname=faculty_named))
    return render(request, 'faculty/faculty_take_attendance.html', context={"total_classes": total_class_obj})


@login_required
def upload_assignment(request):
    upload_done = 0
    if request.method == 'POST':
        assign_faculty = request.user.username
        assign_id = request.POST.get('assign_id')
        assign_title = request.POST.get('assign_title')
        assign_desc = request.POST.get('assign_desc')
        assign_marks = request.POST.get('assign_marks')
        assign_class = request.POST.get('assign_class')
        assign_due = request.POST.get('assign_due')
        if "assignupload" in request.FILES:
            print("___"*20)
            upload = request.FILES['assignupload']
            """fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)
            print("__"*30, "__*********"*20, file_url)"""
        assign_faculty_subject = Faculty_Subject_Class.objects.get(
            faculty_name=assign_faculty, class_name=assign_class)
        assign_faculty_subject = assign_faculty_subject.subject_name
        writing_assignment = Assignments(assignment_id=assign_id, assignment_title=assign_title, assignment_marks=assign_marks, assignment_class=Classes.objects.get(classname=assign_class),
                                         assignment_due=assign_due, assignment_file=upload, assignment_faculty=Faculty.objects.get(facultyname=assign_faculty), assignmentsubject=Subjects.objects.get(subject=assign_faculty_subject), assignment_desc=assign_desc)
        writing_assignment.save()
        upload_done = 1

    faculty_named = request.user.user_id
    total_class_obj = Faculty_Subject_Class.objects.filter(
        faculty_name=Faculty.objects.get(facultyname=faculty_named))
    return render(request, 'faculty/faculty_upload_assignment.html', context={"upload_done": upload_done, "total_classes": total_class_obj})


@login_required
def assignment_list(request):
    l = Assignments.objects.filter(
        assignment_faculty=Faculty.objects.get(facultyname=request.user.username)).order_by('assignment_created')
    return render(request, 'faculty/faculty_assignment_list.html', context={"assignments": l})


@login_required
def view_submissions(request):
    facult = request.user.user_id
    submissions = Submissions.objects.filter(faculty=facult)
    return render(request, 'faculty/faculty_view_submissions.html', context={"tot_submissions": submissions})


@ login_required
def students_list(request):
    if request.method == 'POST':
        class_nam = request.POST.get('select_student_class')
        # print("-_"*50, class_nam)
        selecting_students = Student_Class.objects.filter(class_name=class_nam)
        l = []
        for i in selecting_students:
            l.append(i.student_id)
        final_list = []
        for i in l:
            final_list.append(User.objects.get(username=i))
        return render(request, 'faculty/faculty_students_list.html', context={"students_list_test": final_list, "classroom_name": class_nam})
    return render(request, 'faculty/faculty_students_list.html')


@ login_required
def write_notice(request):
    faculty_write_error = 0
    if request.method == 'POST':
        try:
            faculty_names = request.user.username
            notice_ids = request.POST.get('notice_id')
            notice_titles = request.POST.get('notice_title')
            notice_class = request.POST.get('noticed_class')
            notice_desc = request.POST.get('notice_text')
            # print("__"*20, notice_class, faculty_names,notice_ids, notice_desc, notice_titles)
            # --Need to change Classes Choice to CharField
            x = type(int(notice_ids))  # For ID validation
            if(notice_titles == "" or notice_desc == ""):
                raise Exception("Please Enter Correct Details")
            notice_subjected = Faculty_Subject_Class.objects.get(
                faculty_name=faculty_names, class_name=notice_class)
            if(notice_subjected == None):
                notice_subject = "default"
            else:
                notice_subject = notice_subjected.subject_name
            writing_notice = Upload_Notices(notice_id=notice_ids, notice_title=notice_titles, notice_description=notice_desc,
                                            faculty_name_notice=Faculty.objects.get(facultyname=faculty_names), notice_class_name=Classes.objects.get(classname=notice_class), notice_subject_name=notice_subject)
            writing_notice.save()
            faculty_write_error = 0
        except:
            faculty_write_error = 1
            # print("___"*100, "please Enter Correct Details Asap")
    # total_objects = Upload_Notices.objects.all()
    faculty_named = request.user.user_id
    total_class_obj = Faculty_Subject_Class.objects.filter(
        faculty_name=Faculty.objects.get(facultyname=faculty_named))
    print("__"*25, faculty_write_error)
    total_objects = Upload_Notices.objects.filter(
        faculty_name_notice=request.user.username)
    # print("_*"*50, total_objects)
    return render(request, 'faculty/faculty_write_notice.html', context={
        "all_notices": total_objects,
        "faculty_errored": faculty_write_error,
        "total_classes": total_class_obj,

    })


@ login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            msg.success(
                request, 'Your password was successfully updated!')
            return render(request, 'faculty/faculty_dashboard.html', {
                'form': form, "passwordchanged": 1
            })
        else:
            return render(request, 'faculty/faculty_password_change.html', {'form': form, "errorinchange": 1})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'faculty/faculty_password_change.html', {
        'form': form
    })


@ login_required
def faculty_time_table(request):
    return render(request, 'faculty/faculty_timetable.html')


@ login_required
def confirm(request, class_n):

    is_taken = 0
    try:
        # Register Classes and Take attendance
        # ------------getting class and subject details
        faculty = request.user.user_id
        faculty_obj = Faculty_Subject_Class.objects.get(
            faculty_name=Faculty.objects.get(facultyname=faculty), class_name=class_n)
        # ---validating With Today Date
        isanytaken = Classes_Taken.objects.get(
            faculty_taken=faculty_obj, taken_at=date.today())
        is_taken = 1
    except:
        is_taken = 0
    if(is_taken == 0):
        # REgister the Class
        takentheclass = Classes_Taken(faculty_taken=faculty_obj)
        takentheclass.save()
        # register the Students Attendance
        takenobj = Classes_Taken.objects.get(
            faculty_taken=faculty_obj, taken_at=date.today())
        selected = Student_Class.objects.filter(
            class_name=Classes.objects.get(classname=class_n))
        for i in selected:
            id = i.student_id
            roll = User.objects.get(user_id=id).roll
            print("\n\n", id)
            status = request.POST.get(str(id))
            print("\n\n", "__"*20, i.student_id, "  ", status)
            obj = StudentAttendance(
                class_taken=takenobj, studentid=id, studentroll=roll, presentorabsent=status)  # presentorabsent=status
            obj.presentorabsent = status
            print("\n\n", obj, "\n\n")
            obj.save()
    # Returning No.of Classes
    totalclasses = Classes_Taken.objects.filter(
        faculty_taken=faculty_obj).order_by('-taken_at')

    return render(request, 'faculty/trying.html', context={"totalclasses": totalclasses, "errorcame": is_taken})


@ login_required
def profile_update(request):
    errorsave = 0
    if request.method == "POST":
        curruser = request.user.username
        instance = User.objects.get(user_id=curruser)
        # instance.user_id = request.POST.get("profile_id")
        instance.bio = request.POST.get("profile_bio")
        instance.location = request.POST.get("profile_location")
        instance.sex = request.POST.get("profile_gender")
        instance.birth_date = request.POST.get("profile_birth")
        instance.first_name = request.POST.get("profile_first")
        instance.last_name = request.POST.get("profile_last")
        instance.email = request.POST.get("profile_email")
        # -------For Files
        if "profile_pic" in request.FILES:
            upload = request.FILES['profile_pic']
            """fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)
            print("__"*30, "__*********"*20, file_url)"""
            instance.profile_pic = upload
        print("|___|"*20, instance.profile_pic.url)
        try:
            instance.save()
            print("\n\n\n", instance.user_id, " ", instance.first_name, " ", instance.last_name, " ", instance.email, " ", instance.bio, " ", instance.location,
                  " ", instance.sex, " ", instance.birth_date, " ", "\n\n")
            return redirect('faculty_profile')
        except Exception as e:
            print("______"*30, "Error While Saving", e)

    curr = request.user.username
    data = User.objects.get(user_id=curr)
    return render(request, 'faculty/faculty_profile_update.html', context={"userprofile": data})


def givemarks(request, assign_id, assign_stdid):
    # student_id
    getobj = Submissions.objects.get(student_id=User.objects.get(user_id=assign_stdid),
                                     assignment_detail=Assignments.objects.get(assignment_id=assign_id))
    print(getobj)
    marks = request.POST.get("given_marks")
    if(str(marks) == ""):
        facult = request.user.user_id
        submissions = Submissions.objects.filter(faculty=facult)
        return render(request, 'faculty/faculty_view_submissions.html', context={"tot_submissions": submissions, "errorwhilegive": 1})
    else:
        getobj.givenmarks = marks
        getobj.is_awarded = str(1)
        getobj.save()
     # print("\n\n", assign_id, assign_stdid, "\n\n", marks, "\n\n")
    return redirect("faculty_view_submissions")


def detailattend(request):
    facultys = request.POST.get("faculty")
    subjects = request.POST.get("subject")
    classs = request.POST.get("class")
    dates = "2022-08-20"
    print("__"*20, facultys, " ", subjects, " ",
          subjects, classs, dates, date.today())
    attendanceobj = Classes_Taken.objects.get(faculty_taken=Faculty_Subject_Class.objects.get(faculty_name=Faculty.objects.get(
        facultyname=facultys), subject_name=Subjects.objects.get(subject=subjects), class_name=Classes.objects.get(classname=classs)), taken_at=dates)
    print("__"*20, attendanceobj)
    total_students = StudentAttendance.objects.filter(
        class_taken=attendanceobj)
    totlist = []
    for i in total_students:
        print("\n", i.presentorabsent)
        totlist += [i.presentorabsent]

    return render(request, 'faculty/detailview.html', context={"total_stude": total_students, "tot_list": totlist, "attendobj": attendanceobj})
