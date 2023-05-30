import os

from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)


def get_file_upload_path(instance, filename):
    folder_name = instance.folder_name
    return os.path.join('files', folder_name, filename)


class Photo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=255, default='unnamed')
    files = models.FileField(upload_to=get_file_upload_path)
