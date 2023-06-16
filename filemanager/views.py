import os

import cloudinary.uploader
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from filemanager.utils import DataMixin, menu, apps
from .models import File


@login_required
def upload_file(request):
    title = "Upload File"
    if request.method == 'POST':
        name = request.POST['name']
        file = request.FILES['file']
        category = request.POST['category']

        allowed_formats = ['pdf', 'doc', 'docx', 'rar', 'jpg', 'png', 'doc', 'zip', 'mp3', 'mp4', 'mov', 'gif', 'dmg', 'txt', 'jpeg']
        file_extension = os.path.splitext(file.name)[1][1:].lower()  # Extract the file extension from the uploaded file
        if file_extension not in allowed_formats:
            error_message = "Unsupported file format. Please try a different file."
            return render(request, 'upload_file.html', {'title': title, 'menu': menu, 'error_message': error_message})

        upload_result = cloudinary.uploader.upload(file, resource_type='raw', allowed_formats=allowed_formats)
        file_url = upload_result['secure_url']

        # Use request.user to get the current user
        File.objects.create(name=name, file=file_url, category=category, user=request.user)
        return redirect('file_list')

    return render(request, 'upload_file.html', {'title': title, 'menu': menu})


@login_required
def file_list(request):
    category = request.GET.get('category')
    user = request.user
    files = File.objects.filter(user=user).order_by('-upload_datetime')

    if category:
        files = files.filter(category=category)

    # Pagination
    paginator = Paginator(files, 4)
    page_number = request.GET.get('page')
    files = paginator.get_page(page_number)

    categories = dict(File.CATEGORIES)
    title = "File List"

    return render(request, 'file_list.html', {'files': files, 'title': title, 'menu': menu, 'apps': apps, 'cloudinary': cloudinary, 'categories': categories})


@login_required
def delete_file(request, file_id):
    file = File.objects.get(id=file_id)
    public_id = file.file.url  # Get the file URL
    cloudinary.uploader.destroy(public_id)  # Delete the file from Cloudinary
    file.delete()  # Delete the file record from the database
    return redirect('file_list')


@login_required
def download_file(request, file_id):
    file = File.objects.get(id=file_id)
    file_url = file.file
    file_extension = os.path.splitext(file.file.name)[1]  # Extract the file extension from the name
    filename = file.name + file_extension  # Add the file format to the filename
    response = HttpResponse(file_url, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response
