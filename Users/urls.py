from django.urls import path
from . import views


urlpatterns = [
    path('account-logout/', views.logout, name='logout'),
    path('account-profile/', views.profile, name='profile'),
    path('account-change-password/', views.change_password, name='change-password'),
    path('account-signup/', views.signup, name='signup'),
    path('account-login/', views.login, name='login')

]
