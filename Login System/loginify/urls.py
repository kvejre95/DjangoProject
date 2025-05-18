from django.urls import path
from .views import landing_test, signup, login

urlpatterns = [
    path("", landing_test, name="Landing Test"),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
]

