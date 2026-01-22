from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Product, Review
from .forms import ProductForm


@login_required
@require_POST
def add_review(request, product_id):
    """Add a review for a product."""
    product = get_object_or_404(Product, pk=product_id)
    
    # Check if user already reviewed this product
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.error(request, 'لقد قمت بتقييم هذا المنتج مسبقاً.')
        return redirect('core:product_detail', pk=product_id)
    
    rating = request.POST.get('rating')
    comment = request.POST.get('comment')
    
    if rating and comment:
        Review.objects.create(
            product=product,
            user=request.user,
            rating=int(rating),
            comment=comment
        )
        messages.success(request, 'تم إضافة تقييمك بنجاح!')
    else:
        messages.error(request, 'الرجاء ملء جميع الحقول.')
        
    return redirect('core:product_detail', pk=product_id)


@login_required
def delete_review(request, review_id):
    """Delete a review."""
    review = get_object_or_404(Review, pk=review_id)
    
    # Allow author OR user with delete_review permission
    if request.user == review.user or request.user.has_perm('products.delete_review'):
        product_id = review.product.id
        review.delete()
        messages.success(request, 'تم حذف التقييم بنجاح.')
        return redirect('core:product_detail', pk=product_id)
    
    messages.error(request, 'غير مصرح لك بحذف هذا التقييم.')
    return redirect('core:home')


@login_required
@permission_required('products.add_product', raise_exception=False, login_url='core:home')
def add_product(request):
    """Add a new product (Permission required)."""
    # Note: raise_exception=False with login_url isn't standard for simple redirect with message.
    # But to keep existing behavior of redirection with message, we might stick to manual check OR 
    # use the decorator and let it redirect to login.
    # To strictly match previous "redirect to home with message" behavior, manual check is better.
    # Let's try manual check with has_perm to be safe and consistent with previous UI feedback.
    
    if not request.user.has_perm('products.add_product'):
         messages.error(request, 'عذراً، ليس لديك صلاحية إضافة منتجات.')
         return redirect('core:home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'تم إضافة المنتج بنجاح!')
            return redirect('core:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'إضافة منتج جديد'
    })


@login_required
def edit_product(request, pk):
    """Edit an existing product (Permission required)."""
    if not request.user.has_perm('products.change_product'):
        messages.error(request, 'عذراً، ليس لديك صلاحية تعديل المنتجات.')
        return redirect('core:home')
        
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث المنتج بنجاح!')
            return redirect('core:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': f'تعديل المنتج: {product.name}',
        'is_edit': True,
        'object': product
    })


@login_required
def delete_product(request, pk):
    """Delete a product (Permission required)."""
    if not request.user.has_perm('products.delete_product'):
        messages.error(request, 'عذراً، ليس لديك صلاحية حذف المنتجات.')
        return redirect('core:home')
        
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'تم حذف المنتج بنجاح!')
        return redirect('core:product_list')
    
    return render(request, 'products/confirm_delete.html', {'product': product})
