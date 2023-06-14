from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import File
import cloudinary.uploader
from django.http import HttpResponse


def upload_file(request):
    if request.method == 'POST':
        name = request.POST['name']
        file = request.FILES['file']
        category = request.POST['category']

        allowed_formats = ['pdf', 'doc', 'docx', 'rar', 'jpg', 'png', 'doc', 'zip', 'mp3', 'mp4', 'mov', 'gif']
        upload_result = cloudinary.uploader.upload(file, resource_type='raw', allowed_formats=allowed_formats)
        file_url = upload_result['secure_url']

        File.objects.create(name=name, file=file_url, category=category)
        return redirect('file_list')

    return render(request, 'upload_file.html')


def file_list(request):
    category = request.GET.get('category')
    files = File.objects.all().order_by('-upload_datetime')

    if category:
        files = files.filter(category=category)

    # Pagination
    paginator = Paginator(files, 4)
    page_number = request.GET.get('page')
    files = paginator.get_page(page_number)

    categories = dict(File.CATEGORIES)

    return render(request, 'file_list.html', {'files': files, 'cloudinary': cloudinary, 'categories': categories})


def delete_file(request, file_id):
    file = File.objects.get(id=file_id)
    public_id = file.file.url  # Get the file URL
    cloudinary.uploader.destroy(public_id)  # Delete the file from Cloudinary
    file.delete()  # Delete the file record from the database
    return redirect('file_list')


def download_file(request, file_id):
    file = File.objects.get(id=file_id)
    response = HttpResponse(file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.name)
    return response
