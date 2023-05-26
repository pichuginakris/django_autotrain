from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']


class PhotoForm(forms.Form):
    folder = forms.FileField()