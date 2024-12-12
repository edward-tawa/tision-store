from django.urls import path
from carstore.views.orders.order_view import OrdersListView, OrderView, OrderCreateView, OrderUpdateView, OrderDeleteView

urlpatterns = [
    path("", OrdersListView.as_view(), name="list-orders"),
    path("<int:order_id>/", OrderView.as_view(), name="list-order"),
    path("create/", OrderCreateView.as_view(), name="create-order"),
    path("update/<int:order_id>/", OrderUpdateView.as_view(), name="update-order"),
    path("delete/<int:order_id>/", OrderDeleteView.as_view(), name="delete-order"),
]