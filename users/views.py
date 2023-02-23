from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth import get_user_model
User = get_user_model()


def register(request):
    if request.method == 'POST':
        user_status = request.POST.get('user_config')
        user_ids = request.POST.get('user_id')
        username = user_ids
        first_name = request.POST.get('user_firstname')
        last_name = request.POST.get('user_lastname')
        email = request.POST.get('email')
        dateofbirth = request.POST.get('user_dob')
        sex = request.POST.get('user_sex')
        password = request.POST.get('password')

        variable = User.objects.filter(username=username)
        if(len(list(variable)) == 0):
            user = User.objects.create_user(
                username=username, email=email, password=password, user_status=user_status, user_id=user_ids, first_name=first_name, last_name=last_name, birth_date=dateofbirth, sex=sex)
            user.save()
            return redirect('login')
        else:
            return render(request, 'users/register.html', context={
                'errorcame': 1,
            })
    return render(request, 'users/register.html', context={'errorcame': 0})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            obj = User.objects.get(username=username)
            if obj.user_status == "student":
                return redirect('student_dashboard')
            elif(obj.user_status == "faculty"):
                return redirect('faculty_dashboard')
        else:
            return render(request, 'users/login.html', context={'errorlogin': 1})

    return render(request, 'users/login.html', context={'errorlogin': 0})


def logout_view(request):
    logout(request)
    return redirect('login')
