from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name	
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.slug]) 


class Suits(models.Model):
    sizes = (
        (40,40),
        (42,42),
        (44,44),
        (46,46),
        (48,48),
        (50,50),
        (52,52),
        (54,54),
        (56,56),
        (58,58),
        (60,60),
        (64,64),
        (66,66),
        (68,68),
        (70,70)
    )
    brands = (
        ('Italian Suits', 'Italian Suits'),
        ('Turkish Suits', 'Turkish Suits'),
        ('Chinese Suits', 'Chinese Suits'),
        ('Italian Shoes', 'Italian Shoes'),
        ('Turkish Shoes', 'Turkish Shoes'),
        ('Chinese Shoes', 'Chinese Shoes')
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    category = models.ForeignKey(Category, related_name='suits_products', on_delete=models.CASCADE)
    sizes = models.IntegerField(choices=sizes, null=True, db_index=True, default=40)
    brands = models.CharField(max_length=100, choices=brands, null=True, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('shop:suit_detail', args=[self.id, self.slug])
    
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='gallery/%Y/%m/%d',blank=True)
    description = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Suits, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.product}'

    class Meta:
        ordering = ('created',)
