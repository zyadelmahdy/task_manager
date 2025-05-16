from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Task

class CustomUserRegistrationForm(UserCreationForm):
    """Extended user creation form with additional fields."""
    name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # Store the name in first_name field since the default User model doesn't have 'name'
        user.first_name = self.cleaned_data['name']
        
        if commit:
            user.save()
        return user

class AuthenticationForm(AuthenticationForm):
    """Custom authentication form."""
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'due_date']
