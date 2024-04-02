import os
from django.conf import settings
from rest_framework import serializers
from .models import Property, Bid, Bidder

class PropertySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            'id', 'category', 'start_bid_amount', 'seller_id', 'created_at',
            'property_descr', 'title', 'is_active', 'address', 'squarefeet', 'room_type', 'image_url'
        )
    
    def get_image_url(self, obj):
        if obj.image_url:
            # Generate the full URL for the image
            request = self.context.get('request')
            relative_path = os.path.relpath(obj.image_url.path, settings.MEDIA_ROOT)
            return request.build_absolute_uri(settings.MEDIA_URL + relative_path)
        return None  # Or a placeholder image URL if necessary
# class PropertySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Property
#         fields = '__all__'

# class BidSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bid
#         fields = '__all__'  # 或者列出你希望包含在序列化/反序列化过程中的字段
        
class BidSerializer(serializers.ModelSerializer):
    bidder_id = serializers.SerializerMethodField()
    # bidder = serializers.PrimaryKeyRelatedField(queryset=Bidder.objects.all())
    # auction = serializers.PrimaryKeyRelatedField(queryset=Auction.objects.all())
    

    class Meta:
        model = Bid
        # fields = ['id', 'amount', 'bidder_user_id', 'auction_id']   # 你可能需要列出所有字段，包括bidder_user_id
        fields = '__all__' 
        # fields = ('id', 'bidder', 'auction', 'amount', 'bidder_user_id',)
    def get_bidder_id(self, obj):
        return obj.bidder.id
    # def create(self, validated_data):
    #     validated_data['bidder'] = Bidder.objects.get(pk=validated_data.pop('bidder_id', None))
    #     validated_data['auction'] = Auction.objects.get(pk=validated_data.pop('auction_id', None))
    #     return super().create(validated_data)
    def create(self, validated_data):
    # 假定Bidder ID为1
        # bidder_instance = Bidder.objects.get(pk=1)
        # validated_data['bidder'] = bidder_instance
        validated_data['bidder'] = Bidder.objects.get(pk=1)
        # 对于auction, 从validated_data中获取auction_id并找到对应的Auction实例
        validated_data['auction'] = Auction.objects.get(pk=validated_data.pop('auction_id', None))
        
        # 调用super().create()创建Bid实例
        return super().create(validated_data)
    

class BidderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Bidder
        fields = ['user']
