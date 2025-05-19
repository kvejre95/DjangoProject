from django.shortcuts import render, redirect
from .models import UserDetails
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from . serializers import UserDetailsSerializer
import json
from django.views.decorators.csrf import csrf_exempt
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


@csrf_exempt
def get_all_users(request):
    if request.method == "GET":
        all_users=UserDetails.objects.all()
        get_all_users_dto = UserDetailsSerializer(all_users, many=True)
        return JsonResponse({
            "success": True,
            "Data": get_all_users_dto.data,
        }, status=200)


@csrf_exempt
def create_new_user(request):
    if request.method == "POST":
        input_data = json.loads(request.body)
        create_user_command = UserDetailsSerializer(data = input_data)
        if create_user_command.is_valid():
            create_user_command.save()

            return JsonResponse({
            "success":True,
            "Data":create_user_command.data
            }, status=201)
        else:
            return JsonResponse({
                "success": False,
                "Data": "Invalid Data"
            }, status=400)

@csrf_exempt
def get_single_user(request, search):
    if request.method == "GET":
        try:
            # First try to find by email
            user_obj = UserDetails.objects.get(email=search)
        except UserDetails.DoesNotExist:
            try:
                # If not found by email, try username
                user_obj = UserDetails.objects.get(username=search)
            except UserDetails.DoesNotExist:
                # Not found by either email or username
                return JsonResponse({
                    "success": False,
                    "message": "User not found"
                }, status=404)
        
        user_dto = UserDetailsSerializer(user_obj)
        return JsonResponse({
            "success": True,
            "Data": user_dto.data,
        }, status=200)
    
@csrf_exempt
def update_user_data(request, username):
    if request.method == "PUT":
        try:
            user=UserDetails.objects.get(username = username)
            input_data=json.loads(request.body)
            print(input_data)
            update_data=UserDetailsSerializer(user, data=input_data)
            print(update_data)
            if update_data.is_valid():
                update_data.save()
                return JsonResponse({
                "success":True,
                "Data":update_data.data,
                "Message":"Data updated successfully"
            }, status=200)

        except Exception as e:
            return JsonResponse({
                "success":False,
                "Data":update_data.data
            }, status=500)

    if request.method=="PATCH":
        try:
            user=UserDetails.objects.get(username=username)
            input_data=json.loads(request.body)
            update_data=UserDetailsSerializer(user,data=input_data, partial=True)

            if update_data.is_valid():
                update_data.save()
                return JsonResponse({
                "success":True,
                "Data":update_data.data,
                "Message":"Data updated successfully"
            }, status=200)
            else:
                return JsonResponse({
                "success":False,
                "error":update_data.errors
            }, status=400)

        except Exception as e:

            return JsonResponse({
                "success":False,
                "Data":update_data.data,
                "Error":str(e)
            }, status=500)

@csrf_exempt
def delete_user_data(request, email):
    if request.method == "DELETE":
        user=UserDetails.objects.get(email=email)
        user.delete()

        return JsonResponse({
                "success":True,
                "Message":"Data deleted successfully",
            }, status=200)

