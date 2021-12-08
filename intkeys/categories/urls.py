from django.urls import path, include
from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('category/<str:slug>', CategoryDetailView.as_view(), name='category_detail'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('add-category/', add_category, name='add_cat'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart')
]