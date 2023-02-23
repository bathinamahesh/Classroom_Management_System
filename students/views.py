from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from faculty.models import messages, Assignments
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages as msg
from students.models import Submissions
from users.models import Classes, Student, Student_Class, Faculty_Subject_Class, Faculty

from django import template

register = template.Library()


@register.filter(name='index')
def index(sequence, position):
    return sequence[position]


User = get_user_model()


@login_required
def home_page(request):
    return render(request, 'student/student_main.html')


@login_required
def dash_board(request):
    return render(request, 'student/student_dashboard.html')


@login_required
def std_inbox(request):
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
    return render(request, 'student/student_inbox.html', context={"inboxmsg": inboxmsg})


@login_required
def std_profile(request):
    if request.method == 'POST':
        curruser = request.user.username
        data = User.objects.get(user_id=curruser)
        return render(request, 'faculty/faculty_profile_update.html', context={"userprofile": data})
    curruser = request.user.username
    data = User.objects.get(user_id=curruser)
    return render(request, 'student/student_profile.html', context={"basicdata": data})


@login_required
def std_profile_update(request):
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
            profile_edited = 1
            return redirect('student_profile')
        except Exception as e:
            print("______"*30, "Error While Saving", e)

    curr = request.user.username
    data = User.objects.get(user_id=curr)
    return render(request, 'student/student_profile_update.html', context={"userprofile": data})


@ login_required
def std_marks(request):
    return render(request, 'student/student_marks.html')


@ login_required
def std_assignments(request):
    submitted = []
    marksassign = []
    user = request.user.user_id
    student = Student_Class.objects.get(student_id=Student(
        studentname=User.objects.get(user_id=user)))
    student_class = student.class_name
    l = Assignments.objects.filter(
        assignment_class=student_class)
    for i in l:
        asdet = i
        print("\n\n", asdet)
        try:
            new = Submissions.objects.get(student_id=User.objects.get(
                user_id=request.user.user_id), assignment_detail=i)
            submitted += [1]
            if new.givenmarks is None:
                marksassign += ["-"]
            else:
                marksassign += [new.givenmarks]
        except Exception as e:
            marksassign += ["-"]
            submitted += [0]
    print("\n\n", submitted, "\n\n")
    return render(request, 'student/student_assignments.html', context={"assignments": l, "submittedlist": submitted, "marksgiven": marksassign})


@ login_required
def teachers_list(request):
    user = request.user.user_id
    student = Student_Class.objects.get(student_id=Student(
        studentname=User.objects.get(user_id=user)))
    student_class = student.class_name
    tot_teachers = Faculty_Subject_Class.objects.filter(
        class_name=student_class)
    return render(request, 'student/student_teachers_list.html', context={"tot_teachers": tot_teachers})


@ login_required
def std_message(request):
    std = request.user.user_id
    std_class = (Student_Class.objects.get(
        student_id=Student.objects.get(studentname=std))).class_name
    faculty = Faculty_Subject_Class.objects.filter(
        class_name=Classes.objects.get(classname=std_class))
    if request.method == 'POST':
        userid = request.user.user_id
        username = request.user.first_name
        #msgtitle = request.POST.get("msg-title")
        msgto = request.POST.get("msg-faculty")
        msg = request.POST.get("msg-desc")
        objmsg = messages(sender=userid, receive=msgto,
                          sender_name=username, sendmessage=msg,)
        objmsg.save()
        return render(request, 'student/student_message.html', context={"totfaculty": faculty, "msgsuccess": 1})

    return render(request, 'student/student_message.html', context={"totfaculty": faculty, "msgsuccess": 0})


@ login_required
def std_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            msg.success(
                request, 'Your password was successfully updated!')
            return render(request, 'student/student_dashboard.html', {
                'form': form, "passwordchanged": 1
            })
        else:
            return render(request, 'student/student_change_password.html', {'form': form, "errorinchange": 1})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'student/student_change_password.html', {
        'form': form
    })


@ login_required
def std_notice(request):
    return render(request, 'student/student_notice.html')


def file_upload(request, assign_id):
    if "uploadfile" in request.FILES:
        userid = User.objects.get(user_id=request.user.user_id)
        assignobj = Assignments.objects.get(assignment_id=assign_id)
        facult = assignobj.assignment_faculty.facultyname
        print("__"*20, facult)
        filesubmit = request.FILES['uploadfile']
        issubmitted = 1
        uploadingobj = Submissions(assignment_detail=assignobj, student_id=userid,
                                   file_submit=filesubmit, is_submitted=issubmitted, faculty=facult)
        uploadingobj.save()
        print("\n\nFile came\n")
    print("__"*20, "function_called", assign_id)
    return redirect('student_assignments')
