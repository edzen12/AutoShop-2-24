from django.urls import path
from apps.product.views import (
    CategoryView, BrandView,
    ProductDetailView, ReviewCreateView, HomeView, 
    ToggleWishlistView, WishlistView, SearchView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'), 
    path('brand/<slug:slug>/', BrandView.as_view(), name='brand'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('search/', SearchView.as_view(), name='search'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/<int:product_id>', ToggleWishlistView.as_view(), name='wishlist_toggle'),
]