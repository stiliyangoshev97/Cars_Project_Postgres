from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, View, DeleteView, UpdateView, DetailView, ListView

from django.contrib.auth.models import Group

from accounts.decorators import any_groups_required
# Create your views here.

from cars.forms import CreateCarForm, CarCommentForm, CarsRaceForm
from cars.models import Car, BoughtCars, CarComment
from profiles.models import Profile
from profiles.forms import UpdateProfileForm


# Car can be created only by superusers -> Logic designed in the template
class CreateCarView(CreateView, LoginRequiredMixin):
    model = Car
    fields = ('hp', 'type', 'photo', 'price',)
    success_url = reverse_lazy('cars:create_car')
    template_name = 'cars/create_car.html'
    context_object_name = 'cars'


class ListCarsView(ListView, LoginRequiredMixin):
    model = Car
    template_name = 'cars/list_cars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        already_bought = False # Cars that are bought won't be displayed
        cars = Car.objects.filter(is_sold=False) # Filter a list with only the not sold cars
        bought_cars = BoughtCars.objects.all()
        profile = Profile.objects.get(user=self.request.user) # Get the profile of the logged user

        for car in cars:
            for bought_car in bought_cars:
                if bought_car.racer.id == profile.user.id: # Check if the racer in bought car model is the same as the profile of the logged user
                    already_bought = True

        context['already_bought'] = already_bought
        context['cars'] = cars
        context['bought_cars'] = bought_cars
        context['profile'] = profile

        return context


@login_required
def alert_message(request):
    message = 'Not enough money to buy this car!'

    context = {
        "message": message,
    }

    return render(request, 'cars/alert_message.html', context)

@login_required
def buy_car(request, pk):
    racer = request.user
    car = Car.objects.get(pk=pk)

    profile = Profile.objects.get(pk=racer.id)

    if profile.money >= car.price: # Check if the racer has enough money to buy the car. Money are stored in his profile
        profile.money = profile.money - car.price
        profile.save()
        bought_car = BoughtCars(racer=racer, car=car) # Add a car which was successfully bought to the model
        bought_car.save()
        car.is_sold = True # When a car is bought, this boolean field will be True until the car is sold again
        car.save()
        return redirect('index')
    else:
        # Redirect to a success page
        return redirect('cars:alert_message')

@login_required
def sell_car(request):
    bought_car = BoughtCars.objects.get(racer=request.user) # Select the car of the logged user which he wants to sell
    car = bought_car.car # Select the car
    car.is_sold = False
    car.save()

    profile = Profile.objects.get(pk=request.user.pk)
    profile.money = profile.money + car.price # When the car is sold, the racer will get his money back
    profile.save()

    # When car is sold, money get back to the owner

    bought_car.delete()

    return redirect('index')

@login_required
def winner_message(request):
    message = 'Congratulations! You have won the race!'

    context = {
        "message": message,
    }

    return render(request, 'cars/winner_message.html', context)

@login_required
def loser_message(request):
    message = 'Sorry, you have lost the race...You better buy a new car!'

    context = {
        "message": message,
    }

    return render(request, 'cars/loser_message.html', context)

# Only users that have a car can race. The logic is in the template
@login_required
def race(request):

    has_car = False
    user_car = None

    if BoughtCars.objects.filter(racer=request.user).exists():
        has_car = True
        user_car = BoughtCars.objects.get(racer=request.user)

    if request.method == "POST":
        form = CarsRaceForm(request.POST)

        if form.is_valid():
            car_to_race = form.cleaned_data['chosen_car']
        # submit_button = form.cleaned_data['submit']

            user_car = BoughtCars.objects.get(racer=request.user)
            chosen_car = Car.objects.get(type=str(car_to_race)) # Query car where car.type is equal to the string car_to_race

            if user_car.car.hp > chosen_car.hp: # Check which car has more horse power
                return redirect('cars:winner_message')
            else:
                return redirect('cars:loser_message')
    else:
        form = CarsRaceForm()

    context = {
        "form": form,
        "has_car": has_car,
        "user_car": user_car,
    }

    return render(request, 'cars/race.html', context)

class EditCarView(UpdateView, LoginRequiredMixin):
    model = Car
    form_class = CreateCarForm
    success_url = reverse_lazy('cars:list_cars')
    template_name = 'cars/edit_car.html'

@login_required
def delete_car(request, pk):
    car = Car.objects.get(pk=pk)
    car.delete()

    return redirect('cars:create_car')


# If logged user is a part of the staff, he can delete the comment of other users, but he cannot edit them
# If logged user is a superuser, he can edit and delete comments of other users
# If logged user is a regular user, he can edit and delete only his own comments
# Logic is in the template
class WriteCommentView(LoginRequiredMixin, CreateView):
    template_name = 'cars/car_comments.html'
    form_class = CarCommentForm
    model = CarComment

    def get(self, request, *args, **kwargs):
        self.car = Car.objects.get(pk=self.kwargs.get('pk'))

        # Filter comments where car is equal to the selected car
        self.comments = CarComment.objects.filter(car=self.car)

        # If user wrote the comment he will see "You" instead of the email address
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        url = reverse_lazy('cars:list_cars')
        return url

    def form_valid(self, form, **kwargs):
        car = Car.objects.get(pk=self.kwargs.get('pk')) # Select the car we are writing the comment for
        comment_form = form.save(commit=False)
        comment_form.car = car
        comment_form.writer = self.request.user
        comment_form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = self.form_class
        context['car'] = self.car
        context['comments'] = self.comments
        context['you'] = 'You'
        context['user'] = self.request.user
        return context



def delete_comment(request, pk):
    comment = CarComment.objects.get(pk=pk)

    comment.delete()

    return redirect('cars:write_comment', comment.car.id)


class EditCommentView(UpdateView, LoginRequiredMixin):
    model = CarComment
    form_class =  CarCommentForm
    template_name = 'cars/edit_comment.html'

    def get_success_url(self, **kwargs):
        url = reverse_lazy('cars:list_cars')
        return url

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['comment'] = CarComment.objects.get(pk=self.kwargs.get('pk')) # Select the comment that will be edited
        #context['comment'] = CarComment.objects.get(pk=self.object.pk) # Works also as the line above
        context['comment_text'] = CarComment.objects.get(pk=self.object.pk).text

        return context








