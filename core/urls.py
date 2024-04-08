"""
URL configuration for goodhome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
# Assuming bid is the app name
from bid.views import home, upload_property, get_properties, get_csrf
from authentication.views import signup_login_view


urlpatterns = [
    path('', home, name='home'),
    # path('api/', include('authentication.urls')),
    path('signup-login/', signup_login_view, name='signup_login'),
    # path('', home_view, name='home'),
    # path('SignUpLogIn/signuplogin.html', signup_login_view, name='signup_login'),
    # 注册页面
    path('signup/', signup_login_view, name='signup'),
    # 登录页面
    path('login/', signup_login_view, name='login'),
    path("admin/", admin.site.urls),
    path('upload_property/', upload_property, name='upload_property'),
    path('get_properties/', get_properties, name='get_properties'),
    path('get-csrf/', get_csrf, name='get_csrf'),
    path('api/bid/', include('bid.urls')),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
