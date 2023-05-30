import os
import yaml

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import ProjectForm, ConfigForm
from .models import Project, Photo

from .ORDC.ODRS.ODRC.ml_model_optimizer import main


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
        folder_id = 0
        if folder:
            for file in folder:
                folder_name = os.path.dirname(folder_paths[folder_id].replace(' ', ''))
                print(folder_name)
                photo = Photo(project=project, files=file, folder_name=folder_name)
                photo.save()
                folder_id += 1
            request.session['selected_folder'] = folder_name
            return redirect('show_photos')

    return render(request, 'upload_photos.html', {'project': project, 'projects': projects})


def save_config_to_file(config):
    config_file_path = os.path.join(os.getcwd(), 'autotrain', 'ORDC', 'ODRS', 'ODRC', 'ml_config.yaml')
    print(config_file_path)
    with open(config_file_path,
              'w') as file:
        yaml.dump(config, file)


def show_photos(request):
    project_id = request.GET.get('project_id')

    selected_folder = ''
    if not project_id:
        project_id = request.session.get('project_id')
        selected_folder = request.session.get('selected_folder')
    else:
        request.session['project_id'] = project_id
    if not project_id:
        return redirect('projects')

    project = Project.objects.get(id=project_id)
    projects = Project.objects.all()

    folder_name = request.GET.get('folder_name', None)  # Get selected folder from query parameter
    folders = project.photo_set.values_list('folder_name', flat=True).distinct()  # Get unique folder names
    if folder_name:
        photos = project.photo_set.filter(folder_name=folder_name)
        selected_folder = folder_name
    else:
        photos = project.photo_set.all()

    # Configuration form
    config = {
        'dataset_path': selected_folder,
        'classes_path': '',
        'GPU': True,
        'speed': 1,
        'accuracy': 10
    }

    if request.method == 'POST':
        config['dataset_path'] = os.path.join(settings.MEDIA_ROOT, 'files', request.POST.get('folder_name'))
        config['classes_path'] = os.path.join(settings.MEDIA_ROOT, 'files', request.POST.get('classes_folder_name'), 'classes_aer.txt')
        config['GPU'] = True
        config['speed'] = int(request.POST.get('speed'))
        config['accuracy'] = int(request.POST.get('accuracy'))
        config['models_array'] = ["yolov5l", "yolov5m", "yolov5n", "yolov5s", "yolov5x",
                       "yolov7x", "yolov7", "yolov7-tiny", "yolov8x6", "yolov8x",
                       "yolov8s", "yolov8n", "yolov8m"]
        save_config_to_file(config)
        result = main()
        print(result)
        return render(request, 'results.html', {'result': result})

    return render(request, 'show_photos.html', {
        'project': project,
        'projects': projects,
        'photos': photos,
        'folders': folders,
        'selected_folder': selected_folder,
        'config': config,

    })


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


def config_page(request):
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            # Чтение данных из формы
            dataset_path = form.cleaned_data['dataset_path']
            classes_path = form.cleaned_data['classes_path']
            GPU = form.cleaned_data['GPU']
            speed = form.cleaned_data['speed']
            accuracy = form.cleaned_data['accuracy']

            # Запись данных в YAML-файл
            config_data = {
                'dataset_path': dataset_path,
                'classes_path': classes_path,
                'GPU': GPU,
                'speed': speed,
                'accuracy': accuracy
            }

            with open('config.yaml', 'w') as file:
                yaml.dump(config_data, file)

            return redirect('projects')
    else:
        form = ConfigForm()

    return render(request, 'config.html', {'form': form})
