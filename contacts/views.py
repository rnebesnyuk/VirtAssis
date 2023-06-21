import csv
import re
from datetime import date, timedelta, datetime

from dateutil.parser import parse
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.core.exceptions import ValidationError


from .utils import DataMixin, menu, apps
from .models import *
from .forms import *


class ContactsHome(LoginRequiredMixin, DataMixin, ListView):
    model = Contact
    template_name = "contacts/index.html"
    context_object_name = "contacts"

    class DaysForm(forms.Form):
        days = forms.IntegerField(label="Number of Days")

    def get_context_data(self, *, object_list=None, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)
        form = self.DaysForm(request.GET)
        days = request.GET.get("days") or 7

        c_def = self.get_user_context(
            title="Contacts",
        )

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(user_id=user.id)


class ContactsBirthday(LoginRequiredMixin, DataMixin, ListView):
    model = Contact
    template_name = "contacts/upcoming_birthdays.html"
    context_object_name = "contacts"

    class DaysForm(forms.Form):
        days = forms.IntegerField(label="")

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(user=user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)

        form = self.DaysForm(request.GET or None)
        days = request.GET.get("days") or 7

        today = date.today()
        end_date = today + timedelta(days=int(days))
        start_date = today

        verified_contacts = []
        contacts = self.get_queryset()
        for c in contacts:
            if c.birthdate:
                contact_birthdate = c.birthdate.date()
                contact_birthdate = contact_birthdate.replace(year=today.year)
                if start_date <= contact_birthdate <= end_date:
                    verified_contacts.append(c)

        c_def = self.get_user_context(
            title="Birthdays",
        )
        context["form"] = form
        context["contacts"] = verified_contacts

        return dict(list(context.items()) + list(c_def.items()))

def validate_phone_number(phone_number):
    phone_number = phone_number
    
    if len(phone_number) not in range(10, 13): 
        return False
    
    if not phone_number.isdigit():
        return False
    
    return True

@login_required
def create_contact(request):
    if request.method == "POST":
        contact_form = AddContactForm(request.POST, request.FILES, prefix="contact")
        phone_number_forms = [
            AddPhoneForm(request.POST, prefix=f"phone_{i}") for i in range(0, 2)
        ]
        email_form = AddEmailForm(request.POST, prefix="email")

        context = {
        "contact_form": contact_form,
        "phone_number_forms": phone_number_forms,
        "email_form": email_form,
        "menu": menu,
        "apps": apps,
        "title": "Add Contact",
    }

        if (
            contact_form.is_valid()
            and email_form.is_valid()
            and all(form.is_valid() for form in phone_number_forms)
        ):
            contact = contact_form.save(commit=False)
            contact.user_id = request.user.id if request.user.is_authenticated else None

            
            existing_contacts = Contact.objects.filter(user_id=request.user.id).all()
            similar_contacts = []
            for _ in existing_contacts:
                clean_last_name = _.last_name.split("(")
                
                if contact_form.cleaned_data['first_name'] == _.first_name and contact_form.cleaned_data['last_name'] == clean_last_name[0].strip():
                    similar_contacts.append(_)
            if similar_contacts:
                contact.last_name = f"{contact_form.cleaned_data['last_name']} ({len(similar_contacts)})"
            
            contact.save()

            email = email_form.save(commit=False)
            email.contact = contact
            email.save()

            for form in phone_number_forms:
                if form.cleaned_data['phone'] != '':
                    phone_number = form.save(commit=False)
                    phone_number.contact = contact
                    if phone_number:
                        if not validate_phone_number(phone_number.phone):
                            form.add_error('phone', 'Invalid phone number')
                            context = {
            "contact_form": contact_form,
            "phone_number_forms": phone_number_forms,
            "email_form": email_form,
            "menu": menu,
            "apps": apps,
            "title": "Add Contact",
        }

                            return render(request, "contacts/add_contact.html", context)
                        
                        phone_number.save()
                        
            full_name = f"{contact_form.cleaned_data['first_name']} {contact_form.cleaned_data['last_name']}"
            messages.success(request, f"Contact {full_name} was added!")
            return redirect("home")
    else:
        contact_form = AddContactForm(prefix="contact")
        phone_number_forms = [AddPhoneForm(prefix=f"phone_{i}") for i in range(0, 2)]
        email_form = AddEmailForm(request.POST, prefix="email")

    context = {
        "contact_form": contact_form,
        "phone_number_forms": phone_number_forms,
        "email_form": email_form,
        "menu": menu,
        "apps": apps,
        "title": "Add Contact",
    }
    return render(request, "contacts/add_contact.html", context)


class ContactDelete(LoginRequiredMixin, DataMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy("home")
    template_name = "contacts/contact_delete.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise Http404("Contact does not exist.")
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Contact was deleted!")
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Delete contact")
        return dict(list(context.items()) + list(c_def.items()))


@login_required
def personal_info_update(request, slug):
    contact = Contact.objects.get(slug=slug)

    if request.method == "POST":
        form = AddContactForm(request.POST, request.FILES, instance=contact)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"{contact.first_name}'s personal information was updated successfully!",
            )
            return redirect("home")
    else:
        form = AddContactForm(instance=contact)

    context = {
        "contact": contact,
        "form": form,
        "title": "Edit Contact's info",
        "menu": menu,
    }

    return render(request, "contacts/contact_edit.html", context)


@login_required
def phone_update(request, contact_slug):
    contact = Contact.objects.get(slug=contact_slug)
    FormSet = forms.inlineformset_factory(
        Contact, PhoneNumber, form=AddPhoneForm, formset=PhoneFormSet, extra=1, can_delete=True
    )

    if request.method == "POST":
        phone_formset = FormSet(request.POST, instance=contact, prefix="phone")

        context = {
            "contact": contact,
            "phone_formset": phone_formset,
            "menu": menu,
            "apps": apps,
            "title": "Add Contact",
    }

        if phone_formset.is_valid():
            for form in phone_formset:
                if not validate_phone_number(form.cleaned_data["phone"]):
                    form.add_error('phone', 'Invalid phone number')
                    return render(request, "contacts/phone_edit.html", context)


                phone_formset.save()
                messages.success(
                    request, f"{contact.first_name}'s phones were updated successfully!"
                )
                return redirect("home")
    else:
        phone_formset = FormSet(instance=contact, prefix="phone")

    context = {
        "menu": menu,
        "title": "Edit Phones",
        "contact": contact,
        "phone_formset": phone_formset,
    }

    return render(request, "contacts/phone_edit.html", context)


@login_required
def email_update(request, contact_slug):
    contact = Contact.objects.get(slug=contact_slug)
    FormSet = forms.inlineformset_factory(Contact, Email, form=AddEmailForm, formset=EmailFormSet, extra=1, can_delete=True)
    email_formset = FormSet(request.POST, instance=contact, prefix="email")


    if request.method == "POST":
        if email_formset.is_valid():
            email_formset.save()
            messages.success(
                request, f"{contact.first_name}'s emails were updated successfully!"
            )
            return redirect("home")
    else:
        email_formset = FormSet(instance=contact, prefix="email")

    context = {
        "menu": menu,
        "title": "Edit Phones",
        "contact": contact,
        "email_formset": email_formset,
    }

    return render(request, "contacts/email_edit.html", context)


@login_required
def export_contacts(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ["FirstName", "LastName", "Birthdate", "Gender", "Address", "Email", "Phones"]
    )

    contacts = Contact.objects.filter(user=request.user)
    for contact in contacts:
        phones = contact.phones.all()
        emails = contact.emails.all()

        email_values = ""
        if emails:
            email_values = ", ".join([email.email for email in emails if email.email])

        phone_values = ""
        if phones:
            phone_values = ", ".join([phone.phone for phone in phones if phone.phone])

        writer.writerow(
            [
                contact.first_name,
                contact.last_name,
                contact.birthdate,
                contact.gender,
                contact.address,
                email_values,
                phone_values,
            ]
        )

    return response


@login_required
def import_contacts(request):
    title = "Import contacts"
    default_birthdate = timezone.make_aware(datetime.strptime("1899-01-01", "%Y-%m-%d"))
    if request.method == "POST":
        form = ContactImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"]
            try:
                reader = csv.reader(csv_file.read().decode("utf-8").splitlines())

                next(reader)

                for row in reader:
                    name1 = row[0]
                    name2 = row[1]
                    birthdate_str = row[2]
                    gender = row[3]
                    address = row[4]

                    try:
                        birthdate = parse(birthdate_str).date()
                    except ValueError:
                        birthdate = default_birthdate

                    existing_contacts = Contact.objects.filter(user_id=request.user.id).all()
                    similar_contacts = []
                    for _ in existing_contacts:
                        clean_last_name = _.last_name.split("(")
                
                        if name1 == _.first_name and name2 == clean_last_name[0].strip():
                            similar_contacts.append(_)
                    if similar_contacts:
                        name2 = f"{name2} ({len(similar_contacts)})"

                    contact = Contact(
                        first_name=name1,
                        last_name=name2,
                        birthdate=birthdate,
                        gender=gender,
                        address=address,
                        user=request.user,
                    )
                    contact.save()

                    for email_value in row[5].split(","):
                        if email_value:
                            email_obj = Email(contact=contact, email=email_value)
                            email_obj.save()

                    for phone_number_value in row[6].split(","):
                        if phone_number_value:
                            phone = PhoneNumber(
                                contact=contact, phone=phone_number_value
                            )
                            phone.save()
                messages.success(request, "Contacts imported successfully!")
                return redirect("home")
            except Exception as e:
                messages.success(request, f"Error {e} happened. Try again.")
    else:
        form = ContactImportForm()

    return render(
        request, "contacts/import.html", {"form": form, "title": title, "menu": menu}
    )


class SearchContacts(LoginRequiredMixin, DataMixin, ListView):
    model = Contact
    template_name = "contacts/search_contacts.html"
    context_object_name = "contacts"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(address__icontains=search_query)
                | Q(emails__email__icontains=search_query)
                | Q(phones__phone__icontains=search_query)
            ).distinct()

        queryset = queryset.filter(user=self.request.user).distinct()

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Search")
        context.update({"contacts": self.get_queryset()})
        return dict(list(context.items()) + list(c_def.items()))
