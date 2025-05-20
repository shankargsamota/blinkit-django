from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager



# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)  #normalize_email keeps the domain part in small case
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    
    location = models.CharField(max_length=255, blank=True, null=True) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email




# class Address(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_addresses', related_query_name='user_address')
#     street = models.CharField(max_length=255)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=20)
#     add_type = models.CharField(max_length=100,default='home')


#     def __str__(self):
#         return f"{self.street}, {self.city}, {self.state}, {self.country} - {self.postal_code}"


