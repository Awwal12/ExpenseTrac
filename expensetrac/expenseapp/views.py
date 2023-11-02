from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, LoginForm
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
from django.contrib import auth
# Create your views here.





def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, "You Have Successfully Registered! Welcome!")
            return redirect('expenses:index')
    else:
        form = CreateUserForm()
        return render(request, 'auth/register.html', {'form': form})

    return render(request, 'auth/register.html', {'form': form})


def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('expenses:index')
        messages.warning(
            request, 'Username or Password is incorrect', extra_tags='login')
        return render(request, 'auth/login.html')
    return render(request, 'auth/login.html')


def logout_user(request):
    auth.logout(request)
    messages.info(request, 'You are now logged out')
    return redirect('expenseapp:my_login')



def preferences(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':

        return render(request, 'prefer.html', {'currencies': currency_data, 'user_preferences': user_preferences})
    else:

        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request, 'prefer.html', {'currencies': currency_data, 'user_preferences': user_preferences})
