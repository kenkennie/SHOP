from django.urls import path
from django.views.generic import TemplateView

from account import views
from django.contrib.auth import views as auth_views

from account.forms import (UserLoginForm, PwdForm, PwdResetConfirmForm)

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login'), name='logout'),
    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),

    # reset password
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="account/user/password_reset_form.html",
                                                                success_url='confirm_password_reset_email',
                                                                email_template_name='account/user/password_reset_email.html',
                                                                form_class=PwdForm), name='pwdReset'),
    path('reset_password_confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="account/user/new_password.html",
                                                     success_url='/account/password_reset_complete/',
                                                     form_class=PwdResetConfirmForm), name='new_password_confirm'),

    path('confirm_password_reset_email', TemplateView.as_view(template_name='account/user/reset_status.html'), name='confirm_password_reset_email'),
    path('complete', TemplateView.as_view(template_name='account/user/reset_status.html'), name='password_reset_complete'),
    # dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('delete_confirm/', TemplateView.as_view(template_name='account/user/delete-confirm.html'),
         name='delete_confirm')
]
