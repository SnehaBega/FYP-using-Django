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
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)
METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti"),
)

# khalti payment 
# class Payment(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     amount = models.FloatField()
#     khalti_order_id = models.CharField(max_length=100, blank=True, null=True)
#     khalti_payment_status = models.CharField(max_length=100, blank=True, null=True)
#     khalti_payment_id = models.CharField(max_length = 100,blank=True, null=True)
#     paid = models.BooleanField(default=False)
# models.py

# class Transaction(models.Model):
#     # Define choices for payment methods
#     PAYMENT_METHOD_CHOICES = [
#         ('Khalti', 'Khalti'),
#         ('COD ', 'COD'),
#     ]
    
#     # Define choices for transaction status
#     TRANSACTION_STATUS_CHOICES = [
#         ('Initiated', 'Initiated'),
#         ('Completed', 'Completed'),
#         ('Pending', 'Pending'),
#         ('Failed', 'Failed'),
#         ('Canceled', 'Canceled'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, default='Khalti')
#     status = models.CharField(max_length=50, choices=TRANSACTION_STATUS_CHOICES, default='Initiated')
#     # transaction_id = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)
#     paid = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user.username} - {self.amount} - {self.created_at}"

class Transaction(models.Model):
    # Define choices for payment methods
    PAYMENT_METHOD_CHOICES = [
        ('Khalti', 'Khalti'),
        ('COD', 'COD'),
    ]
    
    # Define choices for transaction status
    TRANSACTION_STATUS_CHOICES = [
        ('Initiated', 'Initiated'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
        ('Canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, default='Khalti')
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS_CHOICES, default='Initiated')
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.created_at}"
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
  
# class OrderPlaced(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete = models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     ordered_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length = 50, choices= STATUS_CHOICES, default='Pending')
#     transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE,default="")
#     @property
#     def total_cost(self):
#         return self.quantity * self.product.discounted_price
    
    
# class Ordered(models.Model):
#     user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, verbose_name="Product",null=True, on_delete=models.CASCADE)
#     address = models.CharField(max_length=200)
#     mobile = models.IntegerField()
#     email = models.EmailField(null=True, blank=True)
#     quantity = models.PositiveIntegerField(verbose_name="Quantity")
#     total = models.PositiveIntegerField()
#     status_choices = models.CharField(max_length=50,default="Pending", choices=STATUS_CHOICES)
#     created_at = models.DateTimeField(auto_now_add=True)
#     payment_method = models.CharField(
#         max_length=20, choices=METHOD, default="Cash On Delivery")
#     payment_completed = models.BooleanField(
#         default=False, null=True, blank=True)

#     def __str__(self):
#         return "Order: " + str(self.id)



from django.db import models

class COD(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        # Add more options as needed
    ]

    DELIVERY_TIME_CHOICES = [
        ('7-9', 'From 7 to 9'),
        ('4-6', 'From 4 to 6'),
        # Add more options as needed
    ]

    PICKUP_LOCATION_CHOICES = [
        ('chabahil', 'Chabahil'),
        ('naxal', 'Naxal'),
        # Add more options as needed
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phonenum = models.CharField(max_length=20)
    remarks = models.TextField(blank=True)
    address = models.TextField()
    pickup_location = models.CharField(max_length=100, choices=PICKUP_LOCATION_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    delivery_time = models.CharField(max_length=20, choices=DELIVERY_TIME_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 

     
# class OrderPlaced(models.Model):
#     address = models.CharField(max_length=100)
#     mobile = models.CharField(max_length=15)
#     payment_method = models.CharField(max_length=50)
#     # Other fields...
  

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
    length = models.CharField(verbose_name= "length-cm",max_length=50)  # Consider using a CharField to include units (e.g., inches, cm)
    metal_type = models.CharField(max_length=20, choices=METAL_TYPE_CHOICES)
    shipping_address = models.CharField(max_length=255)

    def __str__(self):
        return self.product_type  # Or any other field you want to represent the object with

class RepairRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    type_of_accessory = models.CharField(max_length=100)
    description_of_damage = models.TextField()

    def __str__(self):
        return self.name
    
class ReplacementRequest(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    REPLACEMENT_CHOICES = [
        ('bead', 'Bead Replacement'),
        ('clasp', 'Clasp Replacement'),
        ('string', 'String Replacement'),
    ]
    replacement_issue = models.CharField(max_length=10, choices=REPLACEMENT_CHOICES)
    address_line_1 = models.CharField(max_length=100)
    Pickup_location_Choices = [
        ('naxal', 'Naxal'),
        ('chabahil', 'Chabahil'),
        ('boudha', 'Boudha'),
    ]
    pickup_location = models.CharField(max_length=50, choices = Pickup_location_Choices)
    accessory_type = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.full_name
    
    
class ResizingRequest(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='Full Name')
    email = models.EmailField(max_length=100, verbose_name='Email Address')
    phone_number = models.CharField(max_length=15, verbose_name='Phone Number')
    RESIZING_CHOICES = [
        ('rings', 'Rings Re-sizing'),
        ('bracelets', 'Bracelets Resizing'),
        ('necklace', 'Necklace Resizing'),
    ]
    resizing_options = models.CharField(max_length=20, choices=RESIZING_CHOICES, verbose_name='Re-sizing Options')
    street_address_1 = models.CharField(max_length=100, verbose_name='Address')
    PICKUP_LOCATION_CHOICES = [
        ('Chabahil', 'Chabahil'),
        ('Kapan', 'Kapan'),
        ('Naxal', 'Naxal'),
        ('Boudha', 'Boudha'),
    ]
    pickup_location = models.CharField(max_length=50, choices=PICKUP_LOCATION_CHOICES, verbose_name='Available PickUp Location')
    description = models.TextField(verbose_name='Description of resizing')
    additional_details = models.TextField(verbose_name='Any additional details to resizing')

    def __str__(self):
        return self.full_name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review #{self.id}"   
    
class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

        