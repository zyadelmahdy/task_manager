from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserRegistrationForm, TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
            else:
                # This branch handles if authentication failed
                form.add_error(None, "Invalid username or password.")
        # If form is invalid, errors are already populated
    else:
        form = AuthenticationForm()
    return render(request, 'task_manager_app/login.html', {'form': form})


@login_required(login_url='login')
def task_list_view(request):
    # Get all tasks for the current user without filtering by completion status
    tasks = Task.objects.filter(created_by=request.user).order_by('completed', '-created_at')
    return render(request, 'task_manager_app/tasks_list.html', {
        'tasks': tasks,
        'active_tab': 'all'
    })


@login_required(login_url='login')
def show_completed_tasks_view(request):
    tasks = Task.objects.filter(created_by=request.user, completed=True)
    return render(request, 'task_manager_app/show_completed_tasks.html', {
        'tasks': tasks,
        'active_tab': 'completed'
    })


@login_required(login_url='login')
def show_pending_tasks_view(request):
    tasks = Task.objects.filter(created_by=request.user, completed=False)
    return render(request, 'task_manager_app/show_pending_tasks.html', {
        'tasks': tasks,
        'active_tab': 'pending'
    })


@login_required(login_url='login')
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)
    return render(request, 'task_manager_app/task_detail.html', {'task': task})


@login_required(login_url='login')
def task_edit_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)
    # Add form handling here
    return render(request, 'task_manager_app/task_edit.html', {'task': task})


    # task = get_object_or_404(Task, id=task_id, created_by=request.user)
    # # Add deletion confirmation handling
    # return render(request, 'task_manager_app/task_delete.html', {'task': task})

@login_required(login_url='login')
def task_delete_view(request, task_id):
    try:
        task = get_object_or_404(Task, pk=task_id, created_by=request.user)
    except Task.DoesNotExist:
        # Handle the case where the task doesn't exist
        messages.error(request, "Task not found.")
        return redirect(reverse('tasks_list'))

    if request.method == 'POST':
        task_number = task.id  # Or any other unique identifier you want to display
        task.delete()
        messages.success(request, f"The task no. {task_number} has been deleted.")
        return redirect(reverse('tasks_list'))

    return render(request, 'task_manager_app/task_delete.html', {'task': task})


@login_required(login_url='login')
def profile_view(request):
    user = get_object_or_404(User, id=request.user.id)
    return render(request, 'task_manager_app/profile.html', {'user': user})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks_list')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'task_manager_app/register.html', {'form': form})

def index_view(request):
    return render(request, 'task_manager_app/index.html')


@login_required(login_url='login')
def add_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('tasks_list')
    else:
        form = TaskForm()
    return render(request, 'task_manager_app/add_task.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
