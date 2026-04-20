from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views import View
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy 

from apps.product.utils import get_wishlist
from apps.product.models import Category, Product, Review, Brand, Slider, WishlistItem
from apps.blog.models import Post
from apps.partners.models import Partner


class WishlistView(TemplateView):
    template_name = 'pages/wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist = get_wishlist(self.request)
        context['wishlist'] = wishlist
        return context 


class ToggleWishlistView(View):
    def post(self, request, product_id):
        wishlist = get_wishlist(request)
        product = get_object_or_404(Product, id=product_id)
        item = WishlistItem.objects.filter(
            wishlist=wishlist, 
            product=product_id
        ).first()
        if item:
            item.delete()
        else:
            WishlistItem.objects.create(
                wishlist=wishlist, 
                product=product
            )
        return redirect(request.META.get('HTTP_REFERER', '/'))


class SearchView(ListView):
    template_name = 'pages/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            return Product.objects.none()
        return Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct().prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context 
    



class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(
            is_active=True, parent__isnull=True)[:8]
        context['products'] = Product.objects.filter(is_available=True)[:8]
        context['partners'] = Partner.objects.all()
        context['sliders'] = Slider.objects.all()
        context['brands'] = Brand.objects.all()[:8]
        context['posts'] = (
            Post.objects.prefetch_related('tags')
        )
        return context


class CategoryView(ListView):
    template_name = 'pages/category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        categories = category.get_descendants(include_self=True)
        return Product.objects.filter(
            category__in=categories
        ).prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs['slug']
        )
        return context
    

class BrandView(ListView):
    template_name = 'pages/brand.html'
    context_object_name = 'products'

    def get_queryset(self):
        brand = get_object_or_404(Brand, slug=self.kwargs['slug'])
        
        return Product.objects.filter(
            car_models__brand=brand,
        ).distinct().prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()[:8]
        context['brand'] = get_object_or_404(
            Brand, slug=self.kwargs['slug']
        )
        return context
    

class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)\
            .select_related('brand', 'category')\
            .prefetch_related('images')

        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_available=True)\
            .select_related('brand', 'category')\
            .prefetch_related('images', 'reviews', 'variants__attributes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['variants'] = product.variants.all()
        context['reviews'] = product.reviews.all()
        return context


class ReviewCreateView(CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'product/review_form.html'

    def form_valid(self, form):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        form.instance.user = self.request.user
        form.instance.product = product
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={
            'slug': self.kwargs['slug']
        })