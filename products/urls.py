from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
]
