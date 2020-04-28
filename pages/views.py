from django.shortcuts import render
from django.http import HttpResponse
from listings.models import *
from realtors.models import *
# Create your views here.
def index(request):
    listings=Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    return render(request,"pages/index.html",{'listings':listings})

def about(request):
    realtors=Realtor.objects.order_by('-hire_date')
    mvp_realtors=Realtor.objects.all().get(is_mvp=True)
    print(mvp_realtors)
    context={
        'realtors':realtors,
        'mvp_realtors':mvp_realtors
    }
    return render(request,"pages/about.html",context)