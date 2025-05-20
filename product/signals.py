from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
from django.core.cache import cache 
from vendor.models import Product


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_product_list_cache(sender, **kwargs):
    
    if hasattr(cache, '_cache'):
        try:
            keys = list(cache._cache.keys())
            print(keys,"keys")  # Only works with LocMemCache
            vendor_keys = [key for key in keys if 'vendorproductviewset' in str(key).lower()]
            print(vendor_keys,"vendor_keys")
            for key in vendor_keys:
                print("Deleting cache key:", key)
                cache.delete(key)
        except Exception as e:
            print(e,"print")        