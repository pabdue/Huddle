from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
# Create your views here.

def huddle_home(request):
    return render(request, 'index.html')

def huddle_group(request):
    return render(request, 'huddle_page.html')

def huddle_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is valid, log them in
            login(request, user)
            return redirect('Huddle_app:huddle_home')  # Redirect to the home page after login
        else:
            # If the user is not valid, display an error message
            messages.error(request, "Invalid username or password.")
            return redirect('Huddle_app:huddle_login')

    return render(request, 'login.html')

def huddle_signup(request):
    if request.method == 'POST':
        # Extract data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Perform basic form validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('Huddle_app:huddle_signup')

        # Check if the username or email is already taken
        if Account.objects.filter(username=username).exists() or Account.objects.filter(email=email).exists():
            messages.error(request, "Username or email already taken.")
            return redirect('Huddle_app:huddle_signup')

        # Create an Account instance and save it to the database
        account = Account(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password1
        )
        account.save()

        # Optionally, you might want to log in the user after signing up
        # For simplicity, we'll redirect to the login page
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('Huddle_app:huddle_login')

    return render(request, 'signup.html')

class CustomLoginView(auth_views.LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        # Redirect to huddle/home/ after a successful login
        return redirect('Huddle_app:huddle_home')