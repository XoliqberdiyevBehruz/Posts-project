from django.urls import path
from .views import LogoutView, LoginView, SingUpView

app_name='users'
urlpatterns = [
    path('singup/', SingUpView.as_view(), name='singup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]