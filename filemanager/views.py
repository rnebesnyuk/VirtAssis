import os

import cloudinary.uploader
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from filemanager.utils import DataMixin, menu, apps
from .models import File


@login_required
def upload_file(request):
    title = "Upload File"
    if request.method == 'POST':
        name = request.POST['name']
        file = request.FILES['file']
        category = request.POST['category']

        allowed_formats = ['pdf', 'doc', 'csv', 'docx', 'rar', 'jpg', 'png', 'doc', 'zip', 'mp3', 'mp4', 'mov', 'gif', 'dmg', 'txt', 'jpeg']
        file_extension = os.path.splitext(file.name)[1][1:].lower()  # Extract the file extension from the uploaded file
        if file_extension not in allowed_formats:
            error_message = "Unsupported file format. Please try a different file."
            return render(request, 'upload_file.html', {'title': title, 'menu': menu, 'error_message': error_message})
        try:
            upload_result = cloudinary.uploader.upload(file, resource_type='raw', allowed_formats=allowed_formats)
            file_url = upload_result['secure_url']
            File.objects.create(name=name, file=file_url, category=category, user=request.user)
            return redirect('file_list')
        except Exception as e:
            error_message = {e}
            return render(request, 'upload_file.html', {'title': title, 'menu': menu, 'error_message': error_message})
        
    return render(request, 'upload_file.html', {'title': title, 'menu': menu})


@login_required
def file_list(request):
    category = request.GET.get('category')
    files = File.objects.filter(user=request.user).order_by('-upload_datetime')

    if category:
        files = files.filter(category=category)

    # Pagination
    paginator = Paginator(files, 6)
    page_number = request.GET.get('page')
    files = paginator.get_page(page_number)

    categories = dict(File.CATEGORIES)
    title = "File List"

    return render(request, 'file_list.html', {'files': files, 'title': title, 'menu': menu, 'apps': apps, 'cloudinary': cloudinary, 'categories': categories})


@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)
    public_id = file.file.url
    cloudinary.uploader.destroy(public_id)
    file.delete()
    return redirect('file_list')


@login_required
def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)
    file_url = file.file
    file_extension = os.path.splitext(file.file.name)[1]
    filename = file.name + file_extension
    response = HttpResponse(file_url, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response
