# views.py
from django.http import JsonResponse
from .models import Property
from .serializers import PropertySerializer
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.middleware.csrf import get_token
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.conf import settings
from urllib.parse import urljoin
import os
from django.views.decorators.http import require_http_methods
from .forms import BidForm
from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer, BidSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bid
from rest_framework.permissions import AllowAny

def get_csrf(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def home(request):
    return HttpResponse("Welcome to the homepage!")

@csrf_exempt
def upload_property(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    try:
        data = request.POST
        print(data)  # Debugging purpose
        print(request.FILES)

        required_fields = ['category', 'start_bid_amount', 'seller_id', 'property_descr', 'title',
                           'is_active', 'address', 'squarefeet', 'room_type', 'created_at', 'zipcode']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Missing field: {field}'}, status=400)

        # Convert and validate data types
        is_active = data['is_active'].lower() == 'true'
        start_bid_amount = float(data['start_bid_amount'])
        seller_id = int(data['seller_id'])
        squarefeet = int(data['squarefeet'])
        zipcode = int(data['zipcode']) if data['zipcode'].isdigit() else None

        # Save image and other data
        image = request.FILES.get('image_url')
        if not image:
            return JsonResponse({'error': 'Missing property image'}, status=400)

        property_obj = Property.objects.create(
            category=data['category'],
            start_bid_amount=start_bid_amount,
            seller_id=seller_id,
            property_descr=data['property_descr'],
            title=data['title'],
            is_active=is_active,
            address=data['address'],
            squarefeet=squarefeet,
            room_type=data['room_type'],
            created_at=data['created_at'],
            zipcode=zipcode,
            image_url=image  # Ensure image is handled correctly
        )

        return JsonResponse({'success': 'Property uploaded successfully'})
    except Exception as e:
        return JsonResponse({'error': f'Error processing request: {str(e)}'}, status=400)


def get_properties(request):
    properties = Property.objects.all().values(
        'id', 'category', 'start_bid_amount', 'seller_id', 'created_at',
        'property_descr', 'title', 'is_active', 'address', 'squarefeet', 'room_type', 'image_url'
    )
    properties_list = list(properties)
    for property in properties_list:
        if property['image_url']:
            # 获取相对于MEDIA_ROOT的相对路径
            relative_path = os.path.relpath(
                property['image_url'], settings.MEDIA_ROOT)
            # 构建完整的媒体URL
            property['image_url'] = settings.MEDIA_URL + relative_path

    return JsonResponse(properties_list, safe=False)


class PropertyList(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        """
        Optionally restricts the returned properties to a given zipcode,
        by filtering against a `zipcode` query parameter in the URL.
        """
        queryset = Property.objects.filter(is_active=True)  # Assuming you only want active properties
        zipcode = self.request.query_params.get('zipcode', None)
        if zipcode is not None:
            queryset = queryset.filter(zipcode=zipcode)
        return queryset
    def get_serializer_context(self):
        """
        Pass request object to serializer to construct full image URL.
        """
        return {'request': self.request}



class BidCreate(APIView):
    permission_classes = [AllowAny]  # 允许任何人进行 POST 请求
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
            # 假设出价者ID为1，这里应该替换为实际的逻辑来获取当前用户的ID
            bid_instance = serializer.save(bidder_id=1)
            # 返回创建成功的响应，包括新创建的实例数据
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 如果数据验证失败，返回错误信息
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
