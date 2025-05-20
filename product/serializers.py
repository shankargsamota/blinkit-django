from rest_framework import serializers
from django.contrib.auth import authenticate
from product.models import Product
from vendor.models import VendorProduct


class VendorProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source="vendor.name", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_description = serializers.CharField(source="product.description", read_only=True)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = VendorProduct
        fields = ["id","vendor","vendor_name", "product", "product_name", "product_description", "price", "discount_percent" , "discounted_price"]

    def discounted_price(self,obj):
        if obj.discount_percent:
            return round(obj.price - (obj.price * obj.discount_percent / 100), 2)
        return obj.price 
    



class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price" , "discounted_price" , "stock"]


    # def update(self, instance, validated_data):
    #     """Allow partial updates without requiring all fields."""
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)  # Update only provided fields
    #     instance.save()
    #     return instance
    
    def get_discounted_price(self,obj):
        request = self.context.get('request') # cannot use self.request as request is send in context to serializer
        if request and hasattr(request.user, 'vendor'):  # Ensure the user is a vendor
            vendor = request.user.vendor
            vendor_product = VendorProduct.objects.filter(vendor=vendor, product=obj).order_by("-discount_percent").first()
            
            if vendor_product and vendor_product.discount_percent:
                discount = vendor_product.discount_percent
                if discount > 0:
                    discounted_price = obj.price - (obj.price * discount / 100)
                    return round(discounted_price, 2)

        return obj.price
