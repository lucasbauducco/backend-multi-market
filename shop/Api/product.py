from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q

from shop.models import Product, CustomUser  # Ajusta según la ubicación de tus modelos
from shop.serializers import ProductSerializer, ProductUpdateSerializer
def product_shop(request, product_id):
    """
    Función para obtener la tienda asociada a un producto dado su ID.
    Retorna información básica de la tienda como el ID y nombre/username.
    """
    product = get_object_or_404(Product, id=product_id)
    shop = product.shop
    # Aquí puedes decidir qué información del shop quieres retornar. 
    data = {
        'shop_id': shop.id,
        'shop_name': shop.username,  # Asumiendo que CustomUser tiene un campo username.
    }
    return JsonResponse(data)

class ProductListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar y crear productos.

    Esta vista proporciona endpoints para:
    - Obtener una lista de todos los productos.
    - Crear un nuevo producto.

    La vista utiliza el serializador `ProductSerializer` para validar y deserializar los datos de entrada,
    y serializar las instancias de `Product` para la respuesta.

    Los usuarios deben estar autenticados para acceder a esta vista, como se indica en `permission_classes`.

    Atributos:
        serializer_class (Serializer): El serializador que se utiliza para la validación y serialización de datos.
        permission_classes (list): Una lista de clases de permiso que determina quién puede acceder a esta vista.
        queryset (QuerySet): El conjunto de consultas utilizado para listar los productos. Por defecto, lista todos los productos.

    Métodos:
        get_serializer_context(self): Extiende el contexto proporcionado al serializador, añadiendo la solicitud actual.
    """

    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()

    def get_serializer_context(self):
        """
        Proporciona contexto adicional al serializador.

        Este método extiende el contexto del serializador para incluir la solicitud actual.
        Esto es útil, por ejemplo, cuando el serializador necesita acceder a datos de la solicitud
        para realizar alguna lógica específica como acceder al usuario que realiza la solicitud.

        Returns:
            dict: Un diccionario que extiende el contexto predeterminado del serializador con la solicitud actual.
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

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
def search_products(request):
    search_query = request.GET.get('query', '').strip()
    products_data = []
    if search_query:
        # Primero intenta buscar si la consulta coincide con una tienda específica por razón social
        shop = CustomUser.objects.filter(razon_social__icontains=search_query).first()
        if shop:
            # Si se encuentra una tienda, devuelve todos los productos activos de esa tienda
            products = shop.shop_products.filter(state='active').order_by('-discount')[:100]
        else:
            # Si no se encuentra una tienda, realiza la búsqueda por palabras clave en los productos
            keywords = search_query.split()
            query_filters = Q(state='active') & (
                Q(name__icontains=keywords[0]) |
                Q(description__icontains=keywords[0]) |
                Q(subcategory__name__icontains=keywords[0]) |
                Q(subcategory__category__name__icontains=keywords[0])
            )

            for keyword in keywords[1:]:
                query_filters |= (
                    Q(name__icontains=keyword) |
                    Q(description__icontains=keyword) |
                    Q(subcategory__name__icontains=keyword) |
                    Q(subcategory__category__name__icontains=keyword)
                )

            products = Product.objects.filter(query_filters).order_by('-discount')[:100]
    else:
        # Si no se proporciona una consulta de búsqueda, devuelve los primeros 100 productos activos ordenados por descuento
        products = Product.objects.filter(state='active').order_by('-discount')[:100]

    products_data = list(products.values('id', 'shop' ,'name', 'description', 'price', 'barcode', 'image_base64', 'discount', 'created_at', 'subcategory__name', 'subcategory__category__name', 'shop__razon_social'))
    return JsonResponse({'products': products_data})
