from django.urls import path
from .views import PropertyList,BidCreate
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', PropertyList.as_view(), name='home'), 
    path('properties/', PropertyList.as_view(), name='property-list'),
    path('bids/', BidCreate.as_view(), name='bid-create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
