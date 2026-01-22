from django.db import models


class Category(models.Model):
    """Category model for organizing products."""
    name = models.CharField(max_length=200, verbose_name='اسم الفئة')
    description = models.TextField(blank=True, verbose_name='الوصف')

    class Meta:
        verbose_name = 'فئة'
        verbose_name_plural = 'الفئات'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model for the electronic store catalog."""
    name = models.CharField(max_length=200, verbose_name='اسم المنتج')
    description = models.TextField(verbose_name='الوصف')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر')
    stock = models.IntegerField(default=0, verbose_name='المخزون')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='الفئة'
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='الصورة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Product review model."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='المنتج'
    )
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='المستخدم'
    )
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name='التقييم'
    )
    comment = models.TextField(verbose_name='التعليق')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ التعليق')

    class Meta:
        verbose_name = 'تقييم'
        verbose_name_plural = 'التقييمات'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'
