from rest_framework import viewsets, permissions , mixins
from django.db import transaction
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer , CartSerializer , CartItemSerializer
from .models import Order , OrderItem , Cart , CartItem
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from vendor.models import VendorProduct
from core.tasks import send_email_task


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer


##### list, retrieve, create for CartViewSet
class CartViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin):
    permission_classes = [IsCustomer]
    queryset = Cart.objects.prefetch_related('cart_cartitem')
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related('cart_cartitems')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class QuantityUpdateMixin:
    @action(detail=True, methods=['post'], url_path='increase')
    def increase_quantity(self,request,pk=None):
        cart_item = self.get_object()
        cart_item.quantity += 1
        cart_item.save()
        return Response({'quantity': cart_item.quantity}, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['post'], url_path='decrease')
    def decrease_quantity(self,request,pk=None):
        cart_item = self.get_object()
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return Response({'quantity': cart_item.quantity}, status=status.HTTP_200_OK)
        else:
            cart = cart_item.cart
            with transaction.atomic():
                cart_item.delete()
                if not cart.cart_cartitems.exists():
                    cart.delete()
            return Response({'message': 'Cart item deleted as quantity reached 0'}, status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(QuantityUpdateMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    permission_classes = [IsCustomer]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart = cart_item.cart
        with transaction.atomic():
            cart_item.delete()
            if not cart.cart_cartitems.exists():
                cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        return super().update(request, *args, **kwargs)
    


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCustomer]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

    def perform_create(self, serializer):  # called by create , used to create orderitem model
        user = self.request.user

        products_data = self.request.data.get('products', [])
        if not products_data:
            raise serializers.ValidationError({'products': 'This field is required and must contain at least one product.'})

        total_price = 0

        try:
            with transaction.atomic():

                order = serializer.save(user=user)

                for product_data in products_data:
                    vendor_product_id = product_data.get('vendor_product_id')
                    quantity = int(product_data.get('quantity', 1))

                    if not vendor_product_id:
                        raise serializers.ValidationError({'product_id': 'Each product must have an ID.'})

                    try:
                        product = VendorProduct.objects.get(id=vendor_product_id)
                    except VendorProduct.DoesNotExist:
                        raise serializers.ValidationError({'product_id': f'Product with ID {vendor_product_id} not found.'})

                    discounted_price = product.discounted_price()
                    
                    item_total = discounted_price * quantity
                    total_price += item_total

                    OrderItem.objects.create(
                        order=order,
                        vendor_product=product,
                        quantity=quantity,
                        price_at_purchase=discounted_price,
                        discount_percent = product.discount_percent
                    )

                order.total_price = total_price
                order.save()

                #send mail
                print(user)
                send_email_task.delay(
                    subject='Your order has been placed!',
                    message=f'Hi {user.first_name},\n\nYour order #{order.id} has been placed successfully!\nTotal Amount: ₹{total_price}\n\nThank you for shopping with us!',
                    recipient_list=[user.email],
                )

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

