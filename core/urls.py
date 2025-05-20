
from django.contrib import admin
from django.urls import path , include
from account.views import SignupView, LoginView
from product.views import ProductViewSet , VendorProductViewSet
from order.views import OrderViewSet , CartViewSet , CartItemViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'vendor-product', ProductViewSet)
router.register(r'product', VendorProductViewSet)
router.register(r'order' , OrderViewSet)
router.register(r'cart' , CartViewSet)
router.register(r'cart-item' , CartItemViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('user/signup', SignupView.as_view(), name='signup'),
    path('user/login', LoginView.as_view(), name='login'),


    # path('product/all', VendorProductViewSet.as_view({'get': 'list'}), name='get-products'),
    # path('product/<int:product_id>', VendorProductViewSet.as_view({'get': 'retrieve'}), name='get-product-details'),

    path('', include(router.urls))
    # is-vendor
    # path('vendor-product', ProductViewSet.as_view({'get': 'list'}), name='get-products'),
    # path('vendor-product/<int:pk>', ProductViewSet.as_view({'get': 'retrieve'}), name='get-product-details'),
    # path('vendor-product', ProductViewSet.as_view({'post': 'create'}), name='add-product'),
    # path('vendor-product/<int:pk>', ProductViewSet.as_view({'put': 'update', 'patch': 'update'}), name='update-product'),

    # path('order' , OrderViewSet.as_view({'get' : 'list'}))



]
