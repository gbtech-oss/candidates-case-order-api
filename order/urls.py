from django.urls import path
from .views import OrderCreateView, OrderUpdateView, OrderDetailView, ItemDeleteView, OrderListByDocumentView, OrderUpdateAddressView

urlpatterns = [
    path('orders/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/add-items/', OrderUpdateView.as_view(), name='order-update'),
    path('orders/<int:pk>/items/<int:item_id>/', ItemDeleteView.as_view(), name='order-item-delete'),
    path('orders/filter/', OrderListByDocumentView.as_view(), name='order-list-by-document'),
    path('orders/<int:pk>/update-address/', OrderUpdateAddressView.as_view(), name='order-update-address'),
]
