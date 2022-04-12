from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from accounts.managers import  CarsUserManager

from validators import positive_number, only_letters_validator, validate_image

# Create your models here.

# Extending Django User
class CarsUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,

    )

    is_staff = models.BooleanField(
        default=False,
    )

    # Users can be superadmins or staff. Staff have less functions than superadmins

    date_joined = models.DateTimeField(
        auto_now=True,
    )


    USERNAME_FIELD = "email" # email will be used to login instead of username

    objects = CarsUserManager() # A Manager is the interface through which database query operations are provided to Django models



# Importing signals so the profile gets created automatically
from profiles.signals import user_created