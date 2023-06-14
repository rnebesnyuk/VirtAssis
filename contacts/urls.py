from django.urls import path, include

from .views import *


urlpatterns = [
    path('', ContactsHome.as_view(), name='home'),
    path('add_contact/', AddContact.as_view(), name='add_contact'),
    path('show_bdays/', ContactsBirthday.as_view(), name='show_bdays'),
    path('contact/delete/<int:pk>', ContactDelete.as_view(), name='contact_delete'),
    path('contact/edit/<int:pk>', ContactUpdate.as_view(), name='contact_edit'),
    path('export/', export_contacts, name='export_contacts'),
    path('import/',import_contacts, name='import_contacts'),
    path('search/', SearchContacts.as_view(), name='search')
]