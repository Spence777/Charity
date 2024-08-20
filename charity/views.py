from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings
from decimal import Decimal
from django.shortcuts import render, redirect
from .forms import *
from .models import *

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

import logging
# Create your views here.

def get_causes():
    causes = Cause.objects.all()
    return causes

def Home(request):
    causes = get_causes()
    context = {
        'causes': causes
    }
    return render(request, 'charity/home.html', context)

def About(request):
    return render(request, 'charity/about.html')

def Causes(request):
    causes = get_causes()
    context = {
        'causes': causes
    }
    return render(request, 'charity/causes.html', context)

def Contact(request):
    return render(request, 'charity/contact.html')

@csrf_exempt
@require_POST
def paypal_transaction_complete(request):
    data = json.loads(request.body)
    # Here you would typically:
    # 1. Verify the transaction details with PayPal
    # 2. Update your database to mark the donation as paid
    # 3. Send a confirmation email to the donor
    # For now, we'll just return a success response
    return JsonResponse({"status": "success"})

# def Donate(request):
#     if request.method == 'POST':
#         form = DonationForm(request.POST)
#         if form.is_valid():
#             donation = form.save(commit=False)
            
#             # Update the cause's raised amount
#             cause = donation.cause
#             cause.raised_amount += donation.amount
#             cause.save()
            
#             # PayPal Payment Setup
#             paypal_dict = {
#                 'business': settings.PAYPAL_RECEIVER_EMAIL,
#                 'amount': str(donation.amount),
#                 'item_name': f'Donation for {donation.cause.name}',
#                 'invoice': f'DONATION-{donation.pk}',
#                 'currency_code': 'USD',
#                 'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
#                 'return_url': request.build_absolute_uri(reverse('donation_success')),
#                 'cancel_return': request.build_absolute_uri(reverse('donation_cancel')),
#             }

#             paypal_form = PayPalPaymentsForm(initial=paypal_dict)

#             return render(request, 'charity/donate_paypal.html', {'form': form, 'paypal_form': paypal_form})
#         else:
#             # Debugging: Show form errors if any
#             print(form.errors)
#             return render(request, 'charity/donate.html', {'form': form})

#     else:
#         form = DonationForm()

#     return render(request, 'charity/donate.html', {'form': form})



logger = logging.getLogger(__name__)

def Donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            
            # Update the cause's raised amount
            cause = donation.cause
            cause.raised_amount += donation.amount
            cause.save()
            
            # Instead of creating a PayPal form, we'll pass necessary data to the template
            context = {
                'form': form,
                'paypal_client_id': settings.PAYPAL_CLIENT_ID,
                'donation_amount': str(donation.amount),
                'cause_name': donation.cause.name,
                'donation_id': donation.pk,
            }

            return render(request, 'charity/donate_paypal.html', context)
        else:
            logger.warning(f"Form errors: {form.errors}")
            return render(request, 'charity/donate.html', {'form': form})
    else:
        form = DonationForm()

    return render(request, 'charity/donate.html', {'form': form})

def paypal_transaction_complete(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        donation_id = payload.get('donation_id')
        order_id = payload.get('orderID')
        
        try:
            donation = Donation.objects.get(pk=donation_id)
            donation.paypal_order_id = order_id
            donation.is_paid = True
            donation.save()
            
            # Here you might want to send a confirmation email to the donor
            
            return JsonResponse({'status': 'success'})
        except Donation.DoesNotExist:
            logger.error(f"Donation with id {donation_id} not found")
            return JsonResponse({'status': 'error', 'message': 'Donation not found'}, status=404)
        except Exception as e:
            logger.error(f"Error processing PayPal transaction: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def donation_success(request):
    return render(request, 'charity/donation_success.html')

def donation_cancel(request):
    return render(request, 'charity/donation_cancel.html')
