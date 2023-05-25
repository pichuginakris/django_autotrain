from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)


class Photo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    folder_name = models.CharField(max_length=255)
