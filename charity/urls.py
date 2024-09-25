from django.urls import path
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    
    path('', Home, name='home'),
    path('about/', About, name='about'),
    path('causes/', Causes, name='causes'),
    path('contact/', contact_view, name='contact'),
    path('gallery/', Gallery, name='gallery'),
    # path('gallery/category/<int:category_id>/', Gallery, name='gallery_category'),
    path('donate/', Donate, name='donate'),
    path('paypal-transaction-complete/', paypal_transaction_complete, name='paypal_transaction_complete'),
    # path('send-message/', contact_view, name='send_message'),
    path('contact-success/', contact_success, name='contact_success'),
    path('donation-success/', donation_success, name='donation_success'),
    path('donation-cancel/', donation_cancel, name='donation_cancel'),
    # path('blog-list', blog_list, name='blog_list'),
    # path('<slug:slug>/', blog_detail, name='blog_detail'),
    # path('<slug:slug>/add-comment/', add_comment, name='add_comment')
    path('blog/', blog_home, name='blog_home'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)