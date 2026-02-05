from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Barcode(models.Model):
    TYPE_CHOICES = (
        ('link', 'لينك'),
        ('product', 'منتج'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='General')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)         # للـ link
    product_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)  # للمنتج
    qr_code = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    scans = models.IntegerField(default=0)

    def __str__(self):
        return self.title
