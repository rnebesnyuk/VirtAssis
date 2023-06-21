from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

from .forms import RegisterForm, LoginForm
from .utils import DataMixin, menu, apps
from contacts.models import Contact
from noteapp.models import Note
from filemanager.models import File

class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Signup"
        context["menu"] = menu
        return context

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data["username"]
        messages.success(
            self.request, f"Welcome, {username}. Your account has been registered!"
        )
        login(self.request, user)
        return redirect("main")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    subject_template_name = 'users/password_reset_subject.txt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


def logout_user(request):
    logout(request)
    return redirect("main")


class CustomLoginView(LoginView):
    template_name = 'users/signin.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login' 
        context['menu'] = menu
        return context


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password was successfully reset!")
            return redirect(to="login")
        return render(request, self.template_name, {'form': form})
    
    def get_success_url(self):
        return reverse_lazy("login")
    

@login_required
def profile(request):

    number_of_contacts = Contact.objects.filter(user_id=request.user.pk)
    contacts = number_of_contacts.count()

    number_of_notes = Note.objects.filter(user_id=request.user.pk)
    notes = number_of_notes.count()

    number_of_files = File.objects.filter(user_id=request.user.pk)
    files = number_of_files.count()
    

    context = {
        "menu": menu,
        "apps": apps,
        "title": "My profile",
        'contacts': contacts,
        'notes': notes,
        'files': files,
    }

    return render(request, 'users/profile.html', context)
