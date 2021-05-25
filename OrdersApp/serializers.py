from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.relations import PrimaryKeyRelatedField

from OrdersApp.models import Order, Stock
from OrdersApp.utils import utc_now, utc_timestamp, utc_datetime


class OrderSerializer(serializers.Serializer):
    isin = serializers.CharField(min_length=12, max_length=12)
    limit_price = serializers.FloatField(min_value=0, allow_null=True)
    side = serializers.CharField()
    valid_until = serializers.IntegerField(min_value=0)
    quantity = serializers.IntegerField(min_value=0)

    def __init__(self, instance=None, data=empty, **kwargs) -> None:
        super().__init__(instance, data, **kwargs)
        self.now = self.context.get('now', utc_now())

    def validate(self, attrs):
        try:
            Stock.objects.get(isin=attrs.get('isin'))
        except Stock.DoesNotExist:
            raise serializers.ValidationError({'isin': "Stock ISIN does not exist"})
        if attrs.get('valid_until') < utc_timestamp(self.now):
            raise serializers.ValidationError({'valid_until': "valid_until is in the past"})
        if attrs.get('side').lower() not in ('buy', 'sell'):
            raise serializers.ValidationError({'side': "side must be 'buy' or 'sell'"})

        return attrs

    def create(self, validated_data):
        validated_data['side'] = validated_data.get('side').lower() == 'buy'
        validated_data['valid_until'] = utc_datetime(validated_data.get('valid_until'))
        validated_data['stock'] = Stock.objects.get(isin=validated_data.pop('isin'))
        return Order.objects.create(**validated_data)


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('isin', 'name')
