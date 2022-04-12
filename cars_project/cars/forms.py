from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from profiles.models import Profile
from cars.models import Car, BoughtCars, CarComment

UserModel = get_user_model()

class CreateCarForm(ModelForm):
    class Meta:
        model = Car
        exclude = ('is_sold',)


class CarCommentForm(ModelForm):
    class Meta:
        model = CarComment
        exclude = ('car','writer',)

# Form that allows racers to race each other
class CarsRaceForm(forms.Form):
    cars = Car.objects.all() # Select all cars

    cars_list = [] # Creating a list for the cars

    for car in cars:
        cars_list.append(car.type) # Adding to the list the current cars

    CARS_CHOICES = [] # Creating an empty list for the current cars

    for car in cars_list:
        CARS_CHOICES.append((cars_list.index(car), car)), # Create the tuple for the CARS_CHOICES list

    car_to_race = forms.CharField(
        label='Who do you want to race?',
        widget=forms.Select(choices=CARS_CHOICES), # Choices will be visible in a form
    )

    chosen_car = forms.CharField(
        max_length=12,
        required=True,
        label='Write the name of the car from the list above',
    )






