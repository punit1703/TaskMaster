from django import forms
from django.forms import ModelForm
from .models import Task

class TodoForm(ModelForm):
    category = forms.CharField(
        label='Category',
        widget=forms.TextInput(attrs={
            'list': 'category-list',
            'class': 'mt-2 block w-full rounded-md border border-gray-300 px-4 py-2 text-base text-gray-700 shadow-sm  focus:outline-none focus:ring-1 focus:ring-black',
            'placeholder': 'Select or type a category',
        })
    )

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-2 block w-full rounded-md border border-gray-300 px-4 py-2 text-base text-gray-900 shadow-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-black',
                'placeholder': 'Enter title'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'mt-2 block w-full rounded-md border border-gray-300 px-4 py-2 text-base text-gray-900 shadow-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-black',
                'placeholder': 'Enter description'
            }),
            'category': forms.Select(attrs={
                'class': 'mt-2 block w-full rounded-md border border-gray-300 px-4 py-2 text-base text-gray-700 shadow-sm  focus:outline-none focus:ring-1 focus:ring-black',
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-2 block w-full rounded-md border border-gray-300 px-4 py-2 text-base text-gray-900 shadow-sm  focus:outline-none focus:ring-1 focus:ring-black',
            }),
            'priority': forms.Select(choices=[
                ('low', 'Low'),
                ('medium', 'Medium'),
                ('high', 'High')
            ], attrs={
                'class': 'mt-2 block w-full rounded-md border border-gray-300 px-4 py-2 text-base text-gray-700 shadow-sm  focus:outline-none focus:ring-1 focus:ring-black',
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'text-green-600',
            }),
        }