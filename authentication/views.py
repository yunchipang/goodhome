import json

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from bid.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.views import APIView
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
# from serializers import UserSerializer


# class CSRFTokenView(APIView):
#     def get(self, request):
#         csrf_token = get_token(request)
#         return JsonResponse({'csrfToken': csrf_token})

# class UserRegistrationView(generics.CreateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]

#     def post(self, request, *args, **kwargs):
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')
#             email = data.get('email')
#             password = data.get('password')
#             first_name = data.get('firstName')
#             last_name = data.get('lastName')
#             phone = data.get('phone')
#             mailing_address = data.get('address')

#             if User.objects.filter(username=username).exists():
#                 return JsonResponse({'error': 'Username is already taken'}, status=400)
#             if User.objects.filter(email=email).exists():
#                 return JsonResponse({'error': 'Email is already registered'}, status=400)

#             user = User.objects.create_user(
#                 username=username,
#                 email=email,
#                 password=password,
#                 first_name=first_name,
#                 last_name=last_name,
#                 phone=phone,
#                 mailing_address=mailing_address
#             )

#             return JsonResponse({'status': 'success', 'message': 'Registration successful'})
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        
# class UserLoginView(APIView):
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')
#             password = data.get('password')

#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 token, created = Token.objects.get_or_create(user=user)
#                 return JsonResponse({
#                     'status': 'success',
#                     'message': 'Login successful',
#                     'user_id': user.id,
#                     'token': token.key
#                 })
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})



def get_csrf(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

@csrf_exempt
def signup_login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if request.path.endswith('/signup/'):
            # Handle signup
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('firstName', '')  # Use default empty string if not provided
            last_name = data.get('lastName', '')
            phone = data.get('phone', '')
            mailing_address = data.get('address', '')

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username is already taken'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email is already registered'}, status=400)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                mailing_address=mailing_address
            )

            return JsonResponse({'status': 'success', 'message': 'Registration successful'})

        elif request.path.endswith('/login/'):
            # Handle login
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)    
                try:
                    access_token = AccessToken.for_user(user)
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Login successful',
                        'user_id': user.id,
                        'token': str(access_token)
                    }, status=status.HTTP_201_CREATED)
                except Exception as e:
                    # Log the error for debugging purposes
                    # You can use Python's logging module to log the exception details
                    print(f"Error creating or retrieving token: {e}")
                    return JsonResponse({'error': 'Error generating token'}, status=500)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=404)

    else:
        return render(request, 'signuplogin.html')
# @csrf_exempt
# def signup_login_view(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             if request.path == '/signup/':
#                 # 注册用户
#                 username = data.get('username')
#                 email = data.get('email')
#                 password = data.get('password')
#                 first_name = data.get('firstName')
#                 last_name = data.get('lastName')
#                 phone = data.get('phone')
#                 mailing_address = data.get('address')

    #             if User.objects.filter(username=username).exists():
    #                 return JsonResponse({'error': 'Username is already taken'}, status=400)
    #             if User.objects.filter(email=email).exists():
    #                 return JsonResponse({'error': 'Email is already registered'}, status=400)

    #             # 创建用户
    #             user = User.objects.create_user(
    #                 username=username,
    #                 email=email,
    #                 password=password,
    #                 first_name=first_name,
    #                 last_name=last_name,
    #                 phone=phone,
    #                 mailing_address=mailing_address
    #             )

    #             return JsonResponse({'status': 'success', 'message': 'Registration successful'})
    #         elif request.path == '/login/':
    #             # 登录用户
    #             username = data.get('username')
    #             password = data.get('password')

    #             # 验证用户
    #             user = authenticate(
    #                 request, username=username, password=password)
    #             if user is not None:
    #                 login(request, user)
    #                 token, created = Token.objects.get_or_create(user=user)
    #             # 确保在响应中返回令牌
    #                 return JsonResponse({
    #                     'status': 'success',
    #                     'message': 'Login successful',
    #                     'user_id': user.id,
    #                     'tokens': token.key  # 包含令牌在响应中
    #                 })
    #             else:
    #                 return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
    #         else:
    #             return JsonResponse({'status': 'error', 'message': 'Invalid action'})
    #     except json.JSONDecodeError:
    #         return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    # else:
    #     return render(request, 'signuplogin.html')

def home(request):
    return HttpResponse("Welcome to the homepage!")