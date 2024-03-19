from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField

# Create your models here.

CATEGORY_CHOICES=(
    ('BR', 'Beads-Rings'),
    ('BC', 'Beaded-Choker'),
    ('PC', 'Phone-charm'),
    ('BB', 'Bead-bracelet'),
    ('WC', 'Waist-Chain'),
    ('ER', 'Earring'),
    ('NE', 'Necklace'),
    ('CL', 'Clips'),   
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.TextField(choices=CATEGORY_CHOICES, max_length=200)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quality * self.product.discounted_price
STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ("On The Way", 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    eSewa_order_id = models.CharField(max_length=100, blank=True, null=True)
    eSewa_payment_status = models.CharField(max_length=100, blank=True, null=True)
    eSewa_payment_id = models.CharField(max_length = 100,blank=True, null=True)
    paid = models.BooleanField(default=False)
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 50, choices= STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
   

class Blog(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to = "images")
    content = models.TextField()
    extra_title = models.CharField(max_length = 100, blank = True, null= True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add = True, blank = True, null = True)
    
    def __str__(self):
        return self.title
    
class Customization(models.Model):
    BEAD_MATERIAL_CHOICES = [
        ('glass', 'Glass'),
        ('crystal', 'Crystal'),
        ('gemstone', 'Gemstone'),
        ('seedBeads', 'SeedBeads'),
        ('none', 'none'),
    ]

    CLOSURE_TYPE_CHOICES = [
        ('lobster', 'Lobster Clasp'),
        ('magnetic', 'Magnetic Clasp'),
        ('toggle', 'Toggle Clasp'),
        ('none', 'none'),
    ]

    METAL_TYPE_CHOICES = [
        ('gold-plated', 'Gold-plated'),
        ('silver', 'Silver'),
        ('copper', 'Copper'),
        ('none', 'none'),
    ]

    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone_num = models.CharField(max_length=15)  # Assuming max length for phone number
    product_type = models.CharField(max_length=100)
    bead_material = models.CharField(max_length=20, choices=BEAD_MATERIAL_CHOICES)
    bead_colour = models.CharField(max_length=100)
    closure_type = models.CharField(max_length=20, choices=CLOSURE_TYPE_CHOICES)
    length = models.CharField(max_length=50)  # Consider using a CharField to include units (e.g., inches, cm)
    metal_type = models.CharField(max_length=20, choices=METAL_TYPE_CHOICES)
    shipping_address = models.CharField(max_length=255)

    def __str__(self):
        return self.product_type  # Or any other field you want to represent the object with

    
# class RepairRequest(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)
#     accessory = models.CharField(max_length=100)
#     description = models.TextField()
#     def __str__(self):
#         return self.name  # Display the name of the requester in the admin panel