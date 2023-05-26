import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ProjectForm, PhotoForm
from .models import Project, Photo


def create_project(request):
    """
     Функция представления для создания нового проекта.

    Args:
        request (HttpRequest): Объект HTTP-запроса.

    Returns:
        HttpResponse: HTTP-ответ с отрендеренным шаблоном.

    """
    project_id = request.GET.get('project_id')
    if not project_id:
        project_id = request.session.get('project_id')
    else:
        request.session['project_id'] = project_id
    if project_id:
        project = Project.objects.get(id=project_id)
    else:
        project = None
    projects = Project.objects.all()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            request.session['project_id'] = project.id
            return redirect('upload_photos')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'project': project, 'projects': projects, 'form': form})


def upload_photos(request):
    """
    Функция представления для загрузки фотографий в проект.

    Args:
        request (HttpRequest): Объект HTTP-запроса.

    Returns:
        HttpResponse: HTTP-ответ с отрендеренным шаблоном.

    """
    project_id = request.GET.get('project_id')
    if not project_id:
        project_id = request.session.get('project_id')
    else:
        request.session['project_id'] = project_id
    if not project_id:
        return redirect('create_project')

    project = Project.objects.get(id=project_id)
    projects = Project.objects.all()

    if request.method == 'POST':
        folder = request.FILES.getlist('folder')
        # Handle folder processing
        folder_paths = request.POST.getlist('folder_paths[]')

        folder_name = os.path.dirname(folder_paths[0])
        print(folder_paths)
        if folder:
            for file in folder:
                photo = Photo(project=project, image=file, folder_name=folder_name)
                photo.save()

            return redirect('show_photos')

    return render(request, 'upload_photos.html', {'project': project, 'projects': projects})


def show_photos(request):
    """
    View function for displaying photos of a project.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.

    """
    project_id = request.GET.get('project_id')
    if not project_id:
        project_id = request.session.get('project_id')
    else:
        request.session['project_id'] = project_id
    if not project_id:
        return redirect('create_project')

    project = Project.objects.get(id=project_id)
    projects = Project.objects.all()

    folder_name = request.GET.get('folder_name', None)  # Get selected folder from query parameter

    if folder_name:
        photos = project.photo_set.filter(folder_name=folder_name)
        folders = project.photo_set.values_list('folder_name', flat=True).distinct()  # Get unique folder names
    else:
        photos = project.photo_set.all()
        folders = project.photo_set.values_list('folder_name', flat=True).distinct()

    return render(request, 'show_photos.html', {'project': project, 'projects': projects, 'photos': photos, 'folders': folders})


def projects(request):
    """
    View function for displaying all projects.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.

    """
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})


def delete_project(request):
    """
    View function for deleting a project.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response.

    """
    project_id = request.GET.get('project_id')
    # Get the project object
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        # Handle the case where the project doesn't exist
        return redirect('projects')  # Redirect to the projects page

    # Perform the deletion
    project.delete()

    return redirect('projects')  # Redirect to the projects page
