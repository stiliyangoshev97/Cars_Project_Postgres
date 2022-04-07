from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

UserModel = get_user_model()

class Car(models.Model):

    hp = models.PositiveIntegerField(
        blank=True,
    )

    TYPE_CHOICE_FERRARI = 'ferrari'
    TYPE_CHOICE_LAMBO = 'lamborghini'
    TYPE_CHOICE_PORCHE = 'porche'

    TYPE_CHOICES = (
        (TYPE_CHOICE_LAMBO, 'Lambo'),
        (TYPE_CHOICE_FERRARI, 'Ferrari'),
        (TYPE_CHOICE_PORCHE, 'Porche'),
    )

    type = models.CharField(
        max_length=32,
        blank=True,
        choices = TYPE_CHOICES,
    )

    photo = models.ImageField(
        upload_to='cars',
        blank=True,
    )

    price = models.PositiveIntegerField(
        blank=True,
    )

    is_sold = models.BooleanField(
        blank=True,
        default=False,
    )

    def __str__(self):
        return self.type


class BoughtCars(models.Model):
    racer = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        blank=True,

    )

    car = models.ForeignKey(
          Car,
         on_delete=models.CASCADE,
         blank=True,
        )

    def __str__(self):
        return self.car.type


class CarComment(models.Model):
    text = models.TextField(
        blank=True,
        max_length=256,
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        blank=True,
    )

    writer = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        blank=True,
    )

    def __str__(self):
        return self.car.type






