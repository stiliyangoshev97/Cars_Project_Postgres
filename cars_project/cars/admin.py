from django.contrib import admin
from cars.models import Car, BoughtCars, CarComment

# Register your models here.

admin.site.register(Car)

admin.site.register(BoughtCars)

admin.site.register(CarComment)

