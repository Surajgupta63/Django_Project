from django.shortcuts import render, redirect
from home.models import Contact
from datetime import datetime
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect('/login')

    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == 'POST':
        name  = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc  = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, "Your message has been sent successfully.")
        
    return render(request, 'contact.html')


## User Authentication

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect('/')
        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')
