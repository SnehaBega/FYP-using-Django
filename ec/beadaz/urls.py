from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm
from .forms import MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm


urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path('about/', views.about,name="about"),
    path('contact/', views.contact,name="contact"),
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("category-title/<val>", views.CategoryTitle.as_view(), name="category-title"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    # path('paymentdone/', views.payment-done, name='paymentdone'),
    # path('orders/', views.orders, name='orders'),
    path('search/', views.search , name='search'),
    path('workshops/', views.workshops, name='workshops'),  # Define URL for workshops page
    path('repair/', views.repair, name='repair'),  # Define URL for workshops page
    path('replacement/', views.replacement, name='replacement'),  # Define URL for workshops page  
    path('resizing/', views.resizing, name='resizing'),  # Define URL for workshops page  resizing
    
    

    path('blog/', views.blog, name='blog'),  # Define URL for workshops page
    path('blog/', views.blogDetail, name='blogDetail'),
    path ('forms/', views.forms, name="forms"),
        
    #for customization of forms
    path('CustomizationForm/',views.CustomizationForm, name='CustomizationForm'),
    
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('pluswishlist/', views.plus_wishlist),
    path('minuswishlist/', views.minus_wishlist),   
               
    path('testimonials/', views.testimonials, name='testimonials'),
    
    #login authentication
    path("registration/", views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='beadaz/login.html',
    authentication_form= LoginForm) , name='login'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='beadaz/changepassword.html',
    form_class=MyPasswordChangeForm ,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name= 'beadaz/passwordchangedone.html'),
    name='passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page="login"), name="logout"),
    # path("restring/", views.RestringView.as_view(), name='restring'),
    
    #forget password (changing password)
    path('password-reset/', auth_view.PasswordResetView.as_view
    (template_name= 'beadaz/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),  
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='beadaz/password_reset-done.html'),
    name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='beadaz/password_reset_confirm.html',
    form_class= MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='beadaz/password_reset_complete.html')
    , name='password_reset_complete'),
    
   
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Beadazzle Shop"
admin.site.site_title = "Beadazzle Shop"
admin.site.site_index_title = "❝ We say it's handscrafted but it really comes from our heart♡ ❞"
