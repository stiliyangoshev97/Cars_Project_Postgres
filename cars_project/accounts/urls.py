from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    #path('register/', views.sign_up, name="sign_up"),
    path('register/', views.SignUpView.as_view(), name="sign_up"),
    #path('login/', views.sign_in, name="sign_in"),
    path('login/', views.SignInView.as_view(), name="sign_in"),
    path('logout/', views.sign_out, name="sign_out"),
]