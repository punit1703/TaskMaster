from django.forms import ModelForm
from .models import Task

class TodoForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['user', 'is_completed']

# class TodoUpdateForm(ModelForm):
#     class Meta:
#         model = Task
#         fields = '__all__'
#         exclude = ['user','is_completed','']