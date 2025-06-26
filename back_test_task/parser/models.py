from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    shard = models.CharField(max_length=255, null=True, blank=True)
    query = models.CharField(max_length=1024, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name or "Без названия"

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    sale_price = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
    rating = models.FloatField(null=True,blank=True)
    feedbacks = models.IntegerField(default=0)
    url = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self) -> str:
        return self.name