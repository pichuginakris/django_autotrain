import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ProjectForm, PhotoForm
from .models import Project, Photo


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            request.session['project_id'] = project.id
            return redirect('upload_photos')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


# def upload_photos(request):
#     project_id = request.session.get('project_id')
#     if not project_id:
#         return redirect('create_project')
#
#     project = Project.objects.get(id=project_id)
#
#     if request.method == 'POST':
#         folder = request.FILES.getlist('folder')
#         for file in folder:
#             photo = Photo(project=project, image=file)
#             photo.save()
#
#         return HttpResponse('Success')
#
#     return render(request, 'upload_photos.html')

def upload_photos(request):
    project_id = request.session.get('project_id')
    if not project_id:
        return redirect('create_project')

    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        folder = request.FILES.getlist('folder')
        folder_paths = request.POST.getlist('folder_paths[]')

        print(folder_paths)
        if folder:
            # Обработка папки
            folder_name = "folder.name  # Получение имени папки"
            for file in folder:
                file_path = file.temporary_file_path()

                photo = Photo(project=project, image=file, folder_name=folder_name)
                photo.save()

            return HttpResponse('Success')

    return render(request, 'upload_photos.html')

#
# def upload_photos(request):
#     project_id = request.session.get('project_id')
#     if not project_id:
#         return redirect('create_project')
#
#     project = Project.objects.get(id=project_id)
#
#     if request.method == 'POST':
#         folder = request.FILES.getlist('folder')
#         print(folder)
#         print(folder[0].name)
#         folder_path = os.path.dirname(folder[0].name)  # Получение пути к папке из имени первого файла
#         print(folder_path)
#         folder_name = os.path.basename(folder_path)  # Извлечение имени папки из пути
#         print(folder_name)
#         for file in folder:
#             photo = Photo(project=project, image=file, folder_name=folder_name)
#             photo.save()
#
#         return HttpResponse('Success')
#
#     return render(request, 'upload_photos.html')


# def show_photos(request):
#     project_id = request.session.get('project_id')
#     if not project_id:
#         return redirect('create_project')
#
#     project = Project.objects.get(id=project_id)
#     photos = project.photo_set.all()
#
#     return render(request, 'show_photos.html', {'project': project, 'photos': photos})

def show_photos(request):
    project_id = request.session.get('project_id')
    if not project_id:
        return redirect('create_project')

    project = Project.objects.get(id=project_id)

    folder_name = request.GET.get('folder_name', None)  # Получение выбранной папки из параметра запроса

    if folder_name:
        photos = project.photo_set.filter(folder_name=folder_name)
        folders = project.photo_set.values_list('folder_name', flat=True).distinct()  # Получение уникальных имен папок
    else:
        photos = project.photo_set.all()
        folders = project.photo_set.values_list('folder_name', flat=True).distinct()

    return render(request, 'show_photos.html', {'project': project, 'photos': photos, 'folders': folders})