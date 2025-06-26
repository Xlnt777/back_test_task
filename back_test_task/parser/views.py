from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend 
from .forms import CategorySearchForm
from .wb_product_parser import parser_by_category
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filters import ProductFilter

class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

class CategoryAutocompleteView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response([])

        matches = Category.objects.filter(name__icontains=query).select_related('parent')
        results = []

        for cat in matches:
            label = f"{cat.parent.name} > {cat.name}" if cat.parent else cat.name
            results.append({"id": cat.id, "shard": cat.shard, "query": cat.query, "label": label})
        return Response(results)
    
def category_search_view(request):
    if request.method == 'POST':
        form = CategorySearchForm(request.POST)
        if form.is_valid():
            category_id = form.cleaned_data.get('category_id')
            category_shard = form.cleaned_data.get('category_shard')
            category_query = form.cleaned_data.get('category_query')
            
            if category_id and category_shard and category_query:
                parser_by_category(category_id, category_shard, category_query)
            #print("id " + str(category_id))
            #print("shard " + category_shard)
            #print("query " + category_query)

    return render(request, 'index.html')

