from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
from rest_framework.permissions import AllowAny

class ItemsByCategoryView(APIView):
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]

    def get(self, request, uuid):
        try:
            items = Item.objects.filter(category=uuid)
            serializer = self.serializer_class(items, many=True)
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class AllItemsView(APIView):
    """
    A view to list all items.
    """
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]
    def get(self, request):
        """
        Retrieve a list of all items.
        """
        items = Item.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)
    
class AllCategoriesView(APIView):
    """
    A view to list all categories.
    """
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    def get(self, request):
        """
        Retrieve a list of all categories.
        """
        items = Category.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)
