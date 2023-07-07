from django.urls import path
from users.views import register_user, login_user, logout_user

urlpatterns = [
    path('registration/', register_user, name="register"),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]