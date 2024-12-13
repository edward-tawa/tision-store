from django.urls import path
from carstore.views.product.product_view import ProductListView, ProductView, ProductCreateView, ProductUpdateView, ProductDeleteView


urlpatterns= [
    path('', ProductListView.as_view(), name="product-list-view"),
    path('<int:product_id>/', ProductView.as_view(), name="product-view"),
    path('create/', ProductCreateView.as_view(), name="product-create"),
    path('update', ProductUpdateView.as_view(), name="product-update"),
    path('delete/<int:product_id>', ProductDeleteView.as_view(), name="product-delete"),
]
