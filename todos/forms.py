from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model  = Todo
        fields = ['title', 'description', 'priority', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter todo title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description...'
            }),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }