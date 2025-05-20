from django.db import models
from account.models import User
from product.models import Product


# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class VendorProduct(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_vendorproducts', related_query_name='vendor_vendorproduct')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_vendorproducts', related_query_name='product_vendorproduct')
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Vendor-specific price
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Vendor-specific discount

    class Meta:
        unique_together = ('vendor', 'product')  # Each vendor can have only one entry per product.

    def discounted_price(self):
        return self.price * (1 - self.discount_percent / 100)

    def __str__(self):
        return f"{self.product.name} by {self.vendor.name}"
