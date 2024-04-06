# views.py
import datetime
from django.http import HttpResponseBadRequest, JsonResponse
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
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bid, Auction, User,Bidder, Winner
from rest_framework.permissions import AllowAny
from datetime import datetime
from django.db.models import Max
from django.utils import timezone
from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now


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
            temp_sale_price = winner.temp_sale_price if winner.temp_sale_price is not None else Decimal('0.00')
            # 如果不是新创建的，并且新的出价高于当前的临时最高出价，则更新
            if not created and amount > temp_sale_price:
                winner.temp_sale_price = amount
                winner.user = bidder.user  # 更新最高出价者
                winner.save()


            # 创建并保存新的出价记录
            bid = Bid.objects.create(amount=amount, auction=auction, bidder=bidder)
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
def submit_bid(auction_id, bidder_id, amount):
    now = timezone.now()
    auction = Auction.objects.get(pk=auction_id)

    # 确保竞拍仍在进行中
    if auction.start_time <= now <= auction.end_time:
        Bid.objects.create(bidder_id=bidder_id, auction_id=auction_id, amount=amount)
        
        # 更新临时最高出价
        max_bid = Bid.objects.filter(auction_id=auction_id).aggregate(Max('amount'))['amount__max']
        highest_bid = Bid.objects.filter(auction_id=auction_id, amount=max_bid).first()
        
        # 检查是否已存在获胜者记录
        winner, created = Winner.objects.get_or_create(auction_id=auction_id, defaults={'user': highest_bid.bidder.user, 'temp_sale_price': max_bid})
        if not created:
            winner.user = highest_bid.bidder.user
            winner.temp_sale_price = max_bid
            winner.save()
    else:
        raise ValueError("The auction is not active.")


