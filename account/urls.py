from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', login, name="login"),
    path('logout/', login, name="logout"),
    path('mobile/signup/', mobileSignup, name="mobileSignup"),
    path('mobile/login/', mobileLogin, name="mobileLogin")
]
