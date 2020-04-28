from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from contacts.models import Contact
# Create your views here.
def register(request):
    if request.method=='POST':
        #Register User
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password!=password2:
            messages.error(request,"Passwords did not match")
            return redirect('accounts:register')
        else:
            if User.objects.filter(username__iexact=username).exists():
                messages.error(request,"Username is already taken")
                return redirect("accounts:register")
            else:
                if User.objects.filter(email__iexact=username).exists():
                    messages.error(request,"Email is already in use")
                    return redirect("accounts:register")
                else:
                    user=User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name)
                    user.set_password(password)
                    user.save()
                    messages.success(request,"Your have registered successfully")
                    return redirect("accounts:login")
    else:
        return render(request,"accounts/register.html")

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        print(username,password)
        user=authenticate(request,username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                #messages.success(request,"Login Successful")
                return redirect('accounts:dashboard')
            else:
                messages.error(request,"Inactive User")
                return redirect("accounts:login")
        else:
            messages.error(request,"Wrong username or password")
            return redirect("accounts:login")
    else:
        return render(request,"accounts/login.html")
@login_required
def user_logout(request):
    logout(request)
    messages.success(request,"Logout Successful")
    return redirect('pages:index')

@login_required
def dashboard(request):
    contacts=Contact.objects.filter(user_id=request.user.id)
    return render(request,"accounts/dashboard.html",{'contacts':contacts})