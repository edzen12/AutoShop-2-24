from django.urls import path
from apps.cart.views import AddToCartView, CartDetailView, RemoveFromCartView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:pk>', RemoveFromCartView.as_view(), name='remove_from_cart'),
]