
from django.contrib import admin
from paypal.standard.ipn import urls as paypal_urls
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('charity.urls')),
    path('paypal/', include(paypal_urls)),
]
