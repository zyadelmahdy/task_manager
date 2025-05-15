from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default="Please add a description")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title