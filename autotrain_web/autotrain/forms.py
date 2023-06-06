from django import forms
from .models import Project

from .models import Classes


class ClassesForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ('project', 'folder_name', 'files_classes')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']


class PhotoForm(forms.Form):
    folder = forms.FileField()


class ConfigForm(forms.Form):
    dataset_path = forms.CharField(label='Dataset Path')
    classes_path = forms.CharField(label='Classes Path')
    GPU = forms.BooleanField(label='GPU')
    speed = forms.IntegerField(label='Speed', min_value=1, max_value=5)
    accuracy = forms.IntegerField(label='Accuracy', min_value=1, max_value=10)