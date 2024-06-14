from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

User = get_user_model()

def login_page(request):
    if request.method=="POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')


        if not CustomUser.objects.filter(phone_number = phone_number).exists :
            messages.error(request, 'Invalid Username.')
            return redirect('/user-login/')
        
        user = authenticate(phone_number = phone_number , password = password)
        queryset = CustomUser.objects.filter(phone_number = phone_number)
        

        if user is None:
            messages.error(request, 'Invalid Password.')
            return redirect('/user-login/')
        
        elif queryset.first().is_vendor:
            login(request, user)
            return redirect('/vendor-profile/{}/'.format(user.id))
        else:
            login(request, user)
            return redirect('/') 
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/')

def UserRegister(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name') #the data of 'first_name' name field sent by post method is get using this and stored in the var.   
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        address = request.POST.get('address')
        is_vendor=request.POST.get('is_vendor')
    

        user= CustomUser.objects.filter(phone_number = phone_number)

        if user.exists():
            messages.info(request, 'Phone number already taken.')
            return redirect('/user-register/')

        # CustomUserManager.create_user(email=email, phone_number=phone_number, first_name=first_name, last_name=last_name, address=address)

        user= CustomUser.objects.create_user(
        first_name = first_name,
        last_name = last_name,
        email = email,
        phone_number = phone_number,
        password = password,
        address = address,
        is_vendor = is_vendor
        )
        

        messages.info(request, 'Account created successfully!')
        if user.is_vendor:
            return redirect('/vendor-info/{}/'.format(user.id))
        else:
            return redirect('/user-login/') 
    
    
    return render(request, 'register.html')

@login_required(login_url="/user-login")
def VendorInfo(request, vendor_id):
    if request.method == 'POST':
        user = CustomUser.objects.filter(id = vendor_id).first()
        menu = request.POST.get('menu')
        business_name = request.POST.get('business_name')
        profile_image = request.FILES.get('profile_image')
        price = request.POST.get('price_per_month')
        vendor = VendorInformation.objects.create(user=user, menu=menu, business_name=business_name, profile_image=profile_image, price = price)
        return redirect('/user-login/')
    else:
        # Form is not valid, handle this case (e.g., show errors)
        pass
    

    return render(request, 'VendorForm.html')

def home(request):
    users_with_vendor_info = VendorInformation.objects.all()
    context = {'users': users_with_vendor_info}
    return render(request, 'home.html', context)

    
@login_required(login_url="/user-login")
def ReadMoreVendorInfo(request, vendor_id):
    user = VendorInformation.objects.filter(user_id = vendor_id).first()
    
    context = {'vendor' : user}

    return render(request, 'read_more_vendor.html', context)

@login_required(login_url="/user-login")
def VendorProfile(request, vendor_id):
    user = VendorInformation.objects.filter(user_id = vendor_id).first()
    
    context = {'user' : user}

    return render(request, 'vendor_profile.html', context)

@login_required(login_url="/user-login")
def Update_Profile(request , vendor_id):
    queryset = VendorInformation.objects.filter(user_id =vendor_id).first()#to be edited.

    if request.method == "POST":
        data=request.POST
        business_name = data.get('business_name')
        menu = data.get('menu')
        price = data.get('price_per_month')
        profile_image = request.FILES.get('profile_image')

        queryset.business_name = business_name
        queryset.menu = menu
        queryset.price = price
        
        if profile_image:#if entered by user
            queryset.profile_image = profile_image

        queryset.save()
        return redirect('/vendor-profile/{}/'.format(vendor_id))

    context = {'user': queryset}
    return render(request , 'update_Menu.html', context)
    
@login_required(login_url="/user-login")
def subscribe_vendor(request, vendor_id):
    vendor = VendorInformation.objects.get(user_id=vendor_id)
    user = request.user

    # Check if the user is already subscribed to the vendor
    subscription = Subscription.objects.filter(user=user, vendor=vendor).first()

    if subscription:
        # If the user is already subscribed but has unsubscribed in the past, update the existing subscription
        if subscription.date_unsubscribed:
            subscription.date_subscribed=timezone.now()
            subscription.date_unsubscribed = None
            subscription.save()
            messages.success(request, 'You have subscribed again to this vendor.')
        else:
            messages.error(request, 'You are already subscribed to this vendor.')
    else:
        # Subscribe the user to the vendor
        Subscription.objects.create(user=user, vendor=vendor, date_subscribed=timezone.now())
        messages.success(request, 'You have subscribed to this vendor.')

    return redirect('/read-vendor-info/{}/'.format(vendor_id))

@login_required(login_url="/user-login")
def unsubscribe_vendor(request, vendor_id):
    vendor = VendorInformation.objects.get(user_id=vendor_id)
    user = request.user

    # Check if the user is subscribed to the vendor
    if not Subscription.is_subscribed(user,vendor):
        messages.error(request, 'You are not subscribed to this vendor.')
        return redirect('/read-vendor-info/{}/'.format(vendor_id))


    # Unsubscribe the user from the vendor
    subscription = Subscription.objects.filter(user=user, vendor=vendor).first()
    subscription.date_unsubscribed = timezone.now()
    subscription.save()
    messages.success(request, 'You have unsubscribed from this vendor.')
    return redirect('/read-vendor-info/{}/'.format(vendor_id))

@login_required(login_url="/user-login")
def view_customers(request):
    vendor = request.user.vendor_information
    current_customers = Subscription.objects.filter(vendor=vendor, date_unsubscribed__isnull=True)
    past_customers = Subscription.objects.filter(vendor=vendor, date_unsubscribed__isnull=False).order_by('-date_unsubscribed')
    context = {
        'current_customers': current_customers,
        'past_customers': past_customers,
    }
    return render(request, 'customers.html', context)
   

@login_required(login_url="/user-login")
def view_subscribed_vendors(request):
    current_vendors = Subscription.objects.filter(user=request.user, date_unsubscribed__isnull=True)
    past_vendors = Subscription.objects.filter(user=request.user, date_unsubscribed__isnull=False).order_by('-date_unsubscribed')
    context = {
        'current_vendors': current_vendors,
        'past_vendors': past_vendors,
    }
    return render(request, 'subscribed_vendors.html', context)