from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Customer
from .models import *

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus ':'True',
    'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs=
    {'autocomplete' : 'current-password', 'class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus ':'True',
    'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs=
    {'class': 'form-control'}))
    password1 = forms.CharField(label = 'Password',widget=forms.PasswordInput(attrs=
    {'class': 'form-control'}))
    password2 = forms.CharField(label = 'Confirm Password',widget=forms.PasswordInput(attrs=
    {'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class MyPasswordChangeForm(PasswordChangeForm):
    old_password= forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs=
    {'autofocus' : 'True', 'autocomplete': 'current-password','class':'form-control'}))
    new_password1= forms.CharField(label='New Password', widget=forms.PasswordInput(attrs=
    {'autofocus' : 'True', 'autocomplete': 'current-password','class':'form-control'})) 
    new_password2= forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs=
    {'autofocus' : 'True', 'autocomplete': 'current-password','class':'form-control'}))           

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs=
    {'autocomplete' : 'current-password', 'class' : 'form-control'}))
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs=
    {'autocomplete' : 'current-password', 'class' : 'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
      model = Customer  
      fields = ['name', 'locality', 'city', 'mobile']
      widgets = {
          'name' : forms.TextInput(attrs={'class':'form-control'}),
          'locality' : forms.TextInput(attrs={'class':'form-control'}),
          'city' : forms.TextInput(attrs={'class':'form-control'}),
          'mobile' : forms.NumberInput(attrs={'class':'form-control'}),         
          
      }
      
class RepairForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ['name', 'email', 'phone', 'type_of_accessory', 'description_of_damage']

class ReplacementForm(forms.ModelForm):
    class Meta:
        model = ReplacementRequest
        fields = '__all__'
        
class ResizingForm(forms.ModelForm):
    class Meta:
        model = ResizingRequest
        fields = '__all__'               


class CODForm(forms.ModelForm):
    PICKUP_LOCATION_CHOICES = [
        ('chabahil', 'Chabahil'),
        ('naxal', 'Naxal'),
        # Add more options as needed
    ]

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

    pickup_location = forms.ChoiceField(choices=PICKUP_LOCATION_CHOICES)
    payment_status = forms.ChoiceField(choices=PAYMENT_STATUS_CHOICES)
    delivery_time = forms.ChoiceField(choices=DELIVERY_TIME_CHOICES)

    class Meta:
        model = COD
        fields = ['name', 'email', 'phonenum', 'remarks', 'address', 'pickup_location', 'payment_status', 'delivery_time']
           
class CustomizationForm(forms.ModelForm):
    BEAD_MATERIAL_CHOICES = [
        ('glass', 'Glass'),
        ('crystal', 'Crystal'),
        ('gemstone', 'Gemstone'),
        ('seedBeads', 'SeadBeads'),
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
    
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus ':'True',
    'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs=
    {'class': 'form-control'}))
    phone_num = forms.IntegerField(widget=forms.NumberInput(attrs={'autofocus': True, 'class': 'form-control'}))
    product_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    bead_material = forms.ChoiceField(choices=BEAD_MATERIAL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    bead_colour = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    closure_type = forms.ChoiceField(choices=CLOSURE_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    length = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Consider using a CharField to include units (e.g., inches, cm)
    metal_type = forms.ChoiceField(choices=METAL_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    shipping_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Customization
        fields = ['username', 'email', 'phone_num', 'product_type', 'bead_material', 'bead_colour', 'closure_type','length',  'metal_type', 'shipping_address']
   # or
        # fields = "__all__"

    def clean_phone_num(self):
        phone_num = self.cleaned_data.get('phone_num')
        if len(str(phone_num)) < 10:  # Adjust as needed based on your requirements
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone_num

# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['comment', 'rate','product']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = OrderPlaced
        fields = ["product",
                  "status", "transaction"]  

# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = ['amount', 'payment_method', 'status', 'paid']
#         exclude = ['user']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'payment_method', 'status', 'paid']
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product','rate','comment']  # Remove 'rate' field as it will be handled differently

    # Custom widget for the rate field
    rate = forms.IntegerField(
        label='Rate',
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5', 'step': '1'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rate'].label = 'Rate'

    def clean_rate(self):
        rate = self.cleaned_data['rate']
        if rate < 1 or rate > 5:
            raise forms.ValidationError('Rate must be between 1 and 5.')
        return rate

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }  
