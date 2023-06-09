import os
import yaml

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import ProjectForm
from .models import Project, Files, Classes

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

    # Если 'project_id' отсутствует в запросе, проверяем наличие его значения в сессии
    if not project_id:
        project_id = request.session.get('project_id')
    else:
        # Если 'project_id' присутствует в запросе, сохраняем его значение в сессии
        request.session['project_id'] = project_id

    if project_id:
        # Если 'project_id' задан, получаем объект проекта по 'project_id' из базы данных
        project = Project.objects.get(id=project_id)
    else:
        project = None

    # Получение всех проектов из базы данных
    projects = Project.objects.all()

    if request.method == 'POST':
        # Обработка POST-запроса при создании проекта

        form = ProjectForm(request.POST)
        if form.is_valid():
            # Если форма прошла валидацию, сохраняем проект
            project = form.save()
            # Сохраняем 'project_id' в сессии
            request.session['project_id'] = project.id
            # Перенаправление на страницу загрузки фотографий
            return redirect('upload_files')
    else:
        # Создание пустой формы для создания проекта
        form = ProjectForm()

    # Отображение страницы 'create_project.html' с передачей данных в шаблон
    return render(request, 'create_project.html', {'project': project, 'projects': projects, 'form': form})


def upload_files(request):
    """
    Функция представления для загрузки фотографий в проект.

    Args:
        request (HttpRequest): Объект HTTP-запроса.

    Returns:
        HttpResponse: HTTP-ответ с отрендеренным шаблоном.

    """
    project_id = request.GET.get('project_id')

    # Если 'project_id' отсутствует в запросе, проверяем наличие его значения в сессии
    if not project_id:
        project_id = request.session.get('project_id')
    else:
        # Если 'project_id' присутствует в запросе, сохраняем его значение в сессии
        request.session['project_id'] = project_id

    if not project_id:
        # Если значение 'project_id' не задано, перенаправляем на страницу создания проекта
        return redirect('create_project')

    # Получение объекта проекта по 'project_id' из базы данных
    project = Project.objects.get(id=project_id)
    # Получение всех проектов из базы данных
    projects = Project.objects.all()

    if request.method == 'POST':
        # Обработка POST-запроса при загрузке фотографий

        folder = request.FILES.getlist('folder')
        # Обработка папки с фотографиями
        folder_paths = request.POST.getlist('folder_paths[]')
        folder_name = os.path.dirname(folder_paths[0])
        folder_id = 0
        if folder:
            for file in folder:
                # Удаление пробелов из названия папок
                folder_name = os.path.dirname(folder_paths[folder_id].replace(' ', ''))
                print(folder_name)
                # Создание экземпляра класса 'Files' и сохранение его в базе данных
                file = Files(project=project, files=file, folder_name=folder_name)
                file.save()
                folder_id += 1
            # Сохранение выбранной папки в сессии
            request.session['selected_folder'] = folder_name
            # Перенаправление на страницу отображения фотографий
            return redirect('show_files')

    # Отображение страницы 'upload_files.html' с передачей данных в шаблон
    return render(request, 'upload_files.html', {'project': project, 'projects': projects})


def save_config_to_file(config):
    """
    Сохраняет конфигурацию в файл.

    Args:
        config (dict): Словарь с конфигурационными данными.

    Returns:
        None

    """
    config_file_path = os.path.join(os.getcwd(), 'autotrain', 'ORDC', 'ODRS', 'ODRC', 'ml_config.yaml')
    print(config_file_path)
    with open(config_file_path, 'w') as file:
        yaml.dump(config, file)


def show_files(request):
    # Получение значения параметра 'project_id' из запроса
    project_id = request.GET.get('project_id')

    selected_folder = ''
    if not project_id:
        # Если 'project_id' отсутствует в запросе, проверяем наличие его значения в сессии
        project_id = request.session.get('project_id')
        selected_folder = request.session.get('selected_folder')
    else:
        # Если 'project_id' присутствует в запросе, сохраняем его значение в сессии
        request.session['project_id'] = project_id

    if not project_id:
        # Если значение 'project_id' не задано, перенаправляем на страницу проектов
        return redirect('projects')

    # Получение объекта проекта по 'project_id'
    project = Project.objects.get(id=project_id)
    # Получение всех проектов
    projects = Project.objects.all()

    # Получение выбранной папки из параметра запроса 'folder_name'
    folder_name = request.GET.get('folder_name', None)
    # Получение уникальных имен папок, связанных с проектом
    folders = project.files_set.values_list('folder_name', flat=True).distinct()

    if folder_name:
        # Если задан параметр 'folder_name', фильтруем фотографии проекта по указанной папке
        files = project.files_set.filter(folder_name=folder_name)
        selected_folder = folder_name
    else:
        # В противном случае выводим все фотографии проекта
        files = project.files_set.all()

    # Конфигурация формы
    config = {
        'dataset_path': selected_folder,
        'classes_path': '',
        'GPU': True,
        'speed': 1,
        'accuracy': 10
    }

    if request.method == 'POST':
        # Обработка POST-запроса при отправке формы

        # Получение значения параметра 'GPU' из POST-запроса
        print(request.POST.get('GPU'))
        # Получение значения параметра 'folder_name' из POST-запроса
        folder_name = request.POST.get('folder_name')
        # Получение файла из POST-запроса
        file = request.FILES.get('file')
        print(file)
        # Создание экземпляра класса Classes и сохранение его в базу данных
        classes_instance = Classes(project=project, files_classes=file, folder_name=folder_name)
        classes_instance.save()

        # Обновление значений в конфигурации
        config['dataset_path'] = os.path.join(settings.MEDIA_ROOT, 'files', folder_name)
        config['classes_path'] = os.path.join(settings.MEDIA_ROOT, 'classes', folder_name, str(file))

        if request.POST.get('GPU') == 'on':
            config['GPU'] = True
        else:
            config['GPU'] = False

        config['speed'] = int(request.POST.get('speed'))
        config['accuracy'] = int(request.POST.get('accuracy'))
        config['models_array'] = ["yolov5l", "yolov5m", "yolov5n", "yolov5s", "yolov5x",
                                  "yolov7x", "yolov7", "yolov7-tiny", "yolov8x6", "yolov8x",
                                  "yolov8s", "yolov8n", "yolov8m"]

        # Сохранение конфигурации в файл
        save_config_to_file(config)

        # Запуск основной функции main()
        result = main()

        # Отображение страницы результатов с передачей результата в шаблон
        return render(request, 'results.html', {'result': result})

    # Отображение страницы show_files.html с передачей данных в шаблон
    return render(request, 'show_files.html', {
        'project': project,
        'projects': projects,
        'files': files,
        'folders': folders,
        'selected_folder': selected_folder,
        'config': config,
    })


def projects(request):
    """
    Представление для отображения всех проектов

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.

    """
    project_id = request.GET.get('project_id')

    if not project_id:
        # Если 'project_id' отсутствует в запросе, проверяем наличие его значения в сессии
        project_id = request.session.get('project_id')
    else:
        # Если 'project_id' присутствует в запросе, сохраняем его значение в сессии
        request.session['project_id'] = project_id
    if project_id:
        project = Project.objects.get(id=project_id)
    else:
        project = None
    projects = Project.objects.all()
    return render(request, 'projects.html', {'project': project, 'projects': projects})


def delete_project(request):
    """
    Функция для удаления проекта.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response.

    """
    project_id = request.GET.get('project_id')
    # Получение объекта проекта
    try:
        project = Project.objects.get(id=project_id)
    # Обработка случая, когда проект не существует
    except Project.DoesNotExist:
        return redirect('projects')  # Перенаправление на страницу проектов

    # Выполнение удаления
    project.delete()

    return redirect('projects')  # Перенаправление на страницу проектов
