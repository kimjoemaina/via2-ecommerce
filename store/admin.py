from django.contrib import admin
from .models import Cart, Category, Product, CartItem, Variation


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'inventory', 'modified_date', 'is_available')
    prepopulated_fields = {'slug' : ('product_name',)}
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    prepopulated_fields = {'slug' : ('category_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'cart_quantity', 'is_active')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Variation, VariationAdmin)
