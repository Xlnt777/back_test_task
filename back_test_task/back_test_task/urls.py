from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from parser.views import CategoryAPIView, ProductViewSet, CategoryAutocompleteView,category_search_view

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/categories/',CategoryAPIView.as_view()),
    path('api/v1/', include(router.urls)),
    path('api/categories/autocomplete/',CategoryAutocompleteView.as_view()),
    path('', category_search_view),
]
