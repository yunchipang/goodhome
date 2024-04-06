# views.py

from django.http import JsonResponse
from .models import Property
# from .serializers import PropertySerializer
# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.middleware.csrf import get_token
# from django.core.files.storage import FileSystemStorage
# from django.core.files.storage import default_storage
from django.conf import settings
# from urllib.parse import urljoin
import os


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


def get_property_details(request, property_id):
    try:
        property = Property.objects.get(pk=property_id)
        response_data = {
            'title': property.title,
            'category': property.category,
            'address': property.address,
            'description': property.property_descr,
            # 其他需要返回的字段
        }

        # 添加图片URL处理
        if property.image_url:
            image_url = property.image_url.url
            # 如果你需要的是绝对路径
            response_data['image_url'] = request.build_absolute_uri(image_url)

        return JsonResponse(response_data)
    except Property.DoesNotExist:
        return JsonResponse({'error': 'Property not found'}, status=404)
    except Exception as e:
        print(f'Error fetching property details: {e}')
        return JsonResponse({'error': 'Error processing request'}, status=500)
