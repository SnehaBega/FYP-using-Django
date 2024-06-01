from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import  Group
from .models import Product
from .models import Customer, Product, Cart, Wishlist, Review, Subscription
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
    list_display = ['user', 'product', 'quantity']
    
@admin.register(COD)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phonenum','remarks','address','pickup_location', 'payment_status','delivery_time','timestamp']
   
# @admin.register(Ordered)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['user', 'address', 'product', 'quantity','payment_method', 'created_at']

#khalti payment
# @admin.register(Payment)
# class PaymentModelAdmin(admin.ModelAdmin):
#     list_display = ['id','user', 'amount', 'khalti_order_id', 'khalti_payment_status', 'khalti_payment_id', 'paid']
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'payment_method', 'status', 'created_at','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'transaction']
    
@admin.register(Customization)
class CustomizationModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_num', 'product_type', 'bead_material', 'bead_colour', 'closure_type','length',  'metal_type', 'shipping_address']

@admin.register(RepairRequest)
class RepairRequestModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'type_of_accessory', 'description_of_damage']

@admin.register(ReplacementRequest)
class ReplacementRequestModelAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone_number', 'replacement_issue', 'address_line_1','pickup_location', 'accessory_type', 'description']

@admin.register(ResizingRequest)
class ResizingRequestModelAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone_number', 'resizing_options', 'street_address_1','pickup_location', 'description', 'additional_details']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'rate' ,'created_at']
    readonly_fields = ['created_at',]

@admin.register(Subscription)   
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']
    def products(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}"> {}</a>',link, obj.product.title)
    
admin.site.unregister(Group)