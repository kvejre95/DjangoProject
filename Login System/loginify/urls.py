from django.urls import path
from .views import landing_test, signup, login, get_all_users, create_new_user, get_single_user, update_user_data, delete_user_data

urlpatterns = [
    path("", landing_test, name="Landing Test"),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path("get_users/", get_all_users, name="Get User Details"),
    path("create_user/", create_new_user, name="Create New User Detail"),
    path("get_user/<str:search>", get_single_user, name='Search User'),
    path("update_user/<str:username>", update_user_data, name='Update User'),
    path("delete_user/<str:email>", delete_user_data, name= "Delete User"),
]

