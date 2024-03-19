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