import json

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

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bid.models import User
import json


def get_csrf(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def home(request):
    return HttpResponse("Welcome to the homepage!")

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

                return JsonResponse({'status': 'success', 'message': 'Registration successful'})
            elif request.path == '/login/':
                # 登录用户
                username = data.get('username')
                password = data.get('password')

                # 验证用户
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'status': 'success', 'message': 'Login successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid action'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    else:
        return render(request, 'signuplogin.html')
