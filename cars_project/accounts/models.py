from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from accounts.managers import  CarsUserManager

from validators import positive_number, only_letters_validator, validate_image

# Create your models here.

class CarsUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,

    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now=True,
    )


    USERNAME_FIELD = "email"

    objects = CarsUserManager()



# Importing signals so the profile gets created automatically
from profiles.signals import user_created