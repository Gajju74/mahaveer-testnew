# models.py

from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    shop = models.IntegerField(default=1)  # Add a default value

    def __str__(self):
        return self.name

class StockItem(models.Model):
    code = models.CharField(max_length=100, unique=True)
    nw = models.FloatField()
    gw = models.FloatField()
    kundan = models.FloatField()
    moti = models.FloatField()
    po = models.FloatField()
    k_amt  = models.FloatField()  # New field
    m_amt  = models.FloatField()  # New field
    p_amt  = models.FloatField()  # New field
    pcs = models.IntegerField()
    supplier = models.CharField(max_length=255)  # New field
    image = models.ImageField(upload_to='stock_images/', null=True, blank=True)
    category = models.ForeignKey(Category, related_name='stock_items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Convert supplier to uppercase before saving
        if self.supplier:
            self.supplier = self.supplier.upper()
        super(StockItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.code
