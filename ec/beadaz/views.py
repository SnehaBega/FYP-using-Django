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
from .forms import CustomizationForm, RepairForm
from .forms import *
from .models import *
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect, render
import requests
import json


secret_key = settings.KHALTI_SECRET_KEY

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
def Terms(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"beadaz/terms.html",locals())

@login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "beadaz/contact.html",locals())

# def wishlist(request):
#     totalitem = 0
#     wishitem = 0
#     if request.user.is_authenticated:
#         totalitem = len(Cart.objects.filter(user=request.user))
#         wishitem = len(Wishlist.objects.filter(user=request.user))
#     # Assuming user is logged in
#     wishlist_items = Wishlist.objects.filter(user=request.user)
#     return render(request, 'beadaz/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def wishlist(request):
    total_cart_items = Cart.objects.filter(user=request.user).count()
    total_wishlist_items = Wishlist.objects.filter(user=request.user).count()
    wishlist_items = Wishlist.objects.filter(user=request.user)
    
    context = {
        'total_cart_items': total_cart_items,
        'total_wishlist_items': total_wishlist_items,
        'wishlist_items': wishlist_items
    }
    
    return render(request, 'beadaz/wishlist.html', context)

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
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()
        reviews = Review.objects.filter(product_id=product.id)
        form = ReviewForm()  # Initialize an empty form for GET requests
        return self._handle_review_form(request, pk, product, form, reviews, totalitem, wishitem, wishlist)

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        reviews = Review.objects.filter(product_id=product.id)
        form = ReviewForm(request.POST)  # Bind form data to the POST request
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()
        
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product  # Set the product for the review
            review.save()
            messages.success(request, 'Review submitted successfully.')  # Display success message
            return render(request, 'beadaz/reviewSuccess.html')

        else:
            # If the form is not valid, re-render the page with the form and existing reviews
            return self._handle_review_form(request, pk, product, form, reviews, totalitem, wishitem, wishlist)

    def _handle_review_form(self, request, pk, product, form, reviews, totalitem, wishitem, wishlist):
        context = {
            'product': product,
            'form': form,
            'reviews': reviews,
            'totalitem': totalitem,
            'wishitem': wishitem,
            'wishlist': wishlist.exists(),
        }
        return render(request, 'beadaz/productdetail.html', context)
    

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
           messages.success(request, "Congratulations! User Registration Sucessfully completed")
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

@login_required  
def repair_form(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Forms Submitted sucessfully")
            return redirect('repair') 
    else:
        form = RepairForm()
    return render(request, 'beadaz/repair.html', {'form': form})

@login_required  
def replacement_form(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitem = len(Cart.objects.filter(user=request.user))
    if request.method == 'POST':
        form = ReplacementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Forms Submitted sucessfully")
            return redirect('replacement') 
        else:
            messages.warning(request, "Invalid Input data")
    else:
        form = ReplacementForm()
    return render(request, 'beadaz/replacement.html', {'form': form})

@login_required  
def resizing_form(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitem = len(Cart.objects.filter(user=request.user))
    if request.method == 'POST':
        form = ResizingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Forms Submitted sucessfully")
            return redirect('resizing') 
    else:
        form = ResizingForm()
    return render(request, 'beadaz/resizing.html', {'form': form})
  
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
            messages.warning(request, "Invalid Input data")
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
        Cart.objects.filter(user=request.user).delete()
        return render(request, 'beadaz/checkout.html',locals())
       
        user = request.user
        amount = 1000  # Example amount
        payment_method = "Khalti"  # Example payment method
        status = "Initiated"  # Example initial status
        transaction_id = "123456"  # Example transaction ID
        
        # Create Transaction object
        transaction = Transaction.objects.create(
            user=user,
            amount=amount,
            payment_method=payment_method,
            status=status,
            transaction_id=transaction_id
        )
        # Save the transaction to the database
        transaction.save()

        # Redirect to the appropriate page
        return redirect('order-history')   
    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        for cart_item in cart_items:
            OrderPlaced.objects.create(
                user=user,
                customer=Customer.objects.get(user=user),
                product=cart_item.product,
                quantity=cart_item.quantity,
                status='Pending',
                transaction=Transaction.objects.get(user=user, status='Initiated')  # Adjust this line as necessary
            )
        # Clear the cart
        Cart.objects.filter(user=user).delete()
        return redirect('order-history')
        
    
    # def post(self, request):
    #     form = TransactionForm(request.POST)
    #     if form.is_valid():
    #         transaction = form.save(commit=False)
    #         transaction.user = request.user  # Set the user field
    #         transaction.save()
    #         return redirect('transaction_history')
    #     return render(request, 'beadaz/checkout.html', {'form': form})
    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # Set the user field
            transaction.save()
            return redirect('transaction_history')  # Redirect to transaction history page upon successful save
        else:
            # If form is invalid, show errors in the form
            context = {
                'form': TransactionForm,
                'totalitem': Cart.objects.filter(user=request.user).count(),
                'wishitem': Wishlist.objects.filter(user=request.user).count(),
                'addresses': Customer.objects.filter(user=request.user),
                'cart_items': Cart.objects.filter(user=request.user),
                'totalamount': sum(item.quantity * item.product.discounted_price for item in Cart.objects.filter(user=request.user)) + 40,
            }
            return render(request, 'beadaz/checkout.html', context)
        # else:
        #     form = TransactionForm()
        # return render(request, 'beadaz/checkout.html', {'form': form},locals())

def orders(request):
    totalitem = 0 
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, "beadaz/orders.html",locals())


@method_decorator(login_required, name='dispatch')
class OrderHistory(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = Wishlist.objects.filter(user=request.user).count()
        
        # Fetch orders placed by the current user
        orders = OrderPlaced.objects.filter(user=request.user)
        
        return render(request, 'beadaz/orders.html', {
            'orders': orders,
            'totalitem': totalitem,
            'wishitem': wishitem
        })

@login_required
def order_history(request):
    # Retrieve orders for the logged-in user
    orders = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')
    # Pass the orders to the template
    return render(request, 'order_history.html', {'orders': orders})
           
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
        Wishlist(user=user,product=product).save()
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

@login_required 
def COD(request):
    if request.method == 'POST':
        form = CODForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Form submitted successfully")
            # Redirect to the correct URL after form submission
            return render(request, 'beadaz/codnoti.html')
 
    else:
        form = CODForm()
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'beadaz/cod.html', {'form': form, 'totalitem': totalitem, 'wishitem': wishitem})

@login_required 
def CodNoti(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'beadaz/CodNoti.html')

@login_required 
def blog(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'beadaz/blog.html')

@login_required 
def blogDetail(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    # post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'beadaz/blogDetail.html')


@login_required 
def payment_initiate(request):
    user = request.user
    total_amount = int(float(request.GET.get('amount')) * 100)
    print(total_amount)
    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    payload = json.dumps({
        "return_url": "http://127.0.0.1:8000/success/",
        "website_url": "http://127.0.0.1:8000",
        "amount": total_amount,
        "purchase_order_id": "Order01",
        "purchase_order_name": "test",
        "customer_info": {
            "name":user.username,
            "email": user.email
        }
    })
    headers = {
        'Authorization': f'key {secret_key}',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    new_res = json.loads(response.text)

    transaction_id = new_res.get("transaction_id")

# Create Transaction object only if transaction_id is not None
    if transaction_id:
        transaction = Transaction.objects.create(
            user=request.user,
            amount= total_amount, 
            payment_method="Khalti", 
            status="Initiated",  
            transaction_id=transaction_id  
        )
        transaction.save()
    else:

        print("Transaction ID not found in API response:", new_res)

    return redirect(new_res.get("payment_url")) # Redirect to the payment URL


    # response = requests.request("POST", url, headers=headers, data=payload)
    # new_res = json.loads(response.text)
    # transaction = Transaction.objects.create(
    #     user=request.user,
    #     amount=1000,  # Example amount
    #     payment_method="Khalti",  # Example payment method
    #     status="Initiated",  # Example initial status
    #     transaction_id=new_res.get("transaction_id", "")  # Example transaction ID
    # )
    # transaction.save()
    # return redirect(new_res["payment_url"])


def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    pidx = request.GET.get("pidx")
    headers = {
        'Authorization': f'key {secret_key}',
        'Content-Type': 'application/json',
    }
    payload = json.dumps({
        "pidx":pidx
    })
     # Make the request to Khalti API
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        # Extract response data
        response_data = response.json()

        # Check if transaction_id is not None
        if response_data.get("transaction_id"):
            # Create or update Transaction object
            transaction_id = response_data.get("transaction_id")
            transaction, created = Transaction.objects.get_or_create(transaction_id=transaction_id)
            transaction.user = request.user
            transaction.amount = response_data.get("total_amount")
            transaction.payment_method = "Khalti"
            transaction.status = "Initiated"
            transaction.save()
            return render(request, 'beadaz/transaction_history.html')
            # return redirect('transaction_history')
        else:
            print("Transaction ID not found in API response:", response_data)
    else:
        print("Error:", response.status_code)

    return render(request, 'beadaz/transaction_history.html')

    
    # if response.status == 200:
    # # Example: Update payment status in the database
    #     transaction = Transaction.objects.get(transaction_id=pidx)
    #     transaction.status = response_data.get("status", "")
    #     transaction.save()

    # response = requests.request("POST", url, headers = headers, data = payload)
    # if response.status == 200:
    #     return True
    # else:
    #     return False

        
@login_required 
def success(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'beadaz/success.html')

@login_required 
def transaction_history(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    
    # Fetch all transactions for the current user
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
   
    return render(request, 'beadaz/transaction.html', {'transactions': transactions, 'totalitem': totalitem, 'wishitem': wishitem})


    
@login_required 
def add_review(request, product_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product_id = product_id
            review.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()
    return render(request, 'beadaz/add_review.html', {'form': form})

@login_required 
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed!')
            return redirect('subscribe')
        else:
            messages.error(request, 'There was an error with your subscription.')
    else:
        form = SubscriptionForm()
    
    return render(request, 'beadaz/subscribe.html', {'form': form})

