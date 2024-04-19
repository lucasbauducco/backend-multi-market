from django.db.models import Count
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from shop.models import Category, CustomUser, Product  # Asegúrate de tener el import correcto aquí
from shop.serializers import CategorySerializer, CategoryWithProductsSerializer  # Asegúrate de tener el import correcto aquí

class CategoryList(generics.ListAPIView):
    """
    Vista para listar todas las categorías disponibles.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoriesWithProductsView(generics.ListAPIView):
    """
    Vista para listar todas las categorías que tienen al menos un producto.
    """
    serializer_class = CategoryWithProductsSerializer

    def get_queryset(self):
        return Category.objects.annotate(
            products_count=Count('subcategories__products', distinct=True)
        ).filter(products_count__gt=0).distinct()

class CategoriesByShopView(generics.ListAPIView):
    """
    Vista para listar categorías basadas en una tienda específica.
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        products = Product.objects.filter(shop_id=shop_id)
        categories_ids = products.values_list('subcategory__category', flat=True).distinct()
        return Category.objects.filter(id__in=categories_ids)

class CategoryPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 10  # Default to 10 items per page
    max_page_size = 100

class ShopCategoriesAPIView(generics.ListAPIView):
    """
    Vista para listar categorías de una tienda específica con paginación.
    """
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        try:
            shop = CustomUser.objects.get(id=shop_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Tienda no encontrada.'}, status=404)
        return Category.objects.filter(shop_products__shop=shop).distinct()