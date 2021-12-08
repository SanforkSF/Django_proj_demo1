from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class LatestProducts:
    def get_products_for_models(self, *args, **kwargs):
        products = []
        objects = Product.objects.order_by('-id')
        for prod in objects:
            products.extend(prod)
        return products


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category name')
    slug = models.SlugField(unique=True)

    def __str__(self):
        """
        returns Category name
        """
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all Categories
        """
        all_categories = Category.objects.all()
        return all_categories


class Product(models.Model):
    category = models.ManyToManyField(Category, verbose_name='Category', related_name='related_product')
    title = models.CharField(max_length=255, verbose_name='Product name')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Product image')
    description = models.TextField(verbose_name='Description', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')

    def __str__(self):
        """
        returns Products name
        """
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all Products
        """
        all_products = Product.objects.all()
        return all_products


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE,
                                related_name='related_products')
    qty = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total price')

    def __str__(self):
        return f"Cart product: {self.product.title}"

    def save(self, *args, **kwargs):
        self.final_price = self.product.price * self.qty
        super().save(*args, **kwargs)
        if self.qty <= 0:
            self.delete()


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Owner', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total price')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    phone = models.CharField(unique=True, max_length=20, verbose_name='Phone number')

    def __str__(self):
        return f"Customer: {self.user.first_name} {self.user.last_name}"




class Wishlist(models.Model):
    owner = models.ForeignKey("Customer",
                              verbose_name="Wishlist Owner",
                              on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,
                                      blank=True,
                                      related_name="related_wishlist")

    def __str__(self):
        return str(self.id)


class Orders(models.Model):
    pass
