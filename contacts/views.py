from django.shortcuts import render,redirect
from .models import Contact
from django.contrib import messages
from listings.models import Listing 
from django.core.mail import send_mail
# Create your views here.
def contact(request):
    if request.method=="POST":
        print(request.POST)
        listing_id=request.POST['listing_id']
        listing=request.POST['listing']
        name=request.POST['name']
        email=request.POST['email']
        realtor_email=request.POST['realtor_email']
        phone=request.POST['phone']
        message=request.POST['message']
        user_id=request.POST['user_id']
        contact=Contact.objects.create(listing=listing,listing_id=listing_id,
                                        name=name,email=email,phone=phone,
                                        message=message,
                                        user_id=user_id)
        contact.save()
        if request.user.is_authenticated:
            hascontacted=Contact.objects.filter(listing_id=listing_id,user_id=user_id)
            messages.error(request,"your have already enquired property")
            return redirect("/listings/"+listing_id)
        else:
            messages.success(request,"Registration Successful")
            send_mail(
                'People Has Shown Intrest',
                message="person has shown intrest on your property check your dashboard",
                fail_silently=False,from_email='akshayvk64@gmail.com',
                recipient_list=[realtor_email,]
            )
    else:
        messages.error(request,"Registration Failure")

    return redirect("/listings/"+listing_id)