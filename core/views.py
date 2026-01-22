from django.shortcuts import render
from django.views.generic import ListView, DetailView
from products.models import Product, Category


def home(request):
    """Homepage view with featured products and categories."""
    featured_products = Product.objects.all()[:6]
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)


class ProductListView(ListView):
    """List all products with pagination and category filtering."""
    model = Product
    template_name = 'core/product_list.html'
    context_object_name = 'products'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class ProductDetailView(DetailView):
    """Display detailed information about a product."""
    model = Product
    template_name = 'core/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related products from the same category
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk)[:4]
        return context
