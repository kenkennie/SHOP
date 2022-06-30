from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)

from .models import UserBase


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email address',
                                                             'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'login-pwd'}))


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(min_length=3, max_length=30)
    email = forms.EmailField(error_messages={'required': "Email required"})
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email')

    # verification

    def clean_username(self):
        userName = self.cleaned_data['username'].lower()
        i = UserBase.objects.filter(user_name=userName)
        if i.count():
            raise forms.ValidationError('Username already exists')
        return userName

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        i = UserBase.objects.filter(user_name=email)
        if i.count():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_password2(self):
        pas = self.cleaned_data
        if pas['password'] != pas['password2']:
            raise forms.ValidationError('Password do not match')
        return pas['password2']

    # styling
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})


# edit user profile
class EditProfileForm(forms.ModelForm):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                              'id': 'form-username',
                                                              'readonly': 'readonly'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email address',
                                                           'id': 'form-email', 'readonly': 'readonly'}))

    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First name',
                                                                               'id': 'form-fname'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last name',
                                                                              'id': 'form-lname'}))

    class Meta:
        model = UserBase
        fields = ('user_name', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True


class PwdForm(PasswordResetForm):
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Email address',
                                                                           'id': 'form-emailreset_'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        # email is in right format
        u = UserBase.objects.filter(email=email)
        # get user email from DB and compare with the one entered
        if not u:
            # validate user
            raise forms.ValidationError('email not found')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
         widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
         widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

