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
from bid.views import home, upload_property, get_properties, get_csrf, buy_history, get_property_details, get_auction_result, get_winner_by_auction, rate_winner, shipping_create, get_auctions_time, update_property_status
from bid.views import handle_payment, rate_seller
from authentication.views import signup_login_view, logout_view, profile_view
from query.views import execute_query

urlpatterns = [
    path('', home, name='home'),
    path("admin/", admin.site.urls),
    path('signup-login/', signup_login_view, name='signup_login'),
    # 注册页面
    path('signup/', signup_login_view, name='signup'),
    # 登录页面
    path('login/', signup_login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('upload_property/', upload_property, name='upload_property'),
    path('get_properties/', get_properties, name='get_properties'),
    path('get-csrf/', get_csrf, name='get_csrf'),
    path('api/bid/', include('bid.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/buyhistory/', buy_history, name='buy_history'),
    path('api/handle_payment/', handle_payment, name='handle_payment'),
    path('rate_seller/<int:seller_id>', rate_seller, name='rate_seller'),
    path('get_property_details/<int:property_id>',
         get_property_details, name='get_property_details'),
    path('get_auction_result/<int:property_id>',
         get_auction_result, name='get_auction_result'),
    path('get_winner/<int:auction_id>', get_winner_by_auction, name='get_winner'),
    path('rate_winner/<int:winner_id>', rate_winner, name='rate_winner'),
    path('api/shipping', shipping_create, name='shipping_create'),
    path('get_properties/<int:seller_id>/', get_properties, name='get_properties'),
    path('get_auctions_time/<int:property_id>/', get_auctions_time, name='get_auctions_time'),
    path('update_property_status/<int:property_id>/', update_property_status, name='update_property_status'),
    path('api/chat/', include('chat.urls')),
    path('api/query', execute_query, name='execute_query'),
    path('admin_feature/', include('admin_feature.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
