import os
from django.conf import settings
from rest_framework import serializers
<<<<<<< HEAD
from .models import Property, Bid, Bidder, Auction
=======
from .models import Property

>>>>>>> c75839c (build async chat server)


class PropertySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            'id', 'category', 'start_bid_amount', 'seller_id', 'created_at',
            'property_descr', 'title', 'is_active', 'address', 'squarefeet', 'room_type', 'zipcode', 'image_url'
        )

    def get_image_url(self, obj):
        if obj.image_url:
            # Generate the full URL for the image
            request = self.context.get('request')
            relative_path = os.path.relpath(
                obj.image_url.path, settings.MEDIA_ROOT)
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
