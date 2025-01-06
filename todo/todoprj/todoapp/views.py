from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
# Create your views here.

@login_required
def home(request):
    priority_filter = request.GET.get('priority', 'all')  # Get priority filter from URL

    if priority_filter == 'all' or not priority_filter:
        all_todos = todo.objects.filter(user=request.user)
    else:
        all_todos = todo.objects.filter(user=request.user, priority=priority_filter)
        
    if request.method == 'POST':
        task = request.POST.get('task')
        deadline = request.POST.get('deadline')  # Capture the deadline from the form
        
        # Convert the deadline string to a DateTime object
        if deadline:
            deadline = timezone.datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
        else:
            deadline = None
        priority = request.POST.get('priority')  # Get the selected priority
        # Check if the task already exists for the current user
        if todo.objects.filter(user=request.user, todo_name=task).exists():
            messages.error(request, 'Task already exists.')
            return redirect('home-page')
        
        new_todo = todo(user=request.user, todo_name=task, priority=priority,deadline=deadline)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('register')

        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Error, username already exists, User another.')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    return render(request, 'todoapp/register.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist')
            return redirect('login')


    return render(request, 'todoapp/login.html', {})

@login_required
def DeleteTask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('home-page')

@login_required
def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')


@login_required
def UpdateTask(request, task_name):
    # Get the task by task_name
    task = todo.objects.get(todo_name=task_name, user=request.user)

    if request.method == 'POST':
        # Get the updated task name from the form
        updated_task_name = request.POST.get('todo_name')
        new_deadline = request.POST.get('deadline')
        if new_deadline:
            new_deadline = timezone.datetime.strptime(new_deadline, "%Y-%m-%dT%H:%M")
        task.deadline = new_deadline
        # Update the task
        task.todo_name = updated_task_name
        task.save()

        return redirect('home-page')

    context = {
        'task': task
    }
    return render(request, 'todoapp/update_task.html', context)