from django.contrib.auth import logout, login, get_user_model, authenticate
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView, View, ListView, TemplateView

from accounts.models import CarsUser
from accounts.forms import RegisterForm, LoginForm

UserModel = get_user_model()

# Create your views here.

'''
def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
    else:
        form = RegisterForm()

    success_message = "Account created successfully!"

    context = {
         "form": form,
        "success_message": success_message,
         "form_isValid": form.is_valid(),
    }

    return render(request, 'accounts/register.html', context)
'''

class SignUpView(CreateView):
    template_name = 'accounts/register.html'
    model = UserModel
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = form.cleaned_data['password1']
        user.save()

        return super().form_valid(form)


class SignInView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = authenticate(
            email = form.cleaned_data['username'],
            password = form.cleaned_data['password'],

        )

        if not user: # if user doesn't get authenticated
            raise ValidationError("Wrong username or password")

        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        url = reverse('index')
        return url


def sign_out(request):
    logout(request)
    return redirect('index')



