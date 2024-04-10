# views.py
import datetime
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Property
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.conf import settings
import os
from django.views.decorators.http import require_http_methods
from .forms import BidForm
from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Bid, Auction, User, Bidder, Winner
from datetime import datetime
from django.db.models import Max
from django.utils import timezone
from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now

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
from django.views.decorators.http import require_GET
from rest_framework_simplejwt.tokens import AccessToken


def get_csrf(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def home(request):
    return HttpResponse("Welcome to the homepage!")


@csrf_exempt
def upload_property(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    token = request.headers.get('Authorization').split()[1]
    decoded_token = AccessToken(token)
    print(f"decoded_token: {decoded_token}")
    user_id = decoded_token['user_id']
    print("user_id: {}".format(user_id))
    
    try:
        # Fetch the user object from the database
        user = User.objects.get(id=user_id)
    except Exception as e:
        return JsonResponse({'error': f'Invalid token: {str(e)}'}, status=400)

    try:
        data = request.POST
        image = request.FILES.get('image_url')
        print(data)  # Debugging purpose
        print(request.FILES)

        seller_id = user_id

        required_fields = ['category', 'start_bid_amount', 'seller_id', 'property_descr', 'title',
                           'is_active', 'address', 'squarefeet', 'room_type', 'created_at', 'zipcode']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Missing field: {field}'}, status=400)

        # Convert and validate data types
        is_active = data['is_active'].lower() == 'true'
        start_bid_amount = float(data['start_bid_amount'])
        # seller_id = int(data['seller_id'])
        squarefeet = int(data['squarefeet'])
        zipcode = int(data['zipcode']) if data['zipcode'].isdigit() else None

        # Save image and other data
        # image = request.FILES.get('image_url')
        # image = files.get('image_url')
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


# class UploadPropertyView(APIView):

#     def upload_property(self, request, *args, **kwargs):
#         print("----------line67 here----------")
#         print(request)

#         try:
#             print("----------line71 Entered")
#             data = request.POST
#             image = request.FILES.get('image_url')
#             print(data)  # Debugging purpose
#             print("----------line74 Entered")
#             print(request.FILES)

#             seller_id = request.user.id

#             required_fields = ['category', 'start_bid_amount', 'property_descr', 'title',
#                                'is_active', 'address', 'squarefeet', 'room_type', 'created_at', 'zipcode']
#             for field in required_fields:
#                 if field not in data:
#                     return JsonResponse({'error': f'Missing field: {field}'}, status=400)

#             # Convert and validate data types
#             is_active = data['is_active'].lower() == 'true'
#             start_bid_amount = float(data['start_bid_amount'])
#             squarefeet = int(data['squarefeet'])
#             zipcode = int(data['zipcode']) if data['zipcode'].isdigit() else None

#             # Save image and other data
#             if not image:
#                 return JsonResponse({'error': 'Missing property image'}, status=400)

#             property_obj = Property.objects.create(
#                 category=data['category'],
#                 start_bid_amount=start_bid_amount,
#                 seller_id=seller_id,
#                 property_descr=data['property_descr'],
#                 title=data['title'],
#                 is_active=is_active,
#                 address=data['address'],
#                 squarefeet=squarefeet,
#                 room_type=data['room_type'],
#                 created_at=data['created_at'],
#                 zipcode=zipcode,
#                 image_url=image  # Ensure image is handled correctly
#             )

#             return JsonResponse({'success': 'Property uploaded successfully'})
#         except Exception as e:
#             return JsonResponse({'error': f'Error processing request: {str(e)}'}, status=400)

@require_GET
def get_properties(request, seller_id):
    try:
        properties = Property.objects.filter(seller_id=seller_id)
        properties_list = []

        for property in properties:
            # Check if there is an image and create the full URL if it exists
            image_url = request.build_absolute_uri(property.image_url.url) if property.image_url else None

            property_data = {
                'id': property.id,
                'category': property.category,
                'start_bid_amount': property.start_bid_amount,
                'seller_id': property.seller_id,
                'created_at': property.created_at,
                'property_descr': property.property_descr,
                'title': property.title,
                'is_active': property.is_active,
                'address': property.address,
                'squarefeet': property.squarefeet,
                'room_type': property.room_type,
                'zipcode': property.zipcode,
                'image_url': image_url
            }
            properties_list.append(property_data)

        return JsonResponse(properties_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])  # Only allow POST requests
def upload_bid(request):
    try:
        # Parse request body to get data
        # data = json.loads(request.body)
        data = json.loads(request.body.decode('utf-8'))
        print("Request data:", request.POST)  # For form data
        print("Request JSON data:", request.body)  # For raw JSON data
        # Extract data
        amount = data['amount']
        amount = Decimal(amount)
        auction_id = data['auction']
        bidder_id = data['bidder']
        # 确保所有必需字段都存在
        if not all([amount, auction_id, bidder_id]):
            return HttpResponseBadRequest("Missing required fields")
        # Fetch the auction and bidder instances
        auction = Auction.objects.get(pk=auction_id)
        bidder = Bidder.objects.get(pk=1)
        print("Bidder instance:", bidder)
        print("Auction instance:", auction)
        if auction.start_time <= now() <= auction.end_time:
            # 获取或创建对应的Winner实例
            winner, created = Winner.objects.get_or_create(
                auction=auction,
                defaults={'temp_sale_price': amount, 'user': bidder.user}
            )
            # 假设如果temp_sale_price是None，则将其视为0
            temp_sale_price = winner.temp_sale_price if winner.temp_sale_price is not None else Decimal(
                '0.00')
            # 如果不是新创建的，并且新的出价高于当前的临时最高出价，则更新
            if not created and amount > temp_sale_price:
                winner.temp_sale_price = amount
                winner.user = bidder.user  # 更新最高出价者
                winner.save()

            # 创建并保存新的出价记录
            bid = Bid.objects.create(
                amount=amount, auction=auction, bidder=bidder)
            # Return success response
            return JsonResponse({"message": "Bid uploaded successfully", "bid_id": bid.id})

        else:
            # 如果当前时间不在拍卖的开始时间和结束时间之间
            return JsonResponse({"error": "Auction has ended. No more bids are accepted."}, status=400)
    except Auction.DoesNotExist:
        return JsonResponse({"error": "Auction does not exist."}, status=400)
    except Bidder.DoesNotExist:
        return JsonResponse({"error": "Bidder does not exist."}, status=400)
    except (KeyError, Auction.DoesNotExist, User.DoesNotExist, json.JSONDecodeError) as e:
        print(e)  # Log the error for debugging
        # Return error response if something goes wrong
        return HttpResponseBadRequest("Invalid data provided")


class PropertyList(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        """
        Optionally restricts the returned properties to a given zipcode,
        by filtering against a `zipcode` query parameter in the URL.
        """
        queryset = Property.objects.filter(
            is_active=True)  # Assuming you only want active properties
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


def submit_bid(auction_id, bidder_id, amount):
    now = timezone.now()
    auction = Auction.objects.get(pk=auction_id)

    # 确保竞拍仍在进行中
    if auction.start_time <= now <= auction.end_time:
        Bid.objects.create(bidder_id=bidder_id,
                           auction_id=auction_id, amount=amount)

        # 更新临时最高出价
        max_bid = Bid.objects.filter(auction_id=auction_id).aggregate(
            Max('amount'))['amount__max']
        highest_bid = Bid.objects.filter(
            auction_id=auction_id, amount=max_bid).first()

        # 检查是否已存在获胜者记录
        winner, created = Winner.objects.get_or_create(auction_id=auction_id, defaults={
                                                       'user': highest_bid.bidder.user, 'temp_sale_price': max_bid})
        if not created:
            winner.user = highest_bid.bidder.user
            winner.temp_sale_price = max_bid
            winner.save()
    else:
        raise ValueError("The auction is not active.")

# 返回当前登录用户作为winner的所有记录


def buy_history(request):
    # 假设当前登录用户的ID为1
    user_id = 1  # 你可以替换为 request.user.id

    # 获取当前用户作为winner的记录
    winners = Winner.objects.filter(user_id=user_id, sale_price__isnull=False)

    # 构建响应数据
    data = [{
        'bid_amount': winner.sale_price,
        'property_address': winner.auction.property.address,
    } for winner in winners]

    return JsonResponse({'winners': data})


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
