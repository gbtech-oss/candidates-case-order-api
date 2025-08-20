from rest_framework import serializers
from .models import Order, Item, DeliveryAddress

class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['street_name', 'number', 'complement', 'reference_point']


class ItemSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Item
        fields = ['id', 'name', 'quantity', 'unit_price']

    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError("O preço unitário não pode ser negativo.")
        return value
    
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("A quantidade não pode ser negativa.")
        return value

class OrderSerializer(serializers.ModelSerializer):

    delivery_address = DeliveryAddressSerializer(required=False, allow_null=True)
    items = ItemSerializer(many=True, required=False)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'client_name',
            'client_document',
            'delivery_date',
            'delivery_address',
            'created_at',
            'updated_at',
            'items',
            'total_price',
        ]
        read_only_fields = ['created_at', 'updated_at', 'total_price']

    def get_total_price(self, obj):
        return sum(item.quantity * item.unit_price for item in obj.items.all())


    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        address_data = validated_data.pop('delivery_address', None)
        address = None
        if address_data:
            address = DeliveryAddress.objects.create(**address_data)
        order = Order.objects.create(delivery_address=address, **validated_data)
        for item_data in items_data:
            Item.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        address_data = validated_data.pop('delivery_address', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if address_data:
            if instance.delivery_address:
                for attr, value in address_data.items():
                    setattr(instance.delivery_address, attr, value)
                instance.delivery_address.save()
            else:
                instance.delivery_address = DeliveryAddress.objects.create(**address_data)
        instance.save()
        if items_data:
            for item_data in items_data:
                Item.objects.create(order=instance, **item_data)
        return instance
