from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import  Group
from . models import Product
from .models import Customer, Product, Cart, Wishlist
from django.utils.html import format_html

# Register your models here.
class BLogAdmin(admin.ModelAdmin):
    exclude= ()
    list_display = ['title','less_content', 'image', 'is_deleted', 'click_me','extra_title' ] 
    list_display_links = ('less_content', 'title')
    # list_filter = ('is_deleted', 'created_at', ('extra_title' , admin.EmptyFieldListFiler))
    
    def less_content(self, obj):
        return format_html(f'<span style="color:green"> {obj.content[:50]} </span>')
    
    def click_me(self, obj):
        return format_html(f'<a href="admin/beadaz/blog/{obj.id}/change/" class="default"> View </a>')
    

admin.site.register(Blog, BLogAdmin)


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']
    
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city']
    
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']
    
@admin.register(Customization)
class CustomizationModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_num', 'product_type', 'bead_material', 'bead_colour', 'closure_type','length',  'metal_type', 'shipping_address']
    
@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']
    def products(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}"> {}</a>',link, obj.product.title)
    
admin.site.unregister(Group)