from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

# Uncomment and fix this when you need the NoteForm
# class NoteForm(forms.ModelForm):
#     class Meta:
#         model = Note  # This should be your Note model, not User
#         fields = ['title', 'content', 'due_date']  # Use actual Note model fields