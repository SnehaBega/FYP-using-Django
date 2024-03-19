from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import Product, Cart, Customer, Wishlist
from django.db.models import Count
from .forms import CustomerRegistrationForm, CustomerProfileForm, Customer, CustomizationForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required #login decorator is for functions 
from django.utils.decorators import method_decorator #methd decorator is for the class
from .forms import CustomizationForm

# Create your views here.
@login_required
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"beadaz/home.html",locals())
  

@login_required
def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"beadaz/about.html",locals())

@login_required
def replacement(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"beadaz/replacement.html",locals())

@login_required
def resizing(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"beadaz/resizing.html",locals())

@login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "beadaz/contact.html",locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"beadaz\category.html",locals())

@method_decorator(login_required, name='dispatch')    
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,"beadaz\category.html",locals())   
 
@method_decorator(login_required, name='dispatch')   
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        return render(request,"beadaz\productdetail.html ",locals())

# @method_decorator(login_required, name='dispatch')     
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "beadaz\customerregistration.html", locals() )
    def post(self, request):
       form = CustomerRegistrationForm(request.POST)
       if form.is_valid(): 
           form.save()
           messages.success(request, "Cngratulations! User Registration Sucessfully completed")
       else:
           messages.warning(request, "Invalid Input Data")
       return render(request, 'beadaz\customerregistration.html', locals()) 
            
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "beadaz\profile.html", locals() )  
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']  
            
            reg = Customer (user= user, name=name, locality=locality, mobile=mobile,city=city)   
            reg.save()   
            messages.success(request, "Congratulations! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Inout data")
        return render(request, "beadaz\profile.html", locals() )

@login_required    
def address(request):
        add = Customer.objects.filter(user=request.user)
        totalitem = 0
        wishitem =  0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'beadaz/address.html', locals())
    
@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self, request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'beadaz/updateAddress.html',locals())
    def post(self, request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']  
            add.save()
            messages.success(request, "Congratulations! PRofile Update SUccessfully")
        else:
            messages.warning(request, "Invalid Inout data")
        return redirect("address")

@login_required    
def add_to_cart(request):
    user= request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product= product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user= user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40      
    totalitem = 0
    wishitem  = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'beadaz/addtocart.html',locals())

@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user =  request.user
        add=Customer.objects.filter(user= user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        return render(request, 'beadaz/checkout.html',locals())
    
# def orders(request):
#     totalitem = 0 
#     wishitem = 0
#     if request.user.is_authenticated:
#         totalitem = len(Cart.objects.filter(user=request.user))
#         wishitem = len(Wishlist.objects.filter(user=request.user))
#     order_placed = OrderPlaced.objects.filter(user=request.user)
#     return render(request, "bedaz/order.html",locals())

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user=request.user))
        c.quantity+= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount =  amount + value
        totalamount = amount + 40
        data={  
              'quantity': c.quantity,
              'amount' : amount,
              'totalamount': totalamount
        }
        return JsonResponse(data)
 
@login_required   
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user=request.user))
        c.quantity-= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount =  amount + value
        totalamount = amount + 40
        data={  
              'quantity': c.quantity,
              'amount' : amount,
              'totalamount': totalamount
        }
        return JsonResponse(data)
    
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount =  amount + value
        totalamount = amount + 40
        data={  
              'quantity': c.quantity,
              'amount' : amount,
              'totalamount': totalamount
        }
        return JsonResponse(data)
    
@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user = user,product=product).save()
        data={
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)

@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data={
            'message': 'Wishlist Removed Successfully',
        }
        return JsonResponse(data)
    
@login_required
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "beadaz/search.html", locals())

# def search(request):
#     query = request.GET.get('search', '')  # Get the search query or default to an empty string
#     totalitem = 0
#     wishitem = 0
#     if request.user.is_authenticated:
#         totalitem = Cart.objects.filter(user=request.user).count()  # Count total items in cart
#         wishitem = Wishlist.objects.filter(user=request.user).count()  # Count total items in wishlist
#     products = Product.objects.filter(title__icontains=query)  # Filter products by title containing the query
#     return render(request, "beadaz/search.html", {'products': products, 'totalitem': totalitem, 'wishitem': wishitem, 'query': query})


@login_required
def testimonials(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'beadaz/testimonials.html')

@login_required
def workshops(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'beadaz/workshops.html')

@login_required
def repair(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'beadaz/repair.html')

@login_required  
def forms(request):
    if request.method == 'POST':
        form = CustomizationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Forms Submitted sucessfully")
            # Redirect to a success page or display a success message
            return redirect('forms')  # Replace 'success-page' with the name of your success page URL
    else:
        form = CustomizationForm()
    return render(request, 'beadaz/forms.html', {'form': form})


# @login_required  
# def CustomizationForm(request):
#     if request.method == 'POST':
#         form = CustomizationForm(request.POST)
#         if form.is_valid():
#             # Process the form data (e.g., save to database)
#             # For demonstration purposes, let's just print the form data
#             print(form.cleaned_data)
#             # Redirect to a success page or another URL
#             return redirect('success_url')  # Replace 'success_url' with your actual success URL name
#     else:
#         form = CustomizationForm()

#     return render(request, 'CustomizationForm.html', {'form': form},locals())
   
# def repair_form(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         accessory = request.POST['accessory']
#         description = request.POST['description']
        
#         # Create a new RepairRequest object and save it to the database
#         repair_request = RepairRequest.objects.create(name=name, email=email, phone=phone, accessory=accessory, description=description)
#         repair_request.save()
        
        # Redirect the user to a thank you page or any other page
        # return redirect('thank_you_page')  # Replace 'thank_you_page' with the name of your thank you page URL pattern
        
    #return render(request, 'repair.html')  # Render the repair form template

def blog(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'beadaz/blog.html')

def blogDetail(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    # post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blogDetail.html')
# class RestringView(View):
#     def get(self, request):
#         return render(request, "beadaz\restring.html", locals() )

        
    