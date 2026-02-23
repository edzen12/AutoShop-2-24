from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy 

from .models import Category, Product, Review
from apps.blog.models import Post
from apps.partners.models import Partner


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(
            is_active=True, parent__isnull=True)[:8]
        context['products'] = Product.objects.filter(is_available=True)[:8]
        context['partners'] = Partner.objects.all()
        context['posts'] = (
            Post.objects.prefetch_related('tags')
        )
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'product/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent__isnull=True)
    

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