
from rest_framework import permissions, status, views, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Q, Count
from .models import UserHistory, Product, CustomUser, Category, SubCategory
from .serializers import CustomUserSerializer, StateChangeSerializer, ProductSerializer, ProductUpdateSerializer, UserSerializer, CategoryWithProductsSerializer, CategorySerializer, SubCategorySerializer, CustomUserDetailSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from django.db import models
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import Http404

import json
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Aquí puedes añadir cualquier lógica adicional antes de la autenticación
        return super().post(request, *args, **kwargs)
class LoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Obtiene o crea un token para el usuario autenticado
            token, created = Token.objects.get_or_create(user=user)
            # Devuelve el token y el username como respuesta
            return Response({
                'token': token.key,
                'username': username  # Asegúrate de que el manejo del username aquí es seguro y adecuado para tu caso de uso
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas o usuario no encontrado'}, status=status.HTTP_401_UNAUTHORIZED)
def product_shop(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    shop = product.shop
    # Aquí puedes decidir qué información del shop quieres retornar. 
    # Por simplicidad, retornaré el ID y el username/email si es que usas esos campos.
    data = {
        'shop_id': shop.id,
        'shop_name': shop.username,  # Asumiendo que CustomUser tiene un campo username.
    }
    return JsonResponse(data)
class VerifyUserToken(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # Asegura que solo usuarios autenticados pueden hacer la petición

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        token_key = request.data.get('token')

        try:
            usuario = get_object_or_404(CustomUser, pk=user_id)
            token = Token.objects.get(key=token_key)
            user = token.user
            if user.id == user_id:
                return JsonResponse({"success": "El token es válido y corresponde al usuario."}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": "El token no corresponde al user_id proporcionado."}, status=status.HTTP_400_BAD_REQUEST)
        except Token.DoesNotExist:
            return JsonResponse({"error": "Token inválido o no encontrado."}, status=status.HTTP_404_NOT_FOUND)
       
class CreateUserView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProductShopView(views.APIView):
    # Definir las clases de permiso si es necesario, por ejemplo:
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise Http404
        shop = product.shop
        # Aquí adaptas qué información del shop quieres retornar.
        # Asumiendo que CustomUser tiene un campo 'username'.
        data = {
            'shop_id': shop.id,
            'razon_social': shop.razon_social, # O cualquier campo que represente el nombre del shop.
            'telefono': str(shop.telefono),
            'email': str(shop.email),
        }
        return Response(data, status=status.HTTP_200_OK)
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class UpdateUserView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            original_data = json.dumps(serializer.initial_data)
            updated_user = serializer.save()
            UserHistory.objects.create(
                user=updated_user,
                modified_by=request.user,
                motive=serializer.validated_data.get('motive', ''),
                changes=original_data
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangeUserStateView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = StateChangeSerializer(data=request.data)
        if serializer.is_valid():
            user.state = serializer.validated_data['state']
            user.save()

            UserHistory.objects.create(
                user=user,
                modified_by=request.user,
                changes=f"State changed to {user.state}",
                motive=serializer.validated_data.get('motive', '')
            )
            return Response({'status': 'state changed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {'request': self.request}
    
class CustomUserDetailView(generics.ListAPIView):
    serializer_class = CustomUserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Sobrescribe el método para retornar un queryset que contiene
        solo el usuario especificado por el username en la URL.
        """
        username = self.kwargs['username']
        return CustomUser.objects.filter(username=username)
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(shop=self.request.user)
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class ProductUpdateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        product = Product.objects.filter(pk=pk, shop=request.user).first()
        if not product:
            return Response({'detail': 'Producto no encontrado o permiso denegado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductUpdateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProductsByShopView(views.APIView):
    def get(self, request, shop_id):
        products = Product.objects.filter(shop_id=shop_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
class CategoriesWithProductsView(views.APIView):
    def get(self, request):
        # Aquí nos aseguramos de contar los productos correctamente y filtrar basado en esa cuenta.
        categories_with_products = Category.objects.annotate(
            products_count=Count('subcategories__products', distinct=True)
        ).filter(products_count__gt=0).distinct()

        serializer = CategorySerializer(categories_with_products, many=True)
    
        return Response(serializer.data)
class ProductsByCategory(views.APIView):
    def get(self, request, category_id):
        try:
            # Ahora filtramos productos solo por 'category_id'
            products = Product.objects.filter(subcategory__category_id=category_id).order_by('-created_at')
            page = request.query_params.get('page', 1)
            limit = request.query_params.get('limit', 10)
            paginator = Paginator(products, limit)
            paginated_products = paginator.get_page(page)
            
            serializer = ProductSerializer(paginated_products.object_list, many=True)
            return Response({
                'results': serializer.data,
                'total': paginator.count,
                'pages': paginator.num_pages,
                'current': paginated_products.number
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class ProductsByCategoryShop(views.APIView):
    def get(self, request, shop_id, category_id):
        try:
            # Ordena los productos por 'created_at' antes de paginar
            products = Product.objects.filter(shop_id=shop_id, subcategory__category_id=category_id).order_by('-created_at')
            page = request.query_params.get('page', 1)
            limit = request.query_params.get('limit', 10)
            paginator = Paginator(products, limit)
            paginated_products = paginator.get_page(page)
            
            serializer = ProductSerializer(paginated_products, many=True)
            return Response({
                'results': serializer.data,
                'total': paginator.count,
                'pages': paginator.num_pages,
                'current': paginated_products.number
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductsByShopAndSubcategoryView(views.APIView):
    def get(self, request, shop_id, subcategory_id):
        products = Product.objects.filter(shop_id=shop_id, subcategory_id=subcategory_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductsByShopAndBestDiscountView(views.APIView):
    def get(self, request, shop_id):
        # Si shop_id es -1, busca todos los productos de todos los negocios y ordena por los mejores descuentos
        if shop_id == "-1":
            products = Product.objects.all().order_by('-discount')[:15]
        else:
            # De lo contrario, filtra los productos por shop_id
            products = Product.objects.filter(shop_id=shop_id).order_by('-discount')
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductsSearchView(views.APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        products = Product.objects.filter(
            Q(shop__razon_social__icontains=query) |
            Q(name__icontains=query) |
            Q(subcategory__name__icontains=query) |
            Q(subcategory__category__name__icontains=query)
        )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            product = self.queryset.get(pk=kwargs['pk'], shop=request.user)
            self.perform_destroy(product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
class CategoriesWithProductsView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithProductsSerializer
    
class CategoriesByShopView(views.APIView):
    def get(self, request, shop_id):
        # Obtiene los productos de la tienda y luego las categorías distintas
        products = Product.objects.filter(shop_id=shop_id)
        categories_ids = products.values_list('subcategory__category', flat=True).distinct()
        categories = Category.objects.filter(id__in=categories_ids)
        
        # Serializa las categorías
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
class SubCategoryList(views.APIView):
    def get(self, request, format=None):
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data)
    
class CategoryPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    
class ShopCategoriesAPIView(views.APIView):
    def get(self, request, shop_id):
        try:
            shop = CustomUser.objects.get(id=shop_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Tienda no encontrada.'}, status=404)

        categories = Category.objects.filter(shop_products__shop=shop).distinct()
        paginator = CategoryPagination()
        paginator.page_size = request.query_params.get('limit', 1)  # Default to 10 items per page
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
def search_products(request):
    search_query = request.GET.get('query', '')
    query_filters = Q()

    if search_query != "":
        # Divide el string de búsqueda en palabras clave individuales
        keywords = search_query.split()

        # Para cada palabra clave, añade condiciones OR al filtro de búsqueda
        for keyword in keywords:
            query_filters |= Q(name__icontains=keyword) | \
                             Q(description__icontains=keyword) | \
                             Q(subcategory__name__icontains=keyword) | \
                             Q(subcategory__category__name__icontains=keyword)

        # Filtra los productos que coinciden con las palabras clave, limitando a 100 resultados
        products = Product.objects.filter(query_filters, state='active')[:100]
    else:
        # Si search_query está vacío, ordena los productos por mayor descuento
        # Puedes ajustar el criterio de "mejores ofertas" según tus necesidades
        products = Product.objects.filter(state='active').order_by('-discount')[:100]

    # Prepara los datos de los productos para la respuesta JSON
    products_data = list(products.values('id', 'name', 'description', 'price', 'barcode', 'image_base64', 'discount', 'created_at', 'subcategory__name', 'subcategory__category__name'))

    return JsonResponse({'products': products_data})