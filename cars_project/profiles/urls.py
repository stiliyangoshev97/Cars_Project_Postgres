from django.urls import path
from profiles import views

app_name = 'profiles'

urlpatterns = [
    #path('edit_profile/', views.update_profile, name='update_profile'),
    path('edit_profile/', views.UpdateProfileView.as_view(), name='update_profile'),
    #path('profile_details', views.profile_details, name='profile_details'),
    path('profile_details', views.ProfileDetailsView.as_view(), name='profile_details'),
    #path('update_money', views.increase_money, name="update_money"),
    path('update_money', views.IncreaseMoneyView.as_view(), name="update_money"),
]