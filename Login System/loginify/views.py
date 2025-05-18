from django.shortcuts import render, redirect
from .models import UserDetails
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.

def landing_test(request):
    return HttpResponse("Hello World!!")

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if email already exists
        if UserDetails.objects.filter(email=email).exists():
            return render(request, 'loginify/signup.html', {'error': 'Email already exists'})
        
        # Create new user
        user = UserDetails(username=username, email=email, password=password)
        user.save()
        
        # Redirect to login page
        return redirect('login')
    
    return render(request, 'loginify/signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = UserDetails.objects.get(email=email)
            if user.password == password:
                # Successful login
                messages.success(request, f'Welcome, {user.username}! You have successfully logged in.')
                return redirect('login')
            else:
                return render(request, 'loginify/login.html', {'error': 'Invalid password'})
        except UserDetails.DoesNotExist:
            return render(request, 'loginify/login.html', {'error': 'Email not found'})
    
    return render(request, 'loginify/login.html')