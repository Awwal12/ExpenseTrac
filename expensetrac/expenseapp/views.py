from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, LoginForm
# Create your views here.


def home(request):
    return render(request, 'base.html')


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
            return redirect('expenseapp:home')
    else:
        form = CreateUserForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('expenseapp:home')
        print('not here')
        messages.success(request, 'Username or Password is incorrect')
        return render(request, 'login.html')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('expenseapp:login_user')

def dashboard(request):
    return render(request, 'dashboard.html')