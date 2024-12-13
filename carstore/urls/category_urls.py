from django.urls import path
from carstore.views.category.category_view import CategoryListView, CategoryView, CategoryCreateView, CategoryDeleteView, CategoryUpdateView


urlpatterns= [
    path('', CategoryListView.as_view(), name="category-list-view"),
    path('<int:product_id>/', CategoryView.as_view(), name="category-view"),
    path('create/', CategoryCreateView.as_view(), name="category-create"),
    path('update', CategoryUpdateView.as_view(), name="category-update"),
    path('delete/<int:product_id>', CategoryDeleteView.as_view(), name="category-delete"),
]
