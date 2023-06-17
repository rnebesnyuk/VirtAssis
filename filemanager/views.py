import os

import cloudinary.uploader
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from filemanager.utils import menu, apps
from .models import File


@login_required
def upload_file(request):
    title = "Upload File"
    if request.method == 'POST':
        name = request.POST['name']
        file = request.FILES['file']
        category = request.POST['category']

        # Define allowed formats for each category
        allowed_formats = {
            'images': ['jpg', 'jpeg', 'png', 'gif'],
            'documents': ['pdf', 'doc', 'docx', 'txt'],
            'videos': ['mp4', 'mov'],
        }

        # Get the file extension from the uploaded file
        file_extension = os.path.splitext(file.name)[1][1:].lower()

        if category in allowed_formats:
            # Check if the file format is allowed for the selected category
            if file_extension not in allowed_formats[category]:
                error_message = f"Unsupported file format for the '{category}' category. Please try a different file."
                return render(request, 'upload_file.html', {'title': title, 'menu': menu, 'error_message': error_message})
        else:
            # For the "others" category, allow all file formats
            allowed_formats['others'] = []

        upload_result = cloudinary.uploader.upload(file, resource_type='raw')
        file_url = upload_result['secure_url']

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
