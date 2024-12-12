from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.contrib.auth.password_validation import validate_password

# Create your models here.
class Customer(models.Model):
    GENDER_CHIOCES = [
        ('male', 'MALE'),
        ('female', 'FEMALE'),
        ('other','OTHER'),
        ]
    address = models.CharField(max_length=200)
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHIOCES)
    phone_number = models.IntegerField()

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Product: {self.product_name}"

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=200)
    order_products = models.ManyToManyField(Product, through='OrderProduct')


class OrderProduct(models.Model):
    order = models.ForeignKey(Product, on_delete=models.CASCADE)
    product = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    #slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Category: {self.name}"


class Profile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="media/", blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extrafields):
        if not username:
            raise ValueError("username must be provided")
        if not email:
            raise ValueError("email must be provided")
        else:
            try:
                validate_email(email)
            except ValidationError:
                raise ValueError("Invalid email address")
        if not password:
            raise ValueError("password must be provided")
        else:
            validate_password(password)
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, password=password, **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extrafields):
        extrafields.setdefault("is_staff", True)
        extrafields.setdefault("is_superuser", True)
        
        if extrafields.get("is_staff") is not True:
            raise ValueError("is_staff attribute must be True")
        if extrafields.get("is_superuser") is not True:
            raise ValueError("is_superuser attribute must be True")
        
        
        user = self.create_user(username, email, password, **extrafields)
        user.save(using=self._db)
        return user


class CustomUser(PermissionsMixin,AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(editable=True, null=True, blank=True)
    gender = models.CharField(max_length=20)
    email = models.EmailField(unique=True, max_length=200, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()
