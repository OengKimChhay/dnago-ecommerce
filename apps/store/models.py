from django.db import models
from auth.user.models import Account


# Create your models here.
class Customer(models.Model):
    user_id = models.OneToOneField(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to='product/images/')
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# --------------- ProductImages storing multiple images for products------------
class ProductImages(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/', null=True, blank=True)


# ---------------- cart ---------------------------
class Cart(models.Model):
    customer_id = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ---------------- order table --------------------
class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    amount = models.CharField(max_length=100)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=28)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)


class ShippingAddress(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=188)
    lastname = models.CharField(max_length=100)
    contry = models.CharField(max_length=108)
    address = models.TextField(max_length=180)
    city = models.CharField(max_length=180)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=108)
    additional_info = models.TextField()
