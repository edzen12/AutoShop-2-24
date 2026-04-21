from apps.cart.models import Cart, CartItem


def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(
            session_key = request.session.session_key
        )
    return cart 


def merge_cart(request, user):
    session_key = request.session.session_key
    if not session_key:
        return
    try:
        session_cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        return
    user_cart, _ = Cart.objects.get_or_create(user=user)

    for item in session_cart.items.all():
        existing_item = CartItem.objects.filter(
            cart=user_cart,
            product=item.product
        ).first()

        if existing_item:
            existing_item.quantity += item.quantity
            existing_item.save()
        else:
            item.cart = user_cart
            item.save()

    session_cart.delete()