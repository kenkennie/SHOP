from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField


# Abstract base user -> create custom normal user
# BaseUserManager -> overrider the admin models to custom model
# PermissionsMixin -> gives the custom admin account the default permissions


class CustomAccountManager(BaseUserManager):
    # create superadmin
    def create_superuser(self, email, user_name, password, **OtherFields):

        # set superuser field to be true when created
        OtherFields.setdefault('is_staff', True)
        OtherFields.setdefault('is_superuser', True)
        OtherFields.setdefault('is_active', True)

        # if fields are not set to true raise an error
        if OtherFields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_stuff')
        if OtherFields.get('is_superuser') is not True:
            raise ValueError('Super user must be assigned to is_superuser')

        return self.create_user(email, user_name, password, **OtherFields)

    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        # check  email has a good format
        user = self.model(email=email, user_name=user_name, **other_fields)

        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    country = CountryField()

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    # change default username field to email
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'kennie@kennie.com',
            [self.email],
            fail_silently=False
        )

    def __str__(self):
        return self.email
