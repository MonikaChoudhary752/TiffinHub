from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, first_name, last_name, address,is_vendor=False, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, first_name=first_name, last_name=last_name, address=address,is_vendor=is_vendor, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff' , True)
        extra_fields.setdefault('is_superuser' , True)
        extra_fields.setdefault('is_active' , True)

        email = self.normalize_email(email)
        user = self.model(
            email=email, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using = self.db)

        return user


class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = None
    email = models.EmailField(unique=False)
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.TextField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_vendor = models.BooleanField(default=False, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'address']

    def __str__(self):
        return self.phone_number
    

class VendorInformation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='vendor_information')
    menu = models.TextField()
    business_name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to="media")
    price = models.CharField(max_length=20, default = "Rs. 0/-")

    def __str__(self):
        return self.business_name

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorInformation, on_delete=models.CASCADE)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    date_unsubscribed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.vendor}'

    class Meta:
        unique_together = ['user', 'vendor']

    @staticmethod
    def was_subscribed(user, vendor):
        return Subscription.objects.filter(user=user, vendor=vendor, date_unsubscribed__isnull=False).exists()

    @staticmethod
    def is_subscribed(user, vendor):
        return Subscription.objects.filter(user=user, vendor=vendor, date_unsubscribed__isnull=True).exists()