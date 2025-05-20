from django.db import models
from django.conf import settings
from vendor.models import VendorProduct


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_carts' , related_query_name='user_cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_cartitems', related_query_name='cart_cartitem')
    vendor_product  = models.ForeignKey(VendorProduct, on_delete=models.CASCADE, related_name='vendorprod_cartitems', related_query_name='vendorprod_cartitem')
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.vendor_product.discounted_price() * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.vendor_product.product.name} in {self.cart}"
    


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_orders', related_query_name='user_order')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} ({self.status})"
    
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_orderitems', related_query_name='order_orderitem')
    vendor_product = models.ForeignKey(VendorProduct, on_delete=models.SET_NULL, null=True, related_name='vendorprod_orderitems', related_query_name='vendorprod_orderitem')
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.order.user.username} - {self.store_product.product.name} ({self.quantity})"

    def get_total_price(self):
        return self.quantity * self.price_at_purchase