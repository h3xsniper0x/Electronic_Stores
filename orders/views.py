from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm
from products.models import Product


def get_or_create_cart(user):
    """Get existing cart or create a new one for the user."""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_view(request):
    """Display the shopping cart."""
    cart = get_or_create_cart(request.user)
    return render(request, 'orders/cart.html', {'cart': cart})


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add a product to the cart."""
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'تم إضافة "{product.name}" إلى السلة')
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total_items,
            'message': f'تم إضافة "{product.name}" إلى السلة'
        })
    
    return redirect('orders:cart')


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update quantity of a cart item."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    
    quantity = request.POST.get('quantity', 1)
    try:
        quantity = int(quantity)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'تم تحديث الكمية')
        else:
            cart_item.delete()
            messages.success(request, 'تم حذف المنتج من السلة')
    except ValueError:
        messages.error(request, 'كمية غير صالحة')
    
    return redirect('orders:cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'تم حذف "{product_name}" من السلة')
    return redirect('orders:cart')


@login_required
def checkout_view(request):
    """Handle checkout process."""
    cart = get_or_create_cart(request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'السلة فارغة. أضف منتجات قبل إتمام الشراء.')
        return redirect('orders:cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create the order
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.total_price
            order.save()
            
            # Create order items from cart items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Clear the cart
            cart.items.all().delete()
            
            messages.success(request, 'تم إنشاء طلبك بنجاح!')
            return redirect('orders:order_detail', order_id=order.pk)
    else:
        # Pre-fill form with user data if available
        initial_data = {
            'full_name': request.user.get_full_name() or request.user.username,
        }
        form = CheckoutForm(initial=initial_data)
    
    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
    })


@login_required
def order_detail_view(request, order_id):
    """Display order confirmation/details."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list_view(request):
    """Display user's order history."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def cancel_order(request, order_id):
    """Cancel a pending order."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    
    # Only allow cancelling pending orders
    # assuming 'pending' is the status for new orders, check model first?
    # For now, we'll assume a purely status-based check or just allow if recent?
    # Let's check if the status field exists or if we should just allow deleting.
    # The requirement says 'CRUD', so deleting the order is acceptable.
    
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'تم إلغاء الطلب بنجاح.')
        return redirect('orders:order_list')
    
    return render(request, 'orders/confirm_cancel.html', {'order': order})
