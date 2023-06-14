import csv
from datetime import date, timedelta, datetime

from django import forms
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator


from .utils import DataMixin
from .models import *
from .forms import AddContactForm, AddPhoneForm, AddEmailForm, ContactImportForm


class ContactsHome(DataMixin, ListView):
    model = Contact
    template_name = "contacts/index.html"
    context_object_name = "contacts"


    class DaysForm(forms.Form):
            days = forms.IntegerField(label='Number of Days')

    def get_context_data(self, *, object_list=None, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)
        form = self.DaysForm(request.GET)
        days = request.GET.get('days') or 7
    
        c_def = self.get_user_context(
            title="Contacts",
        )

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Contact.objects.all()
    

class ContactsBirthday(DataMixin, ListView):
    model = Contact
    template_name = "contacts/upcoming_birthdays.html"
    context_object_name = 'contacts'

    class DaysForm(forms.Form):
            days = forms.IntegerField(label='')

    def get_context_data(self, *, object_list=None, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)        

        form = self.DaysForm(request.GET or None)
        days = request.GET.get('days') or 7

        today = date.today()
        end_date = today + timedelta(days=int(days))
        start_date = today

        verified_contacts = []
        contacts = Contact.objects.all()
        for c in contacts:
            if c.birthdate:
                start_date = start_date.replace(year=c.birthdate.year)
                end_date = end_date.replace(year=c.birthdate.year)
                if c.birthdate.month >= start_date.month and c.birthdate.day >= start_date.day and c.birthdate.month <= end_date.month and c.birthdate.day <= end_date.day:
                    verified_contacts.append(c)

        c_def = self.get_user_context(
            title="Birthdays",
        ) 
        context['form'] = form
        context["contacts"] = verified_contacts

        return dict(list(context.items()) + list(c_def.items()))
    

class AddContact(DataMixin, CreateView):
    template_name = "contacts/add_contact.html"
    success_url = reverse_lazy("home")
    login_url = "/admin/"
    raise_exception = True
    form_classes = {"contact_form": AddContactForm, "phone_number_form": AddPhoneForm, "email_form": AddEmailForm}

    def get(self, request, *args, **kwargs):
        self.object = None
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = None
        return self.form_valid(self.get_form())

    def get_form(self):
        forms = {}
        for key, form_class in self.form_classes.items():
            forms[key] = form_class(**self.get_form_kwargs())
        return forms

    def form_valid(self, forms):
        self.object = forms['contact_form'].save()

        # Perform additional logic for the phone form
        phone_form = forms['phone_number_form']
        if phone_form.is_valid():
            phone_instance = phone_form.save(commit=False)
            phone_instance.contact = self.object
            phone_instance.save()
        email_form = forms['email_form']
        if email_form.is_valid():
            email_instance = email_form.save(commit=False)
            email_instance.contact = self.object
            email_instance.save()
        
        full_name = f"{forms['contact_form'].cleaned_data['first_name']} {forms['contact_form'].cleaned_data['last_name']}"
        messages.success(self.request, f"Contact {full_name} was added!")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add Contact")
        context.update({'forms': self.get_form()})
        return dict(list(context.items()) + list(c_def.items()))


class ContactDelete(DataMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('home')
    template_name = 'contacts/contact_delete.html'

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.success(self.request, f"Contact was deleted!")
        c_def = self.get_user_context(title="Delete contact")
        return dict(list(context.items()) + list(c_def.items()))
    

class ContactUpdate(DataMixin, UpdateView):
    model = Contact
    fields = ['first_name', 'last_name', 'birthdate', 'address', 'photo']
    template_name = 'contacts/contact_edit.html'
    success_url = reverse_lazy('home')


    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
        
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.success(self.request, f"Contact was updated successfully!")
        c_def = self.get_user_context(title="Edit contact")
        return dict(list(context.items()) + list(c_def.items()))
    

def export_contacts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)
    writer.writerow(['FirstName', 'LastName', 'Birthdate', 'Gender', 'Address', 'Phone', 'Email'])

    contacts = Contact.objects.all()
    for contact in contacts:
        phone = contact.phones.first()
        email = contact.emails.first()
        writer.writerow([contact.first_name, contact.last_name, contact.birthdate, contact.gender, contact.address, phone, email])

    return response

    
def import_contacts(request):
    if request.method == 'POST':
        form = ContactImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
                reader = csv.reader(csv_file.read().decode('utf-8').splitlines())

                for row in reader:
                    name1 = row[0]
                    name2 = row[1]
                    birthdate = row[2]
                    gender = row[3]
                    address = row[4]
                    # phone = row[5]
                    # email = row[6]
                    Contact.objects.create(first_name=name1, last_name=name2, birthdate=birthdate, gender=gender, address=address)

                return render(request, 'contacts/import_success.html')
            except Exception as e:
                messages.success(request, f"Error {e} happened. Try again.")
                print(e)
    else:
        form = ContactImportForm()

    return render(request, 'contacts/import.html', {'form': form})


class SearchContacts(DataMixin, ListView):
    model = Contact
    template_name = 'contacts/search_contacts.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(address__icontains=search_query))
        return queryset
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Search")
        context.update({'contacts': self.get_queryset()})
        return dict(list(context.items()) + list(c_def.items()))