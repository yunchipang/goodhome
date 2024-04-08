# views.py

from django.http import JsonResponse
from .models import Property
from .models import Winner
from .models import Auction
from .models import WinnerRating
from .models import User
from .models import ShippingGift
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.middleware.csrf import get_token
from django.conf import settings
import os
from django.views.decorators.http import require_http_methods


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


def get_auction_result(request, property_id):
    try:
        # 查询对应 property_id 的拍卖信息
        auction = Auction.objects.filter(property_id=property_id).order_by(
            '-current_highest_bid').first()
        if auction:
            # 根据找到的拍卖信息获取对应的获胜者信息
            winner_info = get_winner_by_auction(auction.id)
            if winner_info:
                # 返回拍卖和获胜者信息
                return JsonResponse({
                    'property_id': property_id,
                    'current_highest_bid': auction.current_highest_bid,
                    'start_time': auction.start_time,
                    'end_time': auction.end_time,
                    'winner_id': winner_info['winner_id'],
                    'sale_price': winner_info['sale_price']
                })
            else:
                return JsonResponse({'error': 'Winner not found for this auction'}, status=404)
        else:
            return JsonResponse({'error': 'Auction not found for this property'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_winner_by_auction(auction_id):
    try:
        # 根据 auction_id 查询对应的获胜者信息
        winner = Winner.objects.filter(auction_id=auction_id).first()
        if winner:
            return {
                'winner_id': winner.user_id,
                'sale_price': winner.temp_sale_price
            }
        else:
            return None
    except Exception as e:
        raise e


@csrf_exempt
def rate_winner(request, winner_id):
    try:
        # 解析JSON请求体
        data = json.loads(request.body)
        rating = data.get('rating')
        message = data.get('message')

        # 确认数据存在
        if not (rating and message):
            return JsonResponse({'error': 'Rating or message is missing.'}, status=400)

        # 假设您已经通过身份验证获取了卖家的用户ID
        seller_id = 1

        # 检查卖家和获胜者是否存在，并且评分数据有效
        if User.objects.filter(id=winner_id).exists():
            winner = User.objects.get(id=winner_id)
            WinnerRating.objects.create(
                seller_id=seller_id,
                winner=winner,
                rating=rating,
                message=message
            )
            return JsonResponse({'message': 'Rating saved successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'Seller or winner does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def shipping_create(request):
    # 解析请求体中的JSON数据
    data = json.loads(request.body.decode('utf-8'))

    # 获取数据字段
    # seller_id = data.get('seller_id')
    seller_id = 1
    winner_id = data.get('winner_id')
    trackingNumber = data.get('trackingNumber')

    # 确保所有需要的字段都被正确传递并且不为空
    if seller_id and winner_id and trackingNumber:
        # 创建ShippingGift实例
        shipping_gift = ShippingGift.objects.create(
            seller_id=seller_id,
            winner_id=winner_id,
            ups_tracking_number=trackingNumber
        )
        # 返回成功响应
        return JsonResponse({'status': 'success', 'shipping_id': shipping_gift.id})
    else:
        # 如果数据不完整，返回错误信息
        return JsonResponse({'status': 'error', 'message': 'Missing data in request'}, status=400)
