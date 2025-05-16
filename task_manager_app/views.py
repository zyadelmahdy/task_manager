from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserRegistrationForm, TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator



def get_user_task_or_redirect(request, task_id):
    try:
        task = get_object_or_404(Task, pk=task_id, created_by=request.user)
        return task
    except Task.DoesNotExist:
        messages.error(request, "Task not found.")
        return redirect(reverse('tasks_list'))


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tasks_list')
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
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'task_manager_app/tasks_list.html', {
        'tasks': tasks,
        'active_tab': 'all',
        'page_obj': page_obj,
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
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            # Preserve the task owner and creation time
            task.created_by = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' has been updated successfully!")
            return redirect('task_detail', task_id=task.id)
    else:
        # For GET request, initialize form with existing task data
        form = TaskForm(instance=task)
    
    return render(request, 'task_manager_app/task_edit.html', {'form': form, 'task': task})

@login_required(login_url='login')
def task_delete_view(request, task_id):
    task = get_user_task_or_redirect(request, task_id)

    if request.method == 'POST':
        task_number = task.id  # Or any other unique identifier you want to display
        task.delete()
        messages.success(request, f"The task no. {task_number} has been deleted.")
        return redirect(reverse('tasks_list'))

    return render(request, 'task_manager_app/task_delete.html', {'task': task})


@login_required(login_url='login')    
def move_to_pending_view(request, task_id):
    task = get_user_task_or_redirect(request, task_id)
    
    if request.method == 'POST':
        task_number = task.id
        task.completed = False
        task.save()
        messages.success(request, f"Task {task_number} moved to pending successfully!")
        return redirect(reverse('tasks_list'))
    
    return render(request, 'task_manager_app/move_to_pending.html', {'task': task})

@login_required(login_url='login')
def move_to_completed_view(request, task_id):
    try:
        task = get_object_or_404(Task, pk=task_id, created_by=request.user)
    except Task.DoesNotExist:
        # Handle the case where the task doesn't exist
        messages.error(request, "Task not found.")
        return redirect(reverse('tasks_list'))

    if request.method == 'POST':
        task_number = task.id
        task.completed = True
        task.save()
        messages.success(request, f"Task {task_number} moved to completed successfully!")
        return redirect(reverse('tasks_list'))
    
    return render(request, 'task_manager_app/move_to_completed.html', {'task': task})


@login_required(login_url='login')
def profile_view(request):
    user = get_object_or_404(User, id=request.user.id)
    completed_tasks = Task.objects.filter(created_by=user, completed=True)
    pending_tasks = Task.objects.filter(created_by=user, completed=False)
    total_tasks_count = completed_tasks.count() + pending_tasks.count()
    completed_tasks_count = completed_tasks.count()
    pending_tasks_count = pending_tasks.count()
    return render(request, 'task_manager_app/profile.html', {'user': user,
        'total_tasks': total_tasks_count,
        'completed_tasks_count': completed_tasks_count,
        'pending_tasks_count': pending_tasks_count})

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
            task.completed = False
            task.save()
            messages.success(request, "Task added successfully!")
            return redirect('tasks_list')
    else:
        form = TaskForm()
    return render(request, 'task_manager_app/add_task.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
