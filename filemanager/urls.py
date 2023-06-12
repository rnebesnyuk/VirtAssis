from django.urls import path
from django.views.generic import TemplateView
from filemanager.views import upload_file, file_list, delete_file, download_file

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'),
    path('files/delete/<int:file_id>/', delete_file, name='delete_file'),
    path('files/download/<int:file_id>/', download_file, name='download_file'),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
]

