from django.urls import path
from django.views.generic import TemplateView
from filemanager.views import upload_file, file_list, delete_file, download_file

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('list/', file_list, name='file_list'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
    path('download/<int:file_id>/', download_file, name='download_file'),
]

