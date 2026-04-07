from django.views import View 
from django.views.generic import ListView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from apps.cart.models import CartItem
from apps.product.models import Product
from apps.cart.utils import get_cart


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'price':product.price}
        )
        if not created:
            item.quantity += 1
            item.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))


class CartDetailView(ListView):
    template_name = 'pages/cart.html'
    context_object_name = 'items'

    def get_queryset(self):
        cart = get_cart(self.request)
        return cart.items.select_related('product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = get_cart(self.request)
        return context
    

class RemoveFromCartView(DeleteView):
    model = CartItem

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')