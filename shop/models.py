from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import base64
import json
from django.core.files.base import ContentFile
from phonenumber_field.modelfields import PhoneNumberField
class User_Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
# Create your models here.
class UserType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    user_categories = models.ManyToManyField(User_Category)
    def __str__(self):
        return self.name
class State(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
class CustomUser(AbstractUser):
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    cuit = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=100)
    domicilio_fiscal = models.CharField(max_length=200)
    ingresos_brutos = models.CharField(max_length=50)
    inicio_actividades = models.DateField(null=True, blank=True)
    telefono = PhoneNumberField(null=True, blank=True, unique=True, region="AR")
class UserHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='history')
    modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='modified_users')
    modified_at = models.DateTimeField(auto_now_add=True)
    motive = models.CharField(max_length=200, blank=True, null=True)
    changes = models.TextField()

    def __str__(self):
        return f"History for {self.user.username} modified by {self.modified_by.username} at {self.modified_at}"
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    shop = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shop_products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    barcode = models.CharField(max_length=100, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    image_base64 = models.TextField(blank=True, null=True)  # Campo para almacenar imagen en base64
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=12, default='active', choices=(('active', 'Active'), ('inactive', 'Inactive')))
    def __str__(self):
        return self.name

    def set_image_from_base64(self, base64_str):
        """
        Decodifica una imagen en formato base64 y la guarda en el campo de imagen.
        """
        if base64_str:
            format, imgstr = base64_str.split(';base64,') 
            ext = format.split('/')[-1] 
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            self.image.save(name=self.name + '.' + ext, content=data, save=False)

    def get_image_as_base64(self):
        """
        Devuelve la imagen en formato base64.
        """
        try:
            with open(self.image.path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except (ValueError, FileNotFoundError):
            return None
        
