from django.db import models

# Importing the PhoneNumberField. In settings -> apps -> we have to declare it also
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

from accounts.models import CarsUser
from validators import positive_number, only_letters_validator, validate_image


class Profile(models.Model):
    profile_photo = models.ImageField(
        blank=True,
        upload_to='profiles',
        validators=(
            validate_image,
        )
    )

    user = models.OneToOneField(
        CarsUser,
        on_delete=models.CASCADE,
        primary_key=True, # User and Profile will have the same pk
    )

    first_name = models.CharField(
        blank=True,
        max_length=24,
        validators=(
            only_letters_validator,
        )
    )

    last_name = models.CharField(
        blank=True,
        max_length=24,
        validators=(
            only_letters_validator,
        )
    )

    money = models.FloatField(
        default=0,
        blank=True,
        validators=(
            positive_number,
        )
    )


    phone_number = PhoneNumberField(

    )

    is_verified = models.BooleanField(
        blank=True,
        default=False,
    )

    # is_complete is used to check if profile is all completed or partially
    is_complete = models.BooleanField(
        blank=True,
        default=False,
    )

    def increase_wealth(self):
        self.money += 500

    def __str__(self):
        return self.user.email