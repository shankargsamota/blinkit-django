# from rest_framework_extensions.cache.mixins import CacheResponseMixin


def custom_cache_key_func(view_instance, view_method, request, args, kwargs):
    view_class_name = view_instance.__class__.__name__.lower()
    method_name = view_method.__name__
    return f'{view_class_name}:{method_name}'


# class CustomCacheResponseMixin(CacheResponseMixin):
#     object_cache_key_func = staticmethod(custom_cache_key_func)
#     list_cache_key_func = staticmethod(custom_cache_key_func)
#     object_cache_timeout = 60 * 5
#     list_cache_timeout = 60 * 5
