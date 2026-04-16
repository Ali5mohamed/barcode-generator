from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# class Barcode(models.Model):
#     TYPE_CHOICES = (
#         ('link', 'لينك'),
#         ('product', 'منتج'),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='General')
#     title = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     price = models.CharField(max_length=50)
#     url = models.URLField(blank=True, null=True)         # للـ link
#     product_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)  # للمنتج
#     qr_code = models.ImageField(upload_to='barcodes/', blank=True, null=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     scans = models.IntegerField(default=0)

#     def __str__(self):
#         return self.title

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Barcode(models.Model):

    TYPE_CHOICES = (
        ('link', 'لينك'),
        ('menu', 'منيو'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='menu'
    )

    title = models.CharField(max_length=100)

    qr_code = models.ImageField(
        upload_to='barcodes/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(default=timezone.now)

    scans = models.IntegerField(default=0)

    def __str__(self):
        return self.title


# موديل اللينك
class Link(models.Model):

    barcode = models.OneToOneField(
        Barcode,
        on_delete=models.CASCADE,
        related_name="link"
    )

    url = models.URLField()

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.url

class Category(models.Model):
    barcode = models.ForeignKey("Barcode", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# موديل المنتجات
class Product(models.Model):

    barcode = models.ForeignKey(
        Barcode,
        on_delete=models.CASCADE,
        related_name="products"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)

    price = models.CharField(max_length=50)

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name