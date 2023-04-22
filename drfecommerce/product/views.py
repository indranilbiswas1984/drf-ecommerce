from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection
from .models import Category,Brand,Product
from .serializers import CategorySerializer,BrandSerializer,ProductSerializer


# Create your views here.

class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """    
    queryset = Category.objects.all()



    @extend_schema(responses=CategorySerializer)
    def list(self,request):
        serializer = CategorySerializer(self.queryset,many=True)
        return Response(serializer.data)
    
class BrandViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all brands
    """    
    queryset = Brand.objects.all()  
    
    
    @extend_schema(responses=BrandSerializer)
    def list(self,request):
        serializer = BrandSerializer(self.queryset,many=True)
        return Response(serializer.data)    
    
class ProductViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all products
    """    
    queryset = Product.objects.all()
    lookup_field="slug"

    # @extend_schema(responses=ProductSerializer)
    def retrieve(self,request, slug=None):
        serializer = ProductSerializer(self.queryset.filter(slug=slug),many=True)
        # print(connection.queries)
        return Response(serializer.data)
    
    @extend_schema(responses=ProductSerializer)
    def list(self,request):
        serializer = ProductSerializer(self.queryset,many=True)
        return Response(serializer.data)   
    
    @action(
            methods=['get'],
            detail=False,
            url_path='category/(?P<category>\w+)/all',
            )
    def list_product_by_category(self,request,category=None):
        """
        An endpoint to return products by category
        """
        serializer = ProductSerializer(self.queryset.filter(category__name=category),many=True)
        return Response(serializer.data) 


