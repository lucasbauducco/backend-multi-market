from rest_framework import serializers
from .models import CustomUser, Product, SubCategory, Category
from django.contrib.auth.models import User
from rest_framework import serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'razon_social', 'telefono', 'email']
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_type', 'state', 'motive', 'cuit', 'razon_social','telefono', 'domicilio_fiscal', 'ingresos_brutos', 'inicio_actividades']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Implementa la lógica de actualización aquí, si es necesario
        return super().update(instance, validated_data)
    
class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # Se incluyen todos los campos excepto 'password'
        fields = ['id', 'username', 'email', 'user_type', 'state', 'cuit', 'razon_social','telefono', 'domicilio_fiscal', 'ingresos_brutos', 'inicio_actividades']
    
class StateChangeSerializer(serializers.Serializer):
    state = serializers.CharField(max_length=100)
    motive = serializers.CharField(max_length=200, required=False)

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    def validate_state(self, value):
        if value not in ['active', 'inactive', 'paused', 'eliminate']:
            raise serializers.ValidationError("El estado debe ser 'active' o 'inactive'.")
        return value
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'shop', 'name', 'description', 'price', 'barcode', 'discount', 'image_base64', 'subcategory']

    def create(self, validated_data):
        # Here, you can add logic to handle shop assignment based on the request or other logic
        # For example, using the request user if the shop is not explicitly provided:
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            shop_user = request.user
            validated_data['shop'] = shop_user
        return Product.objects.create(**validated_data)
        
class SubCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'products']

class CategoryWithProductsSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'subcategories']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']