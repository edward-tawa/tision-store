from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from carstore.models import CustomUser,Product,Customer, Category, Order, OrderProduct, Profile
from django.contrib.auth.models import Group
from django import forms

# Register your models here.
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Password_1", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password_2", widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder":"Firstname"}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder":"Lastname"}))
    date_of_birth = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={"type":"date"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"type":"email"}))

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "date_of_birth","gender", "email"]

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError("password length must be at least 8 characters")        
        if not any(char.isdigit() for char in password1):
            raise ValidationError("there should be at least 1 digit")
        if not any(char.isalpha for char in password1):
            raise ValidationError("there should be at least 1 character")
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("passwords should match")
        return password2
        
        


class UserChangeForm(forms.ModelForm):
    
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name",
                  "date_of_birth", "gender", "email"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = CustomUserCreationForm
    
    list_display = ["id", "username", "first_name", "last_name", "date_of_birth", "gender", "email"]
    
    fieldsets = [
        ("Fields", {"fields": ["username", "first_name", "last_name", "date_of_birth", "gender", "email"]}),
        ]

    add_fieldsets = [
        (None, {
            "classes":["wide"],
            "fields":["username", "first_name", "last_name", "date_of_birth", "gender", "email"]
        }),
        ("Credentials", {"fields": ["password1","password2"]}),
    ]
    
    ordering = ["email"]

class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "address", "user", "phone_number", "gender"]

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "product_name", "description", "quantity", "price", "category", "image", "created_at", "updated_at"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_date", "customer", "order_status"]
    

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "unit_price"]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "bio", "profile_picture", "phone_number"]


admin.site.register(Category, CategoryAdmin)

admin.site.register(Customer, CustomerAdmin)

admin.site.register(Product, ProductAdmin)

admin.site.register(Order, OrderAdmin)

admin.site.register(OrderProduct, OrderProductAdmin)

admin.site.register(Profile, ProfileAdmin)

admin.site.register(CustomUser, UserAdmin)

admin.site.unregister(Group)