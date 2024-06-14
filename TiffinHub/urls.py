"""
URL configuration for TiffinHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MainApp.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home , name="home"),
    path('user-register/', UserRegister , name="register"),
    path('user-login/', login_page , name="login_page"),
    path('logout/', logout_page , name="logout_page"),
    path('vendor-info/<vendor_id>/', VendorInfo , name="VendorInfo"), #for input of data
    path('vendor-profile/<vendor_id>/', VendorProfile, name="VendorProfile"), # vendor will see
    path('read-vendor-info/<vendor_id>/', ReadMoreVendorInfo , name="ReadMoreVendorInfo"), #user will see
    path('update-profile/<vendor_id>/', Update_Profile, name="Update_Profile"), # vendor will update
    path('customers/', view_customers, name="view_customers"), # to see customers
    path('subscribed-vendors/', view_subscribed_vendors, name="view_subscribed_vendors"), # to see vendors
    path('subscribe/<vendor_id>/', subscribe_vendor, name="subscribe_vendor"),
    path('unsubscribe/<vendor_id>/', unsubscribe_vendor, name="unsubscribe_vendor"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
