from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title