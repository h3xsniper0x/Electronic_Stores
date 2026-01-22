from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    """Shopping cart for users."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='المستخدم'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'سلة التسوق'
        verbose_name_plural = 'سلات التسوق'

    def __str__(self):
        return f'سلة {self.user.username}'

    @property
    def total_price(self):
        """Calculate total price of all items in cart."""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        """Count total number of items in cart."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Individual item in a shopping cart."""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='السلة'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='المنتج'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='الكمية')

    class Meta:
        verbose_name = 'عنصر السلة'
        verbose_name_plural = 'عناصر السلة'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def total_price(self):
        """Calculate total price for this cart item."""
        if self.product is None or self.quantity is None:
            return 0
        try:
            return self.product.price * self.quantity
        except Exception:
            return 0


class Order(models.Model):
    """Customer order."""
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('processing', 'قيد المعالجة'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التوصيل'),
        ('cancelled', 'ملغي'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='المستخدم'
    )
    full_name = models.CharField(max_length=200, verbose_name='الاسم الكامل')
    address = models.TextField(verbose_name='العنوان')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='السعر الإجمالي')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='حالة الطلب'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الطلب')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
        ordering = ['-created_at']

    def __str__(self):
        return f'طلب #{self.pk} - {self.user.username}'


class OrderItem(models.Model):
    """Individual item in an order."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='الطلب'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='المنتج'
    )
    quantity = models.PositiveIntegerField(verbose_name='الكمية')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر')

    class Meta:
        verbose_name = 'عنصر الطلب'
        verbose_name_plural = 'عناصر الطلب'

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def total_price(self):
        """Calculate total price for this order item."""
        if self.price is None or self.quantity is None:
            return 0
        return self.price * self.quantity
