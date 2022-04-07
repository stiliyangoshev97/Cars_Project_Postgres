from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView, TemplateView

from profiles.forms import UpdateProfileForm, UpdateProfileMoney
from profiles.models import Profile

from cars.models import BoughtCars





class ProfileDetailsView(TemplateView, LoginRequiredMixin):
    template_name = 'profiles/profile_details.html'


    def check_for_car(self):
        car = None
        if BoughtCars.objects.filter(racer=self.request.user).exists():
            car = BoughtCars.objects.get(racer=self.request.user)
        else:
            car = None
        return car

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)

        context['car'] = self.check_for_car()
        return context



class UpdateProfileView(FormView, LoginRequiredMixin):
    model = Profile
    template_name = 'profiles/edit_profile.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('profiles:update_profile')



    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.profile_photo = form.cleaned_data['profile_photo'] #it works also without this line
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)




class IncreaseMoneyView(FormView, LoginRequiredMixin):
    form_class = UpdateProfileMoney
    model = Profile
    template_name = 'profiles/update_money.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_money'] = Profile.objects.get(user=self.request.user).money

        return context

    # Without the post and get method, when we save to the database
    # we will update only the "money" field and the rest will be resetted
    # to blank, so we need to apply this get and post methods here
    # and not write them down in the form, otherwise we will get a
    # WSGIRequest error

    def get(self, request, *args, **kwargs):
        # the object will be the profile of the current logged user
        self.object = Profile.objects.get(pk=request.user.id)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = Profile.objects.get(pk=request.user.id)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        #self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.money += form.cleaned_data['money']
        self.object.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        raise ValidationError('Form not valid!')
        return super().form_invalid(form)





