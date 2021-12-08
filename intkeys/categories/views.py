from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate, logout
from .models import *
from rest_framework import viewsets
from .forms import CategoryForm
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, View
from .mixins import CategoryDetailMixin
from django.http import HttpResponseRedirect


class BaseView(View):
    def get(self, request, *args, **kwargs):
        data = {
            'categories': Category.objects.all(),
            'latest_products': Product.objects.all().order_by('-id')[:6]
        }
        return render(request, 'categories/home.html', data)


class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'categories/category_details.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return render(request, 'categories/add_category.html', {'form': form, 'categories': categories})


class ProductDetailView(CategoryDetailMixin, DetailView):
    model = Product
    template_name = 'categories/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        if not request.user.is_authenticated:
            return redirect('register')
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer, in_order=False)
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=cart.owner, cart=cart, product=product, final_price=product.price
        )
        cart.products.add(cart_product)
        return HttpResponseRedirect('/cart/')


class CartView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('register')
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.all()
        data = {
            'cart': cart,
            'categories': categories
        }
        return render(request, 'categories/cart.html', data)
