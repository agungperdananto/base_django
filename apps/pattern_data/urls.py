from django.urls import path

from .views import ProductDetailView, ProductListView


app_name='pattern_data'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
]
