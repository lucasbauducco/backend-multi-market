from rest_framework import views, status
from rest_framework.response import Response
from shop.models import SubCategory
from shop.serializers import SubCategorySerializer
class SubCategoryList(views.APIView):
    """
    Vista para listar todas las subcategorías.
    """

    def get(self, request):
        """
        Obtiene y retorna todas las subcategorías existentes.
        
        Parámetros:
        - request: HttpRequest, contiene información sobre la solicitud HTTP.
        
        Retorna:
        - Response: Contiene la lista de subcategorías.
        """
        # Se puede aplicar alguna lógica para filtrar las subcategorías si es necesario,
        # por ejemplo, basándose en un parámetro de la solicitud.

        subcategories = SubCategory.objects.all()

        # Usando un serializador para estructurar los datos de las subcategorías
        serializer = SubCategorySerializer(subcategories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)