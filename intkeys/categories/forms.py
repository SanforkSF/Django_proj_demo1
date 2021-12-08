from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter slug'})
        }
