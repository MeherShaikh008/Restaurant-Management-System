from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout  # ✅ correct auth import

import razorpay
from .models import *

# Create your views here.

def index(request):
    if not request.session.get('IS_LOGIN'):
        return redirect('login.html')
    pr = Images.objects.all()
    nn = down.objects.all()
    our = Our.objects.all()
    NM = {
        'PRE' : pr,
        'FRE' : nn,
        'OUR' : our
     }
    if request.method == "POST":
        Day = request.POST.get('DAY')
        Hour = request.POST.get('HOUR')
        Name = request.POST.get('NAME')
        Phone = request.POST.get('PHONE')
        Person = request.POST.get('PERSON')
        Data = Book(day=Day,hour=Hour,name=Name,phone=Phone,person=Person)
        Data.save()
    return render(request,"index.html",NM)
    # return render(request,'index.html')

# def menu(request):
#     mn = Food.objects.all()
#     NN = {
#             'food': mn
#       }
    
#     return render(request,"menu.html",NN)
def menu(request):
    if not request.session.get('IS_LOGIN'):
        return redirect('login.html')
    foods = Menu_f.objects.all()
    FD = {
        'food': foods,
    }
    return render(request, 'menu.html',FD)


def blog(request):
    if not request.session.get('IS_LOGIN'):
        return redirect('login.html')
    bl = Blog.objects.all()
    BL = {
        'BLOG' : bl,

    }
    return render(request,'blog.html',BL)

def contact(request):
    if not request.session.get('IS_LOGIN'):
        return redirect('login.html')
    if request.method == "POST":
        Email = request.POST.get('EMAIL')
        Name = request.POST.get('NAME')
        Phone = request.POST.get('PHONE')
        Message = request.POST.get('MESSAGE')
        Data = ContactForm(name=Name,email=Email,phone=Phone,message=Message)
        Data.save()
        return redirect("index.html")
    return render(request,'contact.html')

def book(request):
    if not request.session.get('IS_LOGIN'):
        return redirect('login.html')
    if request.method == "POST":
        Day = request.POST.get('DAY')
        Hour = request.POST.get('HOUR')
        Name = request.POST.get('NAME')
        Phone = request.POST.get('PHONE')
        Person = request.POST.get('PERSON')
        Data = Book(day=Day,hour=Hour,name=Name,phone=Phone,person=Person)
        Data.save()
        return redirect("index.html")
    return render(request,'Book.html')

def registration(request):
    if request.method == 'POST':
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        formdata=Registration(fname=fname,lname=lname,email=email,password=password)
        formdata.save()
        messages.success(request, 'Thank you for Registration. Now Login')
        return redirect('login.html')
    return render(request,"registration.html")


# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         formdata=Registration.objects.all().filter(email=email,password=password).count()
        
#         if formdata>0:
#             request.session['IS_LOGIN'] = True
#             request.session['email']=email
#             return redirect('index.html')
#         else:
#             messages.error(request,"Wrong Email and password")
#             return redirect('login.html')
        
#     return render(request,"login.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        formdata=Registration.objects.all().filter(email=email,password=password).count()
        
        if formdata>0:
            request.session['IS_LOGIN'] = True
            request.session['email'] = email
            return redirect('index.html')   # home page
        else:
            messages.error(request, "Wrong Email or Password")
            # return redirect('login.html')

    return render(request, "login.html")


def logout(request):
    request.session.flush()
    return redirect('login.html')


def order_page(request):
    foods = Food.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            total_amount=0
        )

        total = 0

        for food in foods:
            qty = int(request.POST.get(f"qty_{food.id}", 0))
            if qty > 0:
                price = food.price * qty
                total += price

                OrderItem.objects.create(
                    order=order,
                    food=food,
                    quantity=qty,
                    price=price
                )

        if total == 0:
            order.delete()
            return render(request, "order.html", {
                "foods": foods,
                "error": "Please select at least one item"
            })

        order.total_amount = total
        order.save()

        return redirect("payment", order.id)

    return render(request, "order.html", {"foods": foods})

def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    client = razorpay.Client(
        auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f')
    )

    razorpay_order = client.order.create({
        "amount": order.total_amount * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        "order": order,
        "razorpay_order_id": razorpay_order["id"],
        "amount": order.total_amount
    }

    return render(request, "payment.html", context)


# Success page
def success(request):
    if request.method == 'POST':
        response = request.POST
        params_dict = {
            'razorpay_order_id': response.get('razorpay_order_id'),
            'razorpay_payment_id': response.get('razorpay_payment_id'),
            'razorpay_signature': response.get('razorpay_signature'),
        }

        client = razorpay.Client(auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f'))

        try:
            client.utility.verify_payment_signature(params_dict)
            payment_obj = Payment.objects.get(order_id=params_dict['razorpay_order_id'])
            payment_obj.razorpay_payment_id = params_dict['razorpay_payment_id']
            payment_obj.paid = True
            payment_obj.save()
            status = True
        except Exception as e:
            print(f"Error: {str(e)}")
            status = False

        return render(request, 'success.html', {'status': status})
    return redirect('order_page')