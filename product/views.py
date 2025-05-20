from rest_framework import viewsets, permissions , filters
from .models import Product 
from vendor.models import VendorProduct
from .serializers import ProductSerializer , VendorProductSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from core.pagination import CustomPagination
# from product.mixins import CustomCacheResponseMixin


class IsVendorOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        vendor_product = VendorProduct.objects.filter(product=obj,vendor=request.user.vendor).first()
        return vendor_product is not None


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated ,IsVendorOwner]
    lookup_field = 'pk'

    def get_queryset(self):
        if hasattr(self.request.user, 'vendor'):
            return Product.objects.filter(product_vendorproduct__vendor=self.request.user.vendor)
        return Product.objects.none() 

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated, IsVendorOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):  # called by create , used to create vendorproduct model

        if not hasattr(self.request.user, 'vendor'):  # only a vendor user can create product
            raise PermissionDenied("You must be a vendor to add products.")
        
        product = serializer.save()
        vendor = self.request.user.vendor 
        VendorProduct.objects.create(vendor=vendor, product=product, price=product.price)


    def perform_update(self,serializer):   # called by update , used to update vendorproduct model

        if not hasattr(self.request.user, 'vendor'):  # only a vendor user can create product
            raise PermissionDenied("You must be a vendor to add products.")
        
        product = serializer.instance
        updated_product = serializer.save(partial=True)  

        new_price = self.request.data.get('price')
        if new_price is not None:
            vendor = self.request.user.vendor  # Get the vendor
            vendor_product = VendorProduct.objects.filter(vendor=vendor, product=product).first()

            if vendor_product:
                vendor_product.price = new_price
                vendor_product.save()
            else:
                VendorProduct.objects.create(vendor=vendor, product=product, price=new_price)

    def update(self, request, *args, **kwargs):

        if not hasattr(self.request.user, 'vendor'):  # only a vendor user can create product
            raise PermissionDenied("You must be a vendor to add products.")

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Ensure `partial=True`
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



# class VendorProductViewSet(CustomCacheResponseMixin, viewsets.ModelViewSet):
class VendorProductViewSet(viewsets.ModelViewSet):
    queryset = VendorProduct.objects.all().order_by('id') 
    serializer_class = VendorProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product__name', 'vendor__name']
    ordering_fields = ['price']
    ordering = ['id']  # default ordering

    lookup_field = 'product_id'

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        if product_id:
            return VendorProduct.objects.filter(product_id=product_id).order_by('-id') 
        return VendorProduct.objects.all().order_by('-id')
    

