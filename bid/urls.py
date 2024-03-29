from django.urls import path
from .views import PropertyList

urlpatterns = [
    path('properties/', PropertyList.as_view(), name='property-list'),
]
