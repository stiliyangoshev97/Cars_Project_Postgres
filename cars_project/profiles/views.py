from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, FormView, TemplateView, DeleteView

from profiles.forms import UpdateProfileForm, UpdateProfileMoney
from profiles.models import Profile

from cars.models import BoughtCars

UserModel = get_user_model() # Reference the user model



# Users can check details about their profile

class ProfileDetailsView(TemplateView, LoginRequiredMixin):
    template_name = 'profiles/profile_details.html'

    # Check if user has a car of he does not have one. In BoughtCars we store the cars that were bought with fk to the user
    # a user can have only 1 car
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

        context['car'] = self.check_for_car() # Calling the method above
        return context


# Update profile view. I have made it without a pk to be given in the urls.py
# Each user has only one profil
class UpdateProfileView(FormView, LoginRequiredMixin):
    model = Profile
    template_name = 'profiles/edit_profile.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('profiles:update_profile')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.profile_photo = form.cleaned_data['profile_photo'] #it works also without this line
        self.object.user = self.request.user # The profile that we update
        self.object.save()

        return super().form_valid(form)

# Will delete the user and the respective profile
def delete_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    user = UserModel.objects.get(pk=pk)

    profile.delete()
    user.delete()

    return redirect('index')

# View not used. It works, it deletes the profile and user, but it does not redirect to the success url
class DeleteProfileView(DeleteView):
    model = Profile
    template_name = 'profiles/profile_confirm_delete.html'

    def get_success_url(self):
        url = reverse_lazy('index')
        return url

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=self.request.user.pk)
        user = UserModel.objects.get(pk=self.request.user.pk)
        profile.delete()
        user.delete()

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=self.request.user.pk)
        user = UserModel.objects.get(pk=self.request.user.pk)
        return super().get(request, *args, **kwargs)


# View used to increase the amount of money for a user. Money is an attribute in his profile
class IncreaseMoneyView(FormView, LoginRequiredMixin):
    form_class = UpdateProfileMoney
    model = Profile
    template_name = 'profiles/update_money.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_money'] = Profile.objects.get(user=self.request.user).money # Money from the profile of the current logged user

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
        self.object.money += form.cleaned_data['money'] # Update the money of the user, adding the new amount
        self.object.save()

        return super().form_valid(form)

  





