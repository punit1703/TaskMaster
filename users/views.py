from todo.models import Task
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def userProfile(request, pk):
    tasks_count = Task.objects.filter(user = request.user).count()
    completed_count = Task.objects.filter(user = request.user, is_completed=True).count()
    not_completed = tasks_count  - completed_count
    context = {
        'tasks_count': tasks_count, 
        'completed_count':completed_count,
        'not_completed': not_completed,
    }
    return render(request,'registration/profile.html', context)

def loginPage(request):
    error = False

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = True

    context = {'page': 'login', 'error': error}
    return render(request, 'registration/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')

    return render(request, 'registration/register.html')
