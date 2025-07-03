from django.shortcuts import render, redirect, HttpResponse
from home.models import Contact
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .PayTm import Checksum
from dotenv import load_dotenv
import os

load_dotenv()

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
    print("Routed to contact")
    if request.method == 'POST':
        name   = request.POST.get('name')
        email  = request.POST.get('email')
        phone  = request.POST.get('phone')
        amount = request.POST.get('amount')
        desc   = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, amount=amount, desc=desc, date=datetime.today())
        contact.save()

        param_dict = {
                'MID': os.getenv('MERCHANT_ID'),
                'ORDER_ID': str(contact.id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handleRequest',
        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, os.getenv('MERCHANT_KEY'))
        return render(request, 'paytm.html', {'param_dict': param_dict})
    
        ## messages.success(request, "Your message has been sent successfully.")

        
    return render(request, 'contact.html')


## User Authentication

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')


## Paytm Gateway Integration Request ke liye
@csrf_exempt
def handleRequest(request):

    return HttpResponse("Your Payments is done")
    # form = request.POST
    # response_dict = {}
    # for i in form.keys():
    #     response_dict[i] = form[i]
    #     if i == 'CHECKSUMHASH':
    #         checksum = form[i]
    
    # verify = Checksum.verify_checksum(response_dict, os.getenv('MERCHANT_KEY'), checksum)
    # if verify:
    #     if response_dict['RESPCODE'] == '01':
    #         print('payment succesfull.')
    #     else:
    #         print('payment unsuccessfull because ' + response_dict['RESPMSG'])

    # return render(request, 'paymentstatus.html', {'response': response_dict})
