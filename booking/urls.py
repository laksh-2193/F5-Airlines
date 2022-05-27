from django.contrib import admin
from django.urls import path,include
from . import views
from .views import PasswordChangeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index,name="index"),
    path('signin', views.signin,name="signin"),
    path('login', views.login,name="login"),
    path('logout', views.logout,name="logout"),
    path('signup', views.signup,name="signup"),
    path('pnrstatus', views.pnrstatus,name="pnrstatus"),
    path('payment', views.payment,name="payment"),
    path('success', views.success,name="success"),
    path('ticket', views.ticket,name="ticket"),
    path('index', views.index,name="index"),
    path('flightdetails', views.flightdetails,name="flightdetails"),
    path('passengerdetails', views.passengerdetails,name="passengerdetails"),
    path('usertrips', views.usertrips,name="usertrips"),
    path('registeruser', views.registeruser,name="registeruser"),
    path('userprofile', views.userprofile,name="userprofile"),
    path('changepassword', views.PasswordChangeView.as_view(template_name="booking/changepassword.html"),name="passwordchange"),

]