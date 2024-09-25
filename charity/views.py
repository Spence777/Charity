from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

import logging
# Create your views here.

def team_view():
    team_members = TeamMember.objects.all()
    return team_members

def get_causes():
    causes = Cause.objects.all()
    return causes

def Home(request):
    causes = get_causes()
    team_members = team_view()
    donations = Donation.objects.select_related('cause').order_by('-created_at')[:10]
    
    context = {
        'causes': causes,
        'donations': donations,
        'team_members': team_members
    }
    return render(request, 'charity/home.html', context)

def About(request):
    team_members = team_view()
    context = {
        'team_members': team_members
    }
    return render(request, 'charity/about.html', context)

def Causes(request):
    causes = get_causes()
    context = {
        'causes': causes
    }
    return render(request, 'charity/causes.html', context)

# def Contact(request):
#     return render(request, 'charity/contact.html')

def Gallery(request):
    # categories = CategoryImage.objects.all()
    # if category_id:
    #     images = GalleryImage.objects.filter(categoryimg_id=category_id)
    # else:
    #     images = GalleryImage.objects.all()

    # context = {
    #     'categories': categories,
    #     'images': images,
    #     'active_category': category_id,
    # }
    return render(request, 'charity/gallery.html')


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
            
            donation.save()
            # Instead of creating a PayPal form, we'll pass necessary data to the template
            context = {
                # 'form': form,
                'paypal_client_id': settings.PAYPAL_CLIENT_ID,
                'donation_amount': str(donation.amount),
                'cause_name': donation.cause.name,
                'donation_id': donation.pk,
            }

            return render(request, 'charity/donate_paypal.html', context)
        else:
            logger.warning(f"Form errors: {form.errors}")
            # return render(request, 'charity/donate.html', {'form': form})
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


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Compose the email
            subject = f"Contact Form Submission from {full_name}"
            message_body = f"Name: {full_name}\nEmail: {email}\n\nMessage:\n{message}"
            from_email = settings.EMAIL_HOST_USER
            to_email = [settings.EMAIL_HOST_USER]
            
            # Send the email
            send_mail(subject, message_body, from_email, to_email)
            
            # Redirect or render success page
            return redirect('contact_success')  
    else:
        form = ContactForm()
    
    return render(request, 'charity/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'charity/contact_success.html')


# blog views
# def blog_list(request):
#     posts = Post.objects.all().order_by('-pub_date')
#     paginator = Paginator(posts, 10)  # Show 10 posts per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     recent_posts = Post.objects.order_by('-pub_date')[:5]  # Get 5 most recent posts
#     categories = Category.objects.all()

#     context = {
#         'page_obj': page_obj,
#         'recent_posts': recent_posts,
#         'categories': categories,
#     }
#     return render(request, 'charity/blog_list.html', context)

# def blog_detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     recent_posts = Post.objects.exclude(id=post.id).order_by('-pub_date')[:5]
#     categories = Category.objects.all()

#     context = {
#         'post': post,
#         'recent_posts': recent_posts,
#         'categories': categories,
#     }
#     return render(request, 'charity/blog_detail.html', context)

# @login_required
# def add_comment(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         if content:
#             Comment.objects.create(post=post, author=request.user, content=content)
#     return redirect('blog_detail', slug=slug)

# Blog home view (List of posts)
def blog_home(request):
    posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Getting the latest 5 blog posts for the sidebar
    latest_posts = Post.objects.order_by('-pub_date')[:5]

    context = {
        'page_obj': page_obj,
        'latest_posts': latest_posts,
    }
    return render(request, 'charity/blog_home.html', context)

# Single post view
def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()  # Fetch comments related to this post

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    else:
        comment_form = CommentForm()
    latest_posts = Post.objects.order_by('-pub_date')[:5]
    context = {
        'post': post,
        'latest_posts': latest_posts,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'charity/blog_detail.html', context)

# Category view (List posts by category)
def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category).order_by('-pub_date')
    latest_posts = Post.objects.order_by('-pub_date')[:5]
    context = {
        'category': category,
        'posts': posts,
        'latest_posts': latest_posts,
    }
    return render(request, 'charity/category_posts.html', context)