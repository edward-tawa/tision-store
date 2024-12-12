from django.urls import path
from carstore.views.customer.customer_view import RegisterCustomerView, CustomerListView, CustomerView, UpdateCustomerView, DeleteCustomerView

urlpatterns= [
    path('', CustomerListView.as_view(), name="customer-list-view"),
    path('<int:product_id>/', CustomerView.as_view(), name="customer-view"),
    path('create/', RegisterCustomerView.as_view(), name="customer-create"),
    path('update', UpdateCustomerView.as_view(), name="customer-update"),
    path('delete/<int:product_id>', DeleteCustomerView.as_view(), name="customer-delete"),
]
