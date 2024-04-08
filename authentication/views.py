import json
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User # type: ignore
import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bid.models import User
import json


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User



def get_csrf(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def home(request):
    return HttpResponse("Welcome to the homepage!")

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            profile_data = {
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                # Add other profile fields as needed
                'phone': user.profile.phone,  # Access phone from profile
                'mailing_address': user.profile.mailing_address,  # Access mailing_address from profile
                'password': user.password,  # This is not recommended to expose passwords
            }
            return Response(profile_data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

# def get_profile(request, username):
#     permission_classes = [IsAuthenticated]
#     try:
#         user = User.objects.get(username=username)
#         profile_data = {
#             'email': user.email,
#             'username': user.username,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'phone': user.profile.phone,  # Access phone from profile
#             'mailing_address': user.profile.mailing_address,  # Access mailing_address from profile
#             'password': user.password,  # This is not recommended to expose passwords
#         }

#         return JsonResponse(profile_data)
#     except ObjectDoesNotExist:
#         return JsonResponse({'error': 'User not found'}, status=404)


def update_profile(request):
    if request.method == 'PUT':
        data = request.POST
        user_profile = request.user
        if user_profile.is_authenticated:
            user_profile.phone = data.get('phone', user_profile.phone)
            user_profile.mailing_address = data.get('mailing_address', user_profile.mailing_address)
            # Update other fields as needed
            user_profile.first_name = data.get('first_name', user_profile.first_name)
            user_profile.last_name = data.get('last_name', user_profile.last_name)
            user_profile.email = data.get('email', user_profile.email)
            user_profile.password = data.get('email', user_profile.password)
            user_profile.save()
            return JsonResponse({'message': 'Profile updated successfully'})
        else:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def signup_login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if request.path == '/signup/':
                # 注册用户
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
                first_name = data.get('firstName')
                last_name = data.get('lastName')
                phone = data.get('phone')
                mailing_address = data.get('address')
                
                if User.objects.filter(username=username).exists():
                    return JsonResponse({'error': 'Username is already taken'}, status=400)
                if User.objects.filter(email=email).exists():
                    return JsonResponse({'error': 'Email is already registered'}, status=400)
        

                # 创建用户
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    mailing_address=mailing_address
                )

                username = user.username
                return JsonResponse({'status': 'success', 'message': 'Registration successful'})
            elif request.path == '/login/':
                # 登录用户
                username = data.get('username')
                password = data.get('password')

                # 验证用户
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    username = user.username
                    return JsonResponse({'status': 'success', 'message': 'Login successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid action'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    else:
        return render(request, 'signuplogin.html')
