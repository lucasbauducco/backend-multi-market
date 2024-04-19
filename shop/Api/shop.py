from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.http import Http404
from shop.models import Product
from shop.serializers import ShopSerializer
class ProductShopView(views.APIView):
    """
    Vista para obtener información sobre la tienda asociada a un producto específico.
    
    Métodos:
    - GET: Retorna información de la tienda asociada a un producto dado.
    """

    # Opcional: Definir clases de permiso si es necesario.
    # Descomenta la siguiente línea si deseas restringir el acceso a usuarios autenticados.
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        """
        Obtiene y retorna información sobre la tienda de un producto específico.
        
        Parámetros:
        - request: HttpRequest, contiene información sobre la solicitud HTTP.
        - product_id: int, el ID del producto del cual se desea obtener información de la tienda.
        
        Retorna:
        - Response: Contiene información sobre la tienda del producto.
        """
        try:
            product = Product.objects.get(id=product_id)
            shop = product.shop
        except Product.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Usando un serializador para la tienda
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ShopProductsListView(views.APIView):
    model = Product
    template_name = 'shop_products_list.html'  # Specify your template name
    context_object_name = 'products'

    def get_queryset(self):
        """
        Override the get_queryset method to return products
        related to a specific shop.
        """
        shop_id = self.kwargs.get('shop_id')
        return Product.objects.filter(shop__id=shop_id, state='active').order_by('-created_at')