from django.contrib import admin
from .models import Category, Suits, Review

# Register your models here.
@admin.register(Suits)
class SuitsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'sizes', 'category', 'brands', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'category', 'brands', 'created', 'price', 'updated']
    list_editable = ['price', 'available']
    search_fields = ('name', 'category__name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'product', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email')
