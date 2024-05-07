from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import SingUpForm
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

class SingUpView(View):
    def get(self, request):
        singup_form = SingUpForm()

        return render(request, 'users/singup.html', {'singup_form':singup_form})
    
    def post(self, request):
        singup_form = SingUpForm(data=request.POST)

        if singup_form.is_valid():
            singup_form.save()

            return redirect(reverse('users:login'))
        
class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {'login_form':login_form})
    
    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            return redirect(reverse('home'))
        
        else:
            return render(request, 'users/login.html', {'login_form':login_form})

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

            return redirect(reverse('home'))
        

        