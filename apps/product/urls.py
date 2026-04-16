from django.urls import path
from .views import (
    CategoryListView, ProductListView,
    ProductDetailView, ReviewCreateView, HomeView, 
    ToggleWishlistView, WishlistView, SearchView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='product_by_category'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('search/', SearchView.as_view(), name='search'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/<int:product_id>', ToggleWishlistView.as_view(), name='wishlist_toggle'),
]