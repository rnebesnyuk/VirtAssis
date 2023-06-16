from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path

from . import views
from .forms import LoginForm
from .views import *


urlpatterns = [
    path("signup/", RegisterUser.as_view(), name="register"),
    path("signin/", CustomLoginView.as_view(),name="login",),
    path("logout/",logout_user, name="logout"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "reset-password/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url="/users/reset-password/complete/",
        ),
        name="password_reset_confirm",
    ),
    path("reset-password/complete/", CustomPasswordResetCompleteView.as_view(), name="password_reset_complete",),
]
