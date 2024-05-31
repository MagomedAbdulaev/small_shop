from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    autocomplete_fields = ['subcategories', ]


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


class CharacteristicAdmin(admin.TabularInline):
    model = CharacteristicValue
    list_display = ('name',)
    list_display_links = ('name',)
    extra = 5


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_created', 'price', 'products')
    list_display_links = ('user', 'date_created', 'price', 'products')
    search_fields = ('products',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price')
    list_display_links = ('name', 'category', 'price', 'discount_price')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ['name', ]}
    autocomplete_fields = ['subcategory', 'category']
    inlines = [CharacteristicAdmin]


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
