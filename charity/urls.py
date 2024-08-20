from django.urls import path
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    
    path('', Home, name='home'),
    path('about/', About, name='about'),
    path('causes/', Causes, name='causes'),
    path('contact/', Contact, name='contact'),
    path('donate/', Donate, name='donate'),
    path('paypal-transaction-complete/', paypal_transaction_complete, name='paypal_transaction_complete'),
    path('donation-success/', donation_success, name='donation_success'),
    path('donation-cancel/', donation_cancel, name='donation_cancel'),
    

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)