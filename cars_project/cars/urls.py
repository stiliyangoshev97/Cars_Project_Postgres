from django.urls import path

from cars import views

app_name = 'cars'

urlpatterns = [
    #path('create_car/', views.create_car, name='create_car'),
    path('create_car/', views.CreateCarView.as_view(), name='create_car'),
    #path('list_cars/', views.list_cars, name='list_cars'),
    path('list_cars/', views.ListCarsView.as_view(), name='list_cars'),
    path('buy_car/<pk>', views.buy_car, name='buy_car'),
    path('sell_car/', views.sell_car, name='sell_car'),
    path('alert_message/', views.alert_message, name='alert_message'),

    path('car_comments/<pk>', views.WriteCommentView.as_view(), name='write_comment'),
    path('edit_comment/<pk>', views.EditCommentView.as_view(), name='edit_comment'),
    path('delete_comment/<pk>', views.delete_comment, name='delete_comment'),
    path('race/', views.race, name='race'),
    path('winner_message/', views.winner_message, name='winner_message'),
    path('loser_message/', views.loser_message, name='loser_message'),





]