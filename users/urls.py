from django.urls import path
from users import views

urlpatterns = [
    path('users/login',views.loginPage,name='user-login')
]