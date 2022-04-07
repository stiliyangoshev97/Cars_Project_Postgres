from django.db import models

# Importing the PhoneNumberField. In settings -> apps -> we have to declare it also
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

from accounts.models import CarsUser

class Profile(models.Model):
    profile_photo = models.ImageField(
        blank=True,
        upload_to='profiles',
    )

    user = models.OneToOneField(
        CarsUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        blank=True,
        max_length=24,
    )

    last_name = models.CharField(
        blank=True,
        max_length=24,
    )

    money = models.FloatField(
        default=0,
        blank=True,
    )


    phone_number = PhoneNumberField(

    )

    is_verified = models.BooleanField(
        blank=True,
        default=False,
    )

    is_complete = models.BooleanField(
        blank=True,
        default=False,
    )

    def increase_wealth(self):
        self.money += 500

    def __str__(self):
        return self.user.email