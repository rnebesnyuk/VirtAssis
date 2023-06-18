from django.urls import path, include

from .views import *


urlpatterns = [
    path('', ContactsHome.as_view(), name='home'),
    path('add_contact/', create_contact, name='add_contact'),
    path('show_bdays/', ContactsBirthday.as_view(), name='show_bdays'),
    path('contact/delete/<slug:slug>', ContactDelete.as_view(), name='contact_delete'),
    path('contact/edit/<slug:slug>', personal_info_update, name='personal_info_edit'),
    path('contact/phone/edit/<slug:contact_slug>', phone_update, name='phone_edit'),
    path('contact/email/edit/<slug:contact_slug>', email_update, name='email_edit'),
    path('export/', export_contacts, name='export_contacts'),
    path('import/',import_contacts, name='import_contacts'),
    path('search/', SearchContacts.as_view(), name='search')
]