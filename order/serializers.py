from rest_framework import serializers
from .models import Order , OrderItem , Cart , CartItem
from product.serializers import VendorProductSerializer
from vendor.models import VendorProduct
from django.db import transaction



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'vendor_product', 'quantity', 'price_at_purchase', 'discount_percent']


class OrderSerializer(serializers.ModelSerializer):
    order_orderitems = OrderItemSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status', 'created_at', 'order_orderitems']


class CartItemSerializer(serializers.ModelSerializer):
    vendor_product_id = serializers.IntegerField(write_only=True)
    product_details = VendorProductSerializer(source='vendor_product',read_only=True)

    class Meta:
        model = CartItem
        fields = ['id' , 'quantity' , 'cart_id' , 'vendor_product_id' , 'product_details']
        read_only_fields = ['cart_id']




class CartSerializer(serializers.ModelSerializer):
    cart_cartitems = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id' , 'created_at' , 'cart_cartitems']

    def create(self,validated_data):
        cart_items_data = validated_data.pop('cart_cartitems' ,[])
        user = validated_data.get('user')

        with transaction.atomic():
            cart, created = Cart.objects.get_or_create(user=user)
            try:
                for item_data in cart_items_data:
                    vp_id = item_data.pop('vendor_product_id')
                    vendor_product = VendorProduct.objects.get(id=vp_id)

                    cart_item, item_created = CartItem.objects.get_or_create(
                        cart=cart,
                        vendor_product=vendor_product,
                        defaults={'quantity': item_data.get('quantity', 1)}
                    )

                    if not item_created:
                        cart_item.quantity += item_data.get('quantity', 1)
                        cart_item.save()

            except Exception as e:
                raise serializers.ValidationError({"error": f"Failed to create cart items: {str(e)}"})

        return cart
    
    def update(self, instance, validated_data):
        cart_items_data = validated_data.pop('cart_cartitems', [])

        with transaction.atomic():
            try: 
                for item_data in cart_items_data:
                    vp_id = item_data.get('vendor_product_id')

                    cart_item = instance.cart_cartitems.get(vendor_product=vp_id)
                    cart_item.quantity = item_data.get('quantity', cart_item.quantity)
                    cart_item.save()

            except Exception as e:
                            raise serializers.ValidationError({"error": f"Failed to update cart items: {str(e)}"})

        return instance


