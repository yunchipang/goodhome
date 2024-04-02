
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .forms import BidForm
# Create your views here.
from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer, BidSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bid
from rest_framework.permissions import AllowAny

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
