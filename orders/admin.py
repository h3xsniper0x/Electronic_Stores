from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
 
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_price_display')
    can_delete = True
    
    def total_price_display(self, obj):
        return format_html(
            '<span style="font-weight: bold; color: #28a745;">{} ر.س</span>',
            obj.total_price
        )
    total_price_display.short_description = 'المجموع'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin configuration for Cart model."""
    list_display = ('id', 'user', 'items_count', 'total_price_display', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'total_price_display')
    inlines = [CartItemInline]
    
    def items_count(self, obj):
        count = obj.items.count()
        return format_html(
            '<span style="background: #007bff; color: white; padding: 3px 10px; '
            'border-radius: 12px;">{}</span>',
            count
        )
    items_count.short_description = 'عدد العناصر'
    
    def total_price_display(self, obj):
        return format_html(
            '<span style="font-weight: bold; color: #28a745;">{} ر.س</span>',
            obj.total_price
        )
    total_price_display.short_description = 'المجموع الكلي'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin configuration for CartItem model."""
    list_display = ('id', 'cart', 'product', 'quantity', 'total_price_display')
    list_filter = ('cart__user',)
    search_fields = ('product__name', 'cart__user__username')
    
    def total_price_display(self, obj):
        return format_html(
            '<span style="font-weight: bold; color: #28a745;">{} ر.س</span>',
            obj.total_price
        )
    total_price_display.short_description = 'المجموع'


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem in Order view."""
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'total_price_display')
    can_delete = False
    
    def total_price_display(self, obj):
        return format_html(
            '<span style="font-weight: bold; color: #28a745;">{} ر.س</span>',
            obj.total_price
        )
    total_price_display.short_description = 'المجموع'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model."""
    list_display = ('order_id', 'user_info', 'full_name', 'phone', 'status_badge', 'total_price_display', 'created_at')
    list_display_links = ('order_id', 'user_info')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__username', 'full_name', 'phone', 'address')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('معلومات الطلب', {
            'fields': ('user', 'status', 'total_price')
        }),
        ('معلومات التوصيل', {
            'fields': ('full_name', 'address', 'phone')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def order_id(self, obj):
        return format_html(
            '<span style="font-weight: bold; color: #e94560;">#{}</span>',
            obj.pk
        )
    order_id.short_description = 'رقم الطلب'
    order_id.admin_order_field = 'id'
    
    def user_info(self, obj):
        return format_html(
            '<span style="color: #007bff;">👤 {}</span>',
            obj.user.username
        )
    user_info.short_description = 'المستخدم'
    user_info.admin_order_field = 'user__username'
    
    def total_price_display(self, obj):
        return format_html(
            '<span style="font-weight: bold; color: #28a745;">{} ر.س</span>',
            obj.total_price
        )
    total_price_display.short_description = 'المجموع'
    total_price_display.admin_order_field = 'total_price'
    
    def status_badge(self, obj):
        colors = {
            'pending': ('#ffc107', '#000'),
            'processing': ('#17a2b8', '#fff'),
            'shipped': ('#007bff', '#fff'),
            'delivered': ('#28a745', '#fff'),
            'cancelled': ('#dc3545', '#fff'),
        }
        bg, fg = colors.get(obj.status, ('#6c757d', '#fff'))
        return format_html(
            '<span style="background: {}; color: {}; padding: 5px 12px; '
            'border-radius: 15px; font-size: 12px; font-weight: bold;">{}</span>',
            bg, fg, obj.get_status_display()
        )
    status_badge.short_description = 'الحالة'
    status_badge.admin_order_field = 'status'
    
    # Admin actions
    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
        self.message_user(request, f'تم تحديث {queryset.count()} طلب إلى "قيد المعالجة"')
    mark_as_processing.short_description = 'تعيين كـ "قيد المعالجة"'
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, f'تم تحديث {queryset.count()} طلب إلى "تم الشحن"')
    mark_as_shipped.short_description = 'تعيين كـ "تم الشحن"'
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
        self.message_user(request, f'تم تحديث {queryset.count()} طلب إلى "تم التوصيل"')
    mark_as_delivered.short_description = 'تعيين كـ "تم التوصيل"'
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f'تم تحديث {queryset.count()} طلب إلى "ملغي"')
    mark_as_cancelled.short_description = 'تعيين كـ "ملغي"'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin configuration for OrderItem model."""
    list_display = ('id', 'order_link', 'product', 'quantity', 'price', 'total_price_display')
    list_filter = ('order__status',)
    search_fields = ('product__name', 'order__id')
    
    def order_link(self, obj):
        return format_html(
            '<a href="/admin/orders/order/{}/change/" style="color: #e94560; font-weight: bold;">طلب #{}</a>',
            obj.order.pk, obj.order.pk
        )
    order_link.short_description = 'الطلب'
    
    def total_price_display(self, obj):
        return format_html(
            '<span style="font-weight: bold; color: #28a745;">{} ر.س</span>',
            obj.total_price
        )
    total_price_display.short_description = 'المجموع'


# Customize admin site header and title
admin.site.site_header = '🛒 لوحة تحكم المتجر الإلكتروني'
admin.site.site_title = 'المتجر الإلكتروني'
admin.site.index_title = 'إدارة المتجر'
