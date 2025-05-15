"""
URL configuration for task_manager_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task_manager_app import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/', views.task_list_view, name='tasks_list'),
    path('tasks/show_pending_tasks/', views.show_pending_tasks_view, name='show_pending_tasks'),
    path('tasks/show_completed_tasks/', views.show_completed_tasks_view, name='show_completed_tasks'),
    path('tasks/<int:task_id>/', views.task_detail_view, name='task_detail'),
    path('tasks/<int:task_id>/edit/', views.task_edit_view, name='task_edit'),
    path('tasks/<int:task_id>/delete/', views.task_delete_view, name='task_delete'),
    path('tasks/<int:task_id>/move_to_pending/', views.move_to_pending_view, name='move_to_pending'),
    path('tasks/<int:task_id>/move_to_completed/', views.move_to_completed_view, name='move_to_completed'),
    path('add_task/', views.add_task_view, name='add_task'),
]