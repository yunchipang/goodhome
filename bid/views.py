# views.py

from django.http import JsonResponse
from .models import Property
from .serializers import PropertySerializer
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.middleware.csrf import get_token


def get_csrf(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def home(request):
    return HttpResponse("Welcome to the homepage!")


@csrf_exempt
def upload_property(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # 验证必需字段是否存在
            required_fields = ['category', 'start_bid_amount', 'seller_id',
                               'property_descr', 'title', 'is_active', 'address', 'squarefeet', 'room_type', 'created_at', 'zipcode']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing field: {field}'}, status=400)

            # 进行数据处理，例如保存到数据库
            # Your code to save data goes here
            property_obj = Property.objects.create(
                category=data['category'],
                start_bid_amount=data['start_bid_amount'],
                seller_id=data['seller_id'],
                property_descr=data['property_descr'],
                title=data['title'],
                is_active=data['is_active'],
                address=data['address'],
                squarefeet=data['squarefeet'],
                room_type=data['room_type'],
                created_at=data['created_at'],
                zipcode=int(data['zipcode'])
            )

            return JsonResponse({'success': 'Property uploaded successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


# @csrf_exempt
# def upload_property(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             # 验证必需字段是否存在
#             required_fields = ['category', 'start_bid_amount', 'seller_id',
#                                'property_descr', 'title', 'is_active', 'address', 'squarefeet', 'room_type']
#             for field in required_fields:
#                 if field not in data:
#                     return JsonResponse({'error': f'Missing field: {field}'}, status=400)

#             # 将数据保存到数据库
#             property_obj = Property.objects.create(
#                 category=data['category'],
#                 start_bid_amount=data['start_bid_amount'],
#                 seller_id=data['seller_id'],
#                 property_descr=data['property_descr'],
#                 title=data['title'],
#                 is_active=data['is_active'],
#                 address=data['address'],
#                 squarefeet=data['squarefeet'],
#                 room_type=data['room_type']
#             )

#             # 返回成功响应
#             return JsonResponse({'success': 'Property uploaded successfully'})
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#         except KeyError as e:
#             return JsonResponse({'error': f'Missing field: {e}'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=400)


def get_properties(request):
    properties = Property.objects.all().values(
        'id', 'category', 'start_bid_amount', 'seller_id', 'created_at',
        'property_descr', 'title', 'is_active', 'address', 'squarefeet', 'room_type'
    )
    return JsonResponse(list(properties), safe=False)
