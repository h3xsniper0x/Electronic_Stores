from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category, Product, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for Review model."""
    list_display = ('product', 'user', 'rating_stars', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    ordering = ('-created_at',)
    
    def rating_stars(self, obj):
        """Display rating as stars."""
        stars = '⭐' * obj.rating
        return format_html(
            '<span style="color: #ffc107; font-size: 1.2rem;">{}</span>',
            stars
        )
    rating_stars.short_description = 'التقييم'
    rating_stars.admin_order_field = 'rating'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ('name', 'description', 'product_count')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    def product_count(self, obj):
        """Display the number of products in this category."""
        count = obj.products.count()
        return format_html(
            '<span style="color: {};">{}</span>',
            '#28a745' if count > 0 else '#dc3545',
            count
        )
    product_count.short_description = 'عدد المنتجات'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    list_display = ('image_thumbnail', 'name', 'category', 'price_display', 'stock_status', 'created_at')
    list_display_links = ('image_thumbnail', 'name')
    list_filter = ('category', 'created_at', 'stock')
    search_fields = ('name', 'description', 'category__name')
    list_per_page = 20
    ordering = ('-created_at',)
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    
    fieldsets = (
        ('معلومات المنتج', {
            'fields': ('name', 'description', 'category')
        }),
        ('السعر والمخزون', {
            'fields': ('price', 'stock')
        }),
        ('الصورة', {
            'fields': ('image', 'image_preview')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_thumbnail(self, obj):
        """Display product image as thumbnail in list view."""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return mark_safe(
            '<span style="display: inline-block; width: 50px; height: 50px; background: #f0f0f0; '
            'border-radius: 8px; text-align: center; line-height: 50px;">📦</span>'
        )
    image_thumbnail.short_description = 'الصورة'
    
    def image_preview(self, obj):
        """Display larger image preview in detail view."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 12px;" />',
                obj.image.url
            )
        return 'لا توجد صورة'
    image_preview.short_description = 'معاينة الصورة'
    
    def price_display(self, obj):
        """Display price with currency."""
        return format_html(
            '<span style="font-weight: bold; color: #28a745;">{} ر.س</span>',
            obj.price
        )
    price_display.short_description = 'السعر'
    price_display.admin_order_field = 'price'
    
    def stock_status(self, obj):
        """Display stock status with color coding."""
        if obj.stock <= 0:
            return mark_safe(
                '<span style="background: #dc3545; color: white; padding: 3px 10px; '
                'border-radius: 12px; font-size: 11px;">نفد المخزون</span>'
            )
        elif obj.stock <= 5:
            return format_html(
                '<span style="background: #ffc107; color: #000; padding: 3px 10px; '
                'border-radius: 12px; font-size: 11px;">منخفض ({})</span>',
                obj.stock
            )
        else:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 10px; '
                'border-radius: 12px; font-size: 11px;">متوفر ({})</span>',
                obj.stock
            )
    stock_status.short_description = 'حالة المخزون'
    stock_status.admin_order_field = 'stock'
    
    # Custom filters
    class StockFilter(admin.SimpleListFilter):
        title = 'حالة المخزون'
        parameter_name = 'stock_status'
        
        def lookups(self, request, model_admin):
            return (
                ('in_stock', 'متوفر'),
                ('low_stock', 'منخفض'),
                ('out_of_stock', 'نفد المخزون'),
            )
        
        def queryset(self, request, queryset):
            if self.value() == 'in_stock':
                return queryset.filter(stock__gt=5)
            elif self.value() == 'low_stock':
                return queryset.filter(stock__gt=0, stock__lte=5)
            elif self.value() == 'out_of_stock':
                return queryset.filter(stock__lte=0)
    
    list_filter = ('category', StockFilter, 'created_at')
