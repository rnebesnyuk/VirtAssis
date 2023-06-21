from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='notes'),
    path('sort_by_done', views.sort_by_done, name='by_done'),
    path('sort_by_undone', views.sort_by_undone, name='by_undone'),
    path('sort_by_priority', views.sort_by_priority, name='by_priority'),
    path('sort_by_priority_rev', views.sort_by_priority_rev, name='by_priority_rev'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('add_note/', views.add_note, name='add_note'),
    path('detail/<int:note_id>', views.detail, name='detail'),
    path('done/<int:note_id>', views.set_done, name='set_done'),
    path('undone/<int:note_id>', views.set_undone, name='set_undone'),
    path('edit_note/<int:note_id>', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>', views.delete_note, name='delete'),
    path('search_note/', views.search_note, name='search_note'),
    path('notes_by_tag/<int:tag_id>/', views.get_notes_by_tag, name='notes_by_tag'),
]