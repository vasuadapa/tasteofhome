from django.shortcuts import render
import io
import json

import requests
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse


from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User_data, Code, Address, Contact, Category, Menu, Driver, Size, Variations, Admin_user, Promocodes, Admin_user, Meals, Takeawayclosetime, Timings,Order,Subscriber_list,Balance,Note,Catering_menu
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout

from django.http import HttpResponseForbidden

import datetime
from django.db.models import Q
from datetime import datetime
from django.core.files.base import ContentFile
from PIL import Image

from django.contrib import messages

from django.core.files.storage import FileSystemStorage

from django.views.decorators.csrf import csrf_exempt

from django.template import RequestContext
fss = FileSystemStorage()
now = datetime.now()
dt_string = now.strftime("%d%m%Y%H%M%S")
date_string = now.strftime("%d%m%Y")

day_name = now.strftime('%A')

from django.conf import settings
from django.core.mail import send_mail


import os

from django.db.models import Q

import random

import datetime
date_now = datetime.date.today()
years_to_add = date_now.year + 1

date_1 = date_now.strftime('%Y-%m-%d')
date_2 = date_now.replace(year=years_to_add).strftime('%Y-%m-%d')

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#
# # Create message container - the correct MIME type is multipart/alternative.
# msg = MIMEMultipart('alternative')
# msg['Subject'] = "welcome to Teohome"
#
# # Create the body of the message (a plain-text and an HTML version).
# text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
# html = """\
# <html>
#   <head></head>
#   <body>
#     <p>Hi!<br>
#        How are you?<br>
#        Here is the <a href="http://www.python.org">link</a> you wanted.
#     </p>
#   </body>
# </html>
# """
#
# # Record the MIME types of both parts - text/plain and text/html.
# part1 = MIMEText(text, 'plain')
# part2 = MIMEText(html, 'html')
#
# # Attach parts into message container.
# # According to RFC 2046, the last part of a multipart message, in this case
# # the HTML message, is best and preferred.
# msg.attach(part1)
# msg.attach(part2)
#
# to = ('ravi.kiran.25494@gmail.com',)
# subject = 'welcome to Teohome'
# message = msg.as_string()
# email_from = settings.EMAIL_HOST_USER
# recipient_list = to
# send_mail(subject, message, email_from, recipient_list)

def get_cookies(request):
    get_email = request.COOKIES.get('get_email')
    get_name = request.COOKIES.get('name')
    type = request.COOKIES.get('type')
    return {"get_email":get_email,"get_name":get_name,"type":type}
subscri_plan =[{'name':"Veg Subscription Plan","meals_text":"5 * VEG MEALS WEEKLY SUBSCRIPTION","desc":"5 * Veg Meals Each Day Monday To Friday","price":60,"Addons1":"Roti","Addons2":"Rice (280ml)","Addons1_price":0.90,"Addons2_price":2.00},
               {'name':"Non Veg Subscription Plan","meals_text":"5 * NON VEG MEALS WEEKLY SUBSCRIPTION","desc":"5 * Non-Veg Meals Each Day Monday To Friday","price":65,"Addons1":"Roti","Addons2":"Rice (280ml)","Addons1_price":0.90,"Addons2_price":2.00}]
@api_view(['GET'])
def index1(request):
    return HttpResponse("Welcomepage Testeohome")


def index(request):
    cookies = get_cookies(request)
    meals_data = Meals.objects.filter(day=day_name).filter(status=0).filter(
        ~Q(specials='active'))
    specials_data = Meals.objects.filter(day=day_name).filter(status=0).filter(specials='active')
    combo_data = Meals.objects.filter(day=day_name).filter(status=0).filter(combo='active').order_by('id')[:5]

    return render(request, 'index.html',{"cookies":cookies,"day_name":day_name,"meals_data":meals_data,"specials_data":specials_data,"combo_data":combo_data})
def about(request):
    cookies = get_cookies(request)
    return render(request, 'about.html', {"cookies": cookies})
def contact(request):
    cookies = get_cookies(request)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact = Contact(name=name, subject=subject, email=email,message=message)
        contact.save()

        try:
            to = (request.data['email'],)
            subject = 'welcome to Teohome'
            message = f'Hi, thank you for contact us. Our team will contact to you soon.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = to
            send_mail(subject, message, email_from, recipient_list)
        except:
            print("email send fail")

        messages.success(request, 'Thank You . Our Team Will Contact You Soon...')
    return render(request, 'contact.html', {"cookies": cookies})
def catering(request):
    cookies = get_cookies(request)
    cat_data = Catering_menu.objects.all().order_by('-id')
    img_name = cat_data[0].image
    return render(request, 'catering.html', {"cookies": cookies,"img_name":img_name})
def forgot_password(request):
    cookies = get_cookies(request)
    if request.method == 'POST':
        messages.success(request, 'Check your Mail Verify link sent.')
        try:
            to = (request.data['email'],)
            subject = 'welcome to Teohome'
            message = "http://127.0.0.1:8081/verify-password/"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = to
            send_mail(subject, message, email_from, recipient_list)
        except:
            print("email send fail")
            messages.error(request, '')
        return render(request, 'forgot-password.html', {"cookies": cookies})
    else:
        return render(request, 'forgot-password.html', {"cookies": cookies})
def verify_password(request):
    cookies = get_cookies(request)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        verify_code = request.POST['vr_code']
        return render(request, 'verify-password.html')
    else:
        return render(request, 'verify-password.html', {"cookies": cookies})

def login(request):
    from datetime import datetime, timedelta
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_data = User_data.objects.filter(Q(email=email) | Q(mobile=email)).filter(password=password).filter(status=0).last()
        driver_data = Driver.objects.filter(email=email).filter(password=password).filter(status=0).last()
        if user_data:
            response = HttpResponse("Cookie Set")
            # response.set_cookie('email', email)
            name = user_data.email.split("@")
            response.cookies['email'] = email
            response.cookies['name'] = name[0]
            messages.success(request, 'Thank you for login.')
            response = render(request, 'menu.html', {"get_email": name[0]})
            response.set_cookie('last_connection', datetime.now())
            response.set_cookie('get_email', email)
            response.set_cookie('name', name[0])
            response.set_cookie('type', 'Customer')

            return response
        elif driver_data:
            response = HttpResponse("Cookie Set")
            name = driver_data.email.split("@")
            response.cookies['email'] = email
            response.cookies['name'] = name[0]
            messages.success(request, 'Thank you for login.')
            code_data = Code.objects.filter(driver=driver_data).filter(status=0).last()
            order_today = Order.objects.filter(order_date=date_1).filter(order_status='In process').filter(order_address_customer_id=code_data)
            order_completed = Order.objects.filter(order_date=date_1).filter(order_status='Completed').filter(order_address_customer_id=code_data)
            response = render(request, 'driver1.html', {"get_email": name[0],"order_today":order_today,"order_completed":order_completed})
            response.set_cookie('last_connection', datetime.now())
            response.set_cookie('get_email', email)
            response.set_cookie('name', name[0])
            response.set_cookie('type', 'driver')

            return response
        else:
            messages.error(request, 'Please Check Your User Name and Password !')
            return render(request, 'login.html')
    else:
        messages.error(request, '')
        return render(request, 'login.html')
def menu(request):
    cookies = get_cookies(request)
    return render(request, 'menu.html',{"cookies": cookies,"get_email":'test'})
def takeaway(request):
    cookies = get_cookies(request)
    user_data = User_data.objects.filter(email=cookies['get_email']).last()
    address = Address.objects.filter(user=user_data.id)
    if address:
        address_exist = "yes"
    else:
        address_exist = "no"
    meals_data = Meals.objects.filter(day=day_name).filter(delivery_type='Pickup').filter(status=0).filter(~Q(specials='active'))
    specials_data = Meals.objects.filter(delivery_type='Pickup').filter(status=0).filter(specials='active')
    return render(request, 'takeaway-menu.html',{"address_exist":address_exist,"cookies": cookies,"meals_data":meals_data,"day_name":day_name,"specials_data":specials_data})
def delivery(request):
    cookies = get_cookies(request)
    meals_data = Meals.objects.filter(day=day_name).filter(delivery_type='Home Delivery').filter(status=0).filter(~Q(specials='active'))
    specials_data = Meals.objects.filter(delivery_type='Pickup').filter(status=0).filter(specials='active')
    return render(request, 'delivery-menu.html',{"cookies": cookies,"meals_data":meals_data,"day_name":day_name,"specials_data":specials_data})

def subscription(request):
    cookies = get_cookies(request)
    return render(request, 'subscription.html',{"cookies": cookies,"subscri_plan":subscri_plan})

def subscription_update(request):
    if request.method == "POST":
        plane = request.POST['plan_price']
        roti_price = request.POST['roti_price']
        rice_price = request.POST['rice_price']
        type = request.POST['veg_nv']

        if type == "veg":
            subscri_plan[0]['price'] = plane
            subscri_plan[0]['Addons1_price'] = roti_price
            subscri_plan[0]['Addons2_price'] = rice_price
        else:
            subscri_plan[1]['price'] = plane
            subscri_plan[1]['Addons1_price'] = roti_price
            subscri_plan[1]['Addons2_price'] = rice_price


    return redirect("app:admin_subscription_plans")

def subscription_details(request,id):
    cookies = get_cookies(request)
    order_data = Order.objects.filter(order_id=id).distinct("order_date")

    return render(request, 'subscription-details.html',{"order_end_date":order_data[len(order_data)-1].order_date,"order_data_len":len(order_data)-1,"cookies": cookies,"order_data":order_data,"order_id":id})

def order_details(request,id):
    cookies = get_cookies(request)
    order_data = Order.objects.filter(id=id).last()
    total = int(order_data.meals_date.price) * int(order_data.meals_date.qty)
    g_total = total+ int(order_data.meals_date.delivery_price)+int(order_data.order_discount_price)
    price_list = {"total":total,"grand_total":g_total}

    return render(request, 'order-details.html',{"cookies": cookies,"order_data":order_data,"price_list":price_list})

def driver1(request):
    cookies = get_cookies(request)
    if cookies['type']=="driver":
        driver_data  = Driver.objects.filter(email=cookies['get_email']).last()
        code_data = Code.objects.filter(driver=driver_data).filter(status=0).last()
        order_today = Order.objects.filter(order_date=date_1).filter(order_status='In process').filter(
            order_address_customer_id=code_data)
        order_completed = Order.objects.filter(order_date=date_1).filter(order_status='Completed').filter(
            order_address_customer_id=code_data)

        return render(request, 'driver1.html',{"cookies": cookies,"order_today":order_today,"order_completed":order_completed})
    else:
        return redirect("app:login")

@csrf_exempt
def user_ajax_addtocart(request):
    id = request.POST['id']
    menu_model_data = Meals.objects.filter(id=id).last()
    meal_fix_item = []
    meal_item = []
    for fim in menu_model_data.fixed_item.split("+"):
        meal_fix_item.append({ "name": fim, "description": fim, "quantity": 0 })

    for it in menu_model_data.item.split("+"):
        meal_item.append({ "name": it, "description": it, "quantity": 0 })

    fixed_item = meal_fix_item
    items = meal_item
    fixed_item_quantity =  menu_model_data.fixed_item_quantity
    # fixed_item_quantity = "YOU CAN CHOOSE 2 ITEMS OUT OF 4"
    qty = menu_model_data.qty

    data = {"qty":qty,"price": menu_model_data.price,"fixed_item_quantity":fixed_item_quantity,"name_id":menu_model_data.name_id,"fixed_item":fixed_item ,"meal_text": menu_model_data.meal_text,"id": id,"description": menu_model_data.description,"item":items,}
    return JsonResponse({'data': data})


def register(request):
    cookies = get_cookies(request)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        user_data = User_data.objects.filter(email=email)
        if user_data:
            messages.error(request, 'This user already register. Please give another email!')
            return render(request, 'register.html', {"cookies": cookies})
        else:
            if password == cpassword:
                user = User_data(name=name, password=password, email=email,user_type="Customer",mobile=mobile)
                user.save()
                try:
                    to = (email,)
                    subject = 'welcome to Teohome'
                    message = f'Hi, thank you for Registering'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = to
                    send_mail(subject, message, email_from, recipient_list)
                except:
                    print("email send fail")
                messages.success(request, 'Thank you for Registering.')
                return render(request, 'register.html', {'recepient': "test"})
            else:
                messages.error(request, 'Password and confirm password was not same')
                return render(request, 'register.html', {"cookies": cookies})
    else:
        return render(request, 'register.html', {"cookies": cookies})
def sign_out(request):
    cookies = get_cookies(request)
    response = render(request, 'index.html', {"cookies": cookies,"get_email": "test"})
    response.set_cookie('get_email', "")
    response.set_cookie('name', "")
    response.set_cookie('type', "")
    response.set_cookie('last_connection', "")
    return response
def user_admin(request):
    cookies = get_cookies(request)
    user_address = []
    user_data = User_data.objects.filter(email=cookies['get_email']).last()
    user_details = {"id":user_data.id,"name":user_data.name,"email":user_data.email,"mobile":user_data.mobile,"password":user_data.password}
    address_details = Address.objects.filter(user=user_data.id).filter(~Q(status=2))
    order_data = Order.objects.filter(user_date=user_data.id)
    subscri_order_data = Order.objects.filter(user_date=user_data.id).filter(order_type="Subscription").distinct("order_id")

    promo_code_data = Promocodes.objects.filter(customer_id=user_data.id)

    pending_payments = Order.objects.filter(payment_status=	"Not Paid").filter(user_date=user_data.id).order_by('-id')

    for j in address_details:
        user_address.append({"id":j.id,"pincode":j.pincode,'address':j.address,"address_active":j.address_active})

    return render(request, 'user-admin.html', {"subscri_order_data":subscri_order_data,"cookies": cookies,"user_data":user_details,"user_address":user_address,"order_data":order_data,"promo_code_data":promo_code_data,"promo_code_data":promo_code_data,"pending_payments":pending_payments})

def profile_update(request):
    cookies = get_cookies(request)
    user_address = []
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']

        image = request.FILES['filename']
        static_folder = os.path.join(settings.BASE_DIR, 'app\\static')
        image_path = os.path.join(static_folder, 'images', image.name)
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        image_name = image.name.split(".")
        img_name = image_name[0] + dt_string + "." + image_name[1]

        user_data = User_data.objects.filter(email=email).last()
        user_data.name = name
        user_data.mobile = mobile
        user_data.password = password
        user_data.image = img_name
        user_data.save()
    user_data = User_data.objects.filter(email=cookies['get_email']).last()
    user_details = {"id":user_data.id,"name":user_data.name,"email":user_data.email,"mobile":user_data.mobile,"password":user_data.password}
    address_details = Address.objects.filter(user=user_data.id).filter(~Q(status=2))
    for j in address_details:
        user_address.append({"id": j.id, "pincode": j.pincode, 'address': j.address})

    return render(request, 'user-admin.html', {"cookies": cookies,"user_data":user_details,"user_address":user_address})

def address_update(request):
    cookies = get_cookies(request)
    user_data = User_data.objects.filter(email=cookies['get_email']).last()
    user_details = {"id": user_data.id, "name": user_data.name, "email": user_data.email, "mobile": user_data.mobile,
                    "password": user_data.password}
    if request.method == 'POST':
        pincode = request.POST['pincode']
        address = request.POST['address']
        user_id = request.POST['id']

        user_data = User_data.objects.filter(id=user_id).last()

        user = Address(pincode=pincode, address=address, user=user_data)
        user.save()
        return redirect("app:user_admin")
        # return render(request, 'user-admin.html', {"cookies": cookies,"user_data":user_details})

    else:
        return redirect("app:user_admin")
        # return render(request, 'user-admin.html', {"cookies": cookies,"user_data":user_details})

@csrf_exempt
def user_ajax_address_edit(request):
    id = request.POST['id']
    user_edit_data = Address.objects.filter(id=id).last()
    sub_dt = []
    sub_data = Code.objects.filter(status=0)
    for i in sub_data:
        sub_dt.append({"name": i.name, "id": i.id,"code":i.code})

    data = {"pincode": user_edit_data.pincode,"id":id,"address": user_edit_data.address,"sub_dt":sub_dt}
    return JsonResponse({'data': data})

def user_edit_address_update(request):
    id = request.POST['id']
    name = request.POST['pincode']
    address = request.POST['address']
    user_edit_data = Address.objects.filter(id=id).last()
    user_edit_data.name = name
    user_edit_data.address = address
    user_edit_data.save()
    return redirect("app:user_admin")

def address_delete(request,id):
    user_data = Address.objects.filter(id=id).last()
    user_data.status = 2
    user_data.save()
    return redirect("app:user_admin")

from datetime import datetime, timedelta, time,date

# admin dashboard functions
def admin_index(request):
    today_start = datetime.combine(date_now, time())
    total_users = User_data.objects.filter(user_type="Customer")
    suburb_data = Code.objects.all()
    user_data_active = User_data.objects.filter(active="Active")
    today_users = User_data.objects.filter(created_at__year=date_now.year, created_at__month=date_now.month, created_at__day=date_now.day)
    context = {"total_users": len(total_users),
               "today_users": len(today_users),
               "suburb_data":suburb_data,
               "user_data_active":user_data_active
               }
    return render(request, 'toh-admin/index.html',context)

def admin_categories(request):
    if request.method=="POST":
        categories = request.POST['categories']
        category = Category.objects.filter(name=categories)
        category_data = Category.objects.filter(status=0)
        context = {"category_data": category_data,
                   }
        if category:
            messages.success(request, 'Categories already added...')
        else:
            category_data = Category(name=categories)
            category_data.save()
            messages.success(request, 'Categories added successfully...')
        return render(request, 'toh-admin/Categories.html', context)
    else:
        category_data = Category.objects.filter(status=0)
        messages.success(request, '')
        context = {"category_data":category_data,}
        return render(request, 'toh-admin/Categories.html',context)

@csrf_exempt
def admin_categories_edit(request):
    id = request.POST['id']
    category_data = Category.objects.filter(id=id).last()
    data = {"name": category_data.name,"id":id}

    return JsonResponse({'data': data})
    # category_data.name = request.POST['categories']
    # category_data.save()
    # messages.success(request, 'Categories edit successfully.')
    return render(request, 'toh-admin/Categories.html', {})

def admin_categories_ed(request):
    if request.method == "POST":
        id = request.POST['cat_id']
        category_data = Category.objects.filter(id=id).last()
        category_data.name = request.POST['edit_categories']
        category_data.save()
        category_dt = Category.objects.filter(status=0)
        context = {"category_data": category_dt, }
        messages.success(request, 'Categories edit successfully.')
        return render(request, 'toh-admin/Categories.html', context)
    else:
        category_dt = Category.objects.filter(status=0)
        context = {"category_data": category_dt, }
        return render(request, 'toh-admin/Categories.html', context)

def admin_categories_delete(request,id):
    category_data = Category.objects.filter(id=id).last()
    category_data.status = 2
    category_data.save()
    category_data = Category.objects.filter(status=0)
    context = {"category_data": category_data,
               }
    messages.success(request, 'Categories deleted successfully.')
    return render(request, 'toh-admin/Categories.html', context)

def admin_items(request):
    category_data = Category.objects.filter(status=0).distinct()

    if request.method == "POST":
        category = request.POST['category']
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        delivery_type = request.POST['delivery_type']
        category_dt = Category.objects.filter(id=category).last()

        menu = Menu.objects.filter(category=category_dt).filter(name=request.POST['name']).filter(price=request.POST['price'])
        if menu:
            messages.success(request, 'Item already added')
        else:
            try:
                image = request.FILES['filename']
                static_folder = os.path.join(settings.BASE_DIR, 'app\\static')
                image_path = os.path.join(static_folder, 'images', image.name)
                image_name = image.name
                with open(image_path, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
            except:
                image_name = ''
            item_data = Menu(name=name,price=price,image=image_name,description=description,category=category_dt,delivery_type=delivery_type)
            item_data.save()
            messages.success(request, 'Item added successfully...')

    menu_data = Menu.objects.filter(status=0)
    context = {"category_data": category_data,
               "menu_data": menu_data,
               }
    return render(request, 'toh-admin/items.html',context)

@csrf_exempt
def admin_item_ajax_edit(request):

    id = request.POST['id']
    item_data = Menu.objects.filter(id=id).last()
    category_data = Category.objects.filter(status=0).distinct()
    category_dt=[]
    for i in category_data:
        category_dt.append({"name":i.name,"id":i.id})

    delivery_type_data =[{"name":"Home Delivery"},{"name":"Takeaway"}]

    data = {"delivery_type_data":delivery_type_data,"category_data":category_dt,"name": item_data.name,"id":id,"category":item_data.category.name,"price":item_data.price,"description":item_data.description,"delivery_type":item_data.delivery_type,"image":item_data.image,}

    return JsonResponse({'data': data})
    # category_data.name = request.POST['categories']
    # category_data.save()
    # messages.success(request, 'Categories edit successfully.')
    return render(request, 'toh-admin/Categories.html', {})

def admin_item_edit(request):
    category_dt = Category.objects.filter(status=0).distinct()
    if request.method == "POST":
        id = request.POST['item_id']
        aj_item = request.POST['aj_item']
        aj_category = request.POST['aj_category']
        aj_price = request.POST['aj_price']
        aj_description = request.POST['aj_description']
        aj_item_old_img = request.FILES['aj_item_old_img']
        aj_item_img = request.POST['item_img']
        aj_delivery_type = request.POST['aj_delivery_type']

        category_data = Category.objects.filter(id=aj_category).last()
        item_data = Menu.objects.filter(id=id).last()
        item_data.name = aj_item
        item_data.category = category_data
        item_data.price = aj_price
        item_data.description = aj_description
        item_data.delivery_type = aj_delivery_type
        if ((aj_item_old_img== "") or (aj_item_old_img== None)):
            item_data.image = aj_item_img
        else:
            image = aj_item_old_img
            static_folder = os.path.join(settings.BASE_DIR, 'app\\static')
            image_path = os.path.join(static_folder, 'images', image.name)
            with open(image_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            item_data.image = image.name
        item_data.save()
        item_dt = Menu.objects.filter(status=0)
        context = {"menu_data": item_dt, "category_data":category_dt}
        messages.success(request, 'Item edit successfully.')
        return render(request, 'toh-admin/items.html',context)
    else:
        item_dt = Menu.objects.filter(status=0)
        context = {"category_data": category_dt,
                   "menu_data": item_dt,
                   }
        return render(request, 'toh-admin/items.html',context)

def admin_items_delete(request,id):
    item_data = Menu.objects.filter(id=id).last()
    item_data.status = 2
    item_data.save()
    menu_data = Menu.objects.filter(status=0)
    context = {"menu_data": menu_data,
               }
    messages.success(request, 'Item deleted successfully.')
    return render(request, 'toh-admin/items.html', context)
def all_day_meals():
    meal_dt_mon = Meals.objects.filter(status=0).filter(day="Monday").order_by('-id')
    meal_dt_tues = Meals.objects.filter(status=0).filter(day="Tuesday").order_by('-id')
    meal_dt_wed = Meals.objects.filter(status=0).filter(day="Wednesday").order_by('-id')
    meal_dt_thu = Meals.objects.filter(status=0).filter(day="Thursday").order_by('-id')
    meal_dt_fri = Meals.objects.filter(status=0).filter(day="Friday").order_by('-id')
    meal_dt_sat = Meals.objects.filter(status=0).filter(day="Saturday").order_by('-id')
    meal_dt_sun = Meals.objects.filter(status=0).filter(day="Sunday").order_by('-id')
    all_meal_data = {"meal_dt_mon":meal_dt_mon,"meal_dt_tues":meal_dt_tues,"meal_dt_wed":meal_dt_wed,"meal_dt_thu":meal_dt_thu,"meal_dt_fri":meal_dt_fri,"meal_dt_sat":meal_dt_sat,"meal_dt_sun":meal_dt_sun}
    return all_meal_data
def admin_meals(request):
    category_data = Category.objects.filter(status=0).distinct()
    item_data = Menu.objects.filter(status=0).values('name').distinct()
    if request.method == "POST":
        day = request.POST['day']
        category = request.POST['category']
        items = request.POST.getlist('items')
        items1 = request.POST.getlist('itemsfixed')
        qty = request.POST['qty']
        fix_item_qty = request.POST['fix_item_qty']
        price = request.POST['price']
        meal_text = request.POST['meal_text']
        description = request.POST['description']
        select_delivery_type = request.POST['select_delivery_type']
        delivery_price = request.POST['delivery_price']
        category_dt = Category.objects.filter(id=category).last()
        items_con = ""
        items1_con = ""
        if len(items) > 1:
            for k in items:
                items_con += k +"+"
        elif len(items) == 1:
            items_con = items[0]
        else:
            items_con = ''

        if items_con[-1] == "+":
            items_con = items_con[:len(items_con) - 1]

        if len(items1) > 1:
            for l in items1:
                items1_con += l +"+"
        elif len(items1) == 1:
            items1_con = items[0]
        else:
            items1_con = ''

        if items1_con[-1] == "+":
            items1_con = items1_con[:len(items_con) - 1]

        try:
            image = request.FILES['image']
            static_folder = os.path.join(settings.BASE_DIR, 'app\\static')
            image_path = os.path.join(static_folder, 'images', image.name)
            with open(image_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            image_name = image.name
        except:
            image_name = ""
        meal_data = Meals(name=category_dt, item=items_con, fixed_item=items1_con, fixed_item_quantity=fix_item_qty,description=description,image=image_name, day=day ,price=price, qty=qty,meal_text=meal_text,delivery_price=delivery_price,delivery_type=select_delivery_type)
        meal_data.save()
        messages.success(request, 'Meal added successfully...')
    meal_dt = Meals.objects.filter(status=0).order_by('-id')
    all_meal_data = all_day_meals()
    context = {"category_data":category_data,"item_data":item_data,"meal_data": meal_dt,"all_meal_data":all_meal_data}
    return render(request, 'toh-admin/meals.html',context)

def admin_meals_delete(request,id):
    meals_data = Meals.objects.filter(id=id).last()
    meals_data.status = 2
    meals_data.save()
    meal_dt = Meals.objects.filter(status=0).order_by('-id')
    category_data = Category.objects.filter(status=0).distinct()
    item_data = Menu.objects.filter(status=0).values('name').distinct()
    messages.success(request, 'Suburb deleted successfully.')
    all_meal_data = all_day_meals()
    context = {"category_data": category_data, "item_data": item_data, "meal_data": meal_dt,"all_meal_data":all_meal_data}
    return render(request, 'toh-admin/meals.html', context)

@csrf_exempt
def user_admin_address_active(request):
    if request.method == "POST":
        id = request.POST['id']
        address_data = Address.objects.filter(id=id).last()
        address_data.address_active = request.POST['address_status']
        address_data.save()

        data = {"id": id, "meals_data": address_data.address_active}
        return JsonResponse({'data': data})

@csrf_exempt
def admin_meals_update_special(request):
    if request.method == "POST":
        id = request.POST['id']
        type = request.POST['type']
        meals_data = Meals.objects.filter(id=id).last()
        if type == "specials":
            meals_data.specials = request.POST['special_status']
        else:
            meals_data.combo = request.POST['special_status']
        meals_data.save()

        data = {"id": id, "meals_data": meals_data.specials}
        return JsonResponse({'data': data})
@csrf_exempt
def admin_user_update_special(request):
    if request.method == "POST":
        id = request.POST['id']
        user_data = User_data.objects.filter(id=id).last()
        user_data.active = request.POST['special_status']
        user_data.save()

        data = {"id": id, "meals_data": user_data.specials}
        return JsonResponse({'data': data})

def admin_meals_edit(request,id):
    if request.method == "POST":
        meals_data = Meals.objects.filter(id=id).last()
        day = request.POST['day']
        category = request.POST['category']
        items = request.POST.getlist('items')
        items1 = request.POST.getlist('itemsfixed')
        qty = request.POST['qty']
        fix_item_qty = request.POST['fix_item_qty']
        price = request.POST['price']
        meal_text = request.POST['meal_text']
        description = request.POST['description']
        select_delivery_type = request.POST['select_delivery_type']
        delivery_price = request.POST['delivery_price']
        category_dt = Category.objects.filter(id=category).last()
        items_con = ""
        items1_con = ""
        if len(items) > 1:
            for k in items:
                items_con += k + "+"
        elif len(items) == 1:
            items_con = items[0]
        else:
            items_con = ''

        if items_con[-1] == "+":
            items_con = items_con[:len(items_con) - 1]

        if len(items1) > 1:
            for l in items1:
                items1_con += l + "+"
        elif len(items1) == 1:
            items1_con = items[0]
        else:
            items1_con = ''

        if items1_con[-1] == "+":
            items1_con = items1_con[:len(items_con) - 1]

        try:
            image = request.FILES['image']
            static_folder = os.path.join(settings.BASE_DIR, 'app\\static')
            image_path = os.path.join(static_folder, 'images', image.name)
            with open(image_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            image_name = image.name
        except:
            image_name = ""

        meals_data.day = day
        meals_data.name = category_dt
        meals_data.item = items_con
        meals_data.fixed_item = items1_con
        meals_data.fixed_item_quantity = fix_item_qty
        meals_data.qty = qty
        meals_data.meal_text = meal_text
        meals_data.delivery_price = delivery_price
        meals_data.description = description
        meals_data.image = image_name
        meals_data.price = price
        meals_data.delivery_type = select_delivery_type
        meals_data.save()
    else:
        pass
    meal_dt = Meals.objects.filter(status=0).order_by('-id')
    category_data = Category.objects.filter(status=0).distinct()
    item_data = Menu.objects.filter(status=0).values('name').distinct()
    meals_data = Meals.objects.filter(id=id).last()
    fixed_item_list = meals_data.fixed_item.split("+")
    item_list = meals_data.item.split("+")
    all_meal_data = all_day_meals()

    context = {"item_list":item_list,"fixed_item_list":fixed_item_list,"category_data": category_data, "item_data": item_data, "meal_data": meal_dt,"all_meal_data":all_meal_data,"meals_data":meals_data}
    return render(request, 'toh-admin/edit-meals.html', context)

def admin_bal_edit(request,id):
    bal_data = Balance.objects.filter(id=id).last()
    user_id = bal_data.user_data.id
    if request.method == "POST":
        bal_data.amount = request.POST['amount']
        bal_data.note = request.POST['bal_note']
        bal_data.transition_type = request.POST['service_type']
        bal_data.save()
    return redirect('app:admin_customers_profile',user_id)

def admin_bal_delete(request,id):
    bal_data = Balance.objects.filter(id=id).last()
    user_id = bal_data.user_data.id
    bal_data.status = 2
    bal_data.save()
    return redirect('app:admin_customers_profile',user_id)

def admin_note_edit(request,id):
    note_data = Note.objects.filter(id=id).last()
    user_id = note_data.user_data.id
    if request.method == "POST":
        note_data.note = request.POST['note_ed']
        note_data.save()
    return redirect('app:admin_customers_profile',user_id)

def admin_note_delete(request,id):
    note_data = Note.objects.filter(id=id).last()
    user_id = note_data.user_data.id
    note_data.status = 2
    note_data.save()
    return redirect('app:admin_customers_profile',user_id)

@csrf_exempt
def admin_ajax_get_items(request):
    id = request.POST['id']
    items_data = Menu.objects.filter(category=id)
    item_dt = []
    for i in items_data:
        item_dt.append({"name":i.name,"id":id})
    data = {"id":id,"item_data":item_dt}
    return JsonResponse({'data': data})

@csrf_exempt
def admin_ajax_get_user(request):
    id = request.POST['id']
    code_data = Code.objects.filter(id=id).last()
    pin_data = code_data.name+"    "+code_data.code
    address_data = Address.objects.filter(pincode=pin_data)
    item_dt = []
    for i in address_data:
        item_dt.append({"name":i.user.name,"id":i.user.id})
    data = {"id":id,"item_data":item_dt}
    return JsonResponse({'data': data})

def admin_orders(request):
    order_data_all = Order.objects.all()
    order_data_pending = Order.objects.filter(order_status="In process")
    order_data_takeaway = Order.objects.filter(order_status="Takeaway")
    order_data_Declined = Order.objects.filter(order_status="Decline")
    order_data_Delivery = Order.objects.filter(order_status="Delivery")
    order_data_Refunded = Order.objects.filter(order_status="Refunded")
    order_data_Delivered = Order.objects.filter(order_status="Delivered")
    order_data_Undelivered = Order.objects.filter(order_status="Undelivered")
    order_data_Cancelled = Order.objects.filter(order_status="Cancelled")
    context = {"order_data_all":order_data_all,"order_data_pending":order_data_pending,"order_data_takeaway":order_data_takeaway,"order_data_Declined": order_data_Declined, "order_data_Delivery": order_data_Delivery,"order_data_Refunded": order_data_Refunded,"order_data_Delivered": order_data_Delivered, "order_data_Undelivered": order_data_Undelivered,"order_data_Cancelled": order_data_Cancelled}
    return render(request, 'toh-admin/orders.html',context)

def admin_orders_delete(request,id):
    order_data = Order.objects.filter(id=id).last()
    order_data.status = 2
    order_data.order_status ="Cancelled"
    order_data.save()
    return redirect('app:admin_orders')

def admin_orders_decline(request,id):
    order_data = Order.objects.filter(id=id).last()
    order_data.order_status ="Decline"
    order_data.save()
    return redirect('app:admin_orders')

def admin_orders_refund(request,id):
    order_data = Order.objects.filter(id=id).last()
    order_data.order_status ="Refunded"
    order_data.save()
    return redirect('app:admin_orders')

def admin_orders_payment(request,id):
    order_data = Order.objects.filter(id=id).last()
    order_data.payment_status = "Completed"
    order_data.save()
    return redirect('app:driver1')
def driver_orders_completed(request,id):
    order_data = Order.objects.filter(id=id).last()
    order_data.order_status = "Completed"
    order_data.save()
    return redirect('app:driver1')

def driver_orders_decline(request,id):
    order_data = Order.objects.filter(id=id).last()
    order_data.order_status ="Decline"
    order_data.save()
    return redirect('app:driver1')

def admin_orders_edit(request,id):
    order_data = Order.objects.filter(id=id).last()
    if request.method == "POST":
        order_data.order_id = request.POST['order_name']
        order_data.user_date.name = request.POST['cus_name']
        order_data.order_address = request.POST['address']
        # order_data.suburb = request.POST['suburb']
        order_data.order_date = request.POST['date']
        order_data.total_amt = request.POST['amt']
        order_data.order_status = request.POST['order_status']
        order_data.save()
    context = {"order_data":order_data,"id":id}
    return render(request, 'toh-admin/edit-orders.html', context)
def admin_orders_delivered(request,id):
    order_data = Order.objects.filter(id=id).last()
    order_data.order_status ="Delivered"
    order_data.save()
    return redirect('app:admin_orders')

def admin_todayreport(request):
    order_today = Order.objects.filter(order_date=date_1)

    return render(request, 'toh-admin/todayreport.html',{"order_today":order_today})
def admin_dailyorder(request):
    return render(request, 'toh-admin/dailyorder.html',{})

def admin_takeaway_close_time(request):
    if request.method=="POST":
        time = request.POST['time']
        takeaway_data = Takeawayclosetime(name=time)
        takeaway_data.save()
    code_data = Code.objects.filter(status=0)
    context = {"code_data":code_data}
    return render(request, 'toh-admin/suburb.html',context)

def admin_suburb(request):
    code_data = Code.objects.filter(status=0)
    context = {"code_data":code_data}
    return render(request, 'toh-admin/suburb.html',context)
def admin_suburb_delete(request,id):
    code_data = Code.objects.filter(id=id).last()
    code_data.status = 2
    code_data.save()
    code_data = Code.objects.filter(status=0)
    context = {"code_data": code_data}
    messages.success(request, 'Suburb deleted successfully.')
    return render(request, 'toh-admin/suburb.html', context)

def admin_suburb_edit(request,id):
    code_dt = Code.objects.filter(id=id).last()
    code_data = Code.objects.filter(status=0)
    driver_dt = Driver.objects.filter(status=0)
    context = {"code_data": code_data,"code_dt":code_dt,"driver_dt": driver_dt}
    if request.method == "POST":
        driver = Driver.objects.filter(id=request.POST['driver']).last()
        code_dt.name = request.POST['name']
        code_dt.code = request.POST['pincode']
        code_dt.food_available = request.POST['food_available']
        code_dt.driver = driver
        code_dt.timefrom = request.POST['timefrom']
        code_dt.timeto = request.POST['timeto']
        code_dt.delfrom = request.POST['delfrom']
        code_dt.delto = request.POST['delto']
        code_dt.amount = request.POST['amount']
        code_dt.delivery_type = request.POST['delivery_type']

        code_dt.save()
        messages.success(request, 'Suburb edit successfully.')
        return render(request, 'toh-admin/suburb.html', context)

    return render(request, 'toh-admin/edit-suburb.html', context)

def admin_add_suburb(request):
    if request.method == "POST":
        available = request.POST['available']
        driver = request.POST['driver']
        name = request.POST['name']
        pincode = request.POST['pincode']
        timefrom = request.POST['timefrom']
        timeto = request.POST['timeto']
        delfrom = request.POST['delfrom']
        delto = request.POST['delto']
        amount = request.POST['amount']
        deliver_type = request.POST['deliver_type']

        driver_data = Driver.objects.filter(id=driver).last()

        loc = Code(name=name,code=pincode,food_available=available,delivery_type=deliver_type,timefrom=timefrom,timeto=timeto,delfrom=delfrom,delto=delto,amount=amount,driver=driver_data)
        loc.save()
        messages.success(request, 'Suburb added successfully.')

    driver_dt = Driver.objects.filter(status=0)
    context = {"driver_dt":driver_dt}
    return render(request, 'toh-admin/add-suburb.html',context)

def admin_drivers(request):
    if request.method=="POST":
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        service = request.POST['service']
        driver = Driver.objects.filter(email=email)
        if driver:
            messages.success(request, 'Item already added')
        else:
            try:
                image = request.FILES['filename']
                static_folder = os.path.join(settings.BASE_DIR, 'app\\static')
                image_name = image.name.split(".")
                img_name = image_name[0]+dt_string+"."+image_name[1]
                image_path = os.path.join(static_folder, 'images', img_name)
                with open(image_path, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
            except:
                img_name =""
            driver_data = Driver(name=name, email=email, image=img_name, password=password, services=service)
            driver_data.save()
            messages.success(request, 'Driver added successfully...')
    driver_date = Driver.objects.filter(status=0)
    context = {"driver_date":driver_date}
    return render(request, 'toh-admin/drivers.html',context)

@csrf_exempt
def admin_driver_ajax_edit(request):

    id = request.POST['id']
    driver_data = Driver.objects.filter(id=id).last()
    data = {"id":id,"name":driver_data.name,"email":driver_data.email,"password":driver_data.password,"services":driver_data.services,"image":driver_data.image}
    return JsonResponse({'data': data})

def admin_driver_edit(request):
    if request.method == "POST":
        email = request.POST['aj_email']
        name = request.POST['aj_name']
        password = request.POST['aj_password']
        service = request.POST['aj_service']
        image = request.POST['aj_img_old']
        id = request.POST['item_id']
        driver = Driver.objects.filter(email=email)
        driver_data = Driver.objects.filter(id=id).last()
        if driver:
            messages.success(request, 'Item already added')
        else:
            if image == "":
                image = request.POST['aj_img_old']
            else:
                image = request.FILES['aj_img']
                static_folder = os.path.join(settings.BASE_DIR, 'app\\static')
                image_name = image.name.split(".")
                img_name = image_name[0] + dt_string + "." + image_name[1]
                image_path = os.path.join(static_folder, 'images', img_name)
                with open(image_path, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
            driver_data.name = name
            driver_data.email = email
            driver_data.image = image
            driver_data.password = password
            driver_data.services = service
            driver_data.save()
            messages.success(request, 'Driver updated successfully...')
    driver_dt = Driver.objects.filter(status=0)
    context = {"driver_date": driver_dt,
               }
    return render(request, 'toh-admin/drivers.html', context)

def admin_driver_delete(request,id):
    driver_data = Driver.objects.filter(id=id).last()
    driver_data.status = 2
    driver_data.save()
    driver_dt = Driver.objects.filter(status=0)
    context = {"driver_date": driver_dt,
               }
    messages.success(request, 'Driver deleted successfully.')
    return render(request, 'toh-admin/drivers.html', context)

def admin_deliverytifin(request):
    driver_dt = Driver.objects.filter(status=0)
    context = {"driver_date": driver_dt,
               }
    return render(request, 'toh-admin/deliverytifin.html',context)

def admin_order_details_1(request,id):
    code_data = Code.objects.filter(driver=id)
    order_details = []
    order_details_completed = []
    for cd in code_data:
        suburb = cd.name+"	"+cd.code
        order_data = Order.objects.filter(order_address=suburb).filter(order_type="Home Delivery").filter(status=0)
        for rr in order_data:
            if rr.order_status == "In process":
                order_details.append({"mobile":rr.user_date.mobile,"name":rr.user_date.name,'order_id':rr.order_id,"id":rr.id,"items":rr.items,"order_status":rr.order_status,"order_type":rr.order_type,"order_address":rr.order_address,"total_amt":rr.total_amt,"items":rr.meals_date.item,"fix_items":rr.meals_date.fixed_item})
            if rr.order_status == "Completed":
                order_details_completed.append({"mobile":rr.user_date.mobile,"name":rr.user_date.name,'order_id':rr.order_id,"id":rr.id,"items":rr.items,"order_status":rr.order_status,"order_type":rr.order_type,"order_address":rr.order_address,"total_amt":rr.total_amt,"items":rr.meals_date.item,"fix_items":rr.meals_date.fixed_item})

    return render(request, 'toh-admin/order-details-1.html',{"order_details":order_details,"order_details_completed":order_details_completed})

@csrf_exempt
def admin_ajax_order(request):
    cart = request.POST['cart']
    order_type = request.POST['order_type']
    email = request.POST['user_id']
    cartTotal = request.POST['cartTotal']
    cart_list = cart.split("^^")
    cart1_list = []
    order_data = Order.objects.all()
    order_len = len(order_data)
    if order_len == 0:
        ord_id = 1
    else:
        ord_id = order_len + 1
    for cc in cart_list:
        if cc != "":
            cc_data = cc.split("--")
            cart1_list.append({"name":cc_data[0].split(".")[1],"price":cc_data[1],"description":cc_data[2],"id":cc_data[0].split(".")[0]})

    order_id = "T" + str(ord_id).zfill(7)
    order_date = date_1
    order_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    order_status = "In process"
    order_type_1 = order_type
    payment_status = "Not Paid"
    user_date = User_data.objects.filter(email=email).last()
    address = Address.objects.filter(user=user_date.id).filter(address_active="active").last()
    if address:
        order_address = address.address
        order_sub = address.pincode

    else:
        address = Address.objects.filter(user=user_date.id)
        order_address = address.address
        order_sub = address.pincode
    # ravi
    code_data = Code.objects.filter(name=order_sub.split("    ")[0]).filter(code=order_sub.split("    ")[1]).last()
    for cart_data in cart1_list:
        item = cart_data['description']
        meals_id = cart_data['id']
        meals_data = Meals.objects.filter(id=meals_id).last()
        order_data = Order(order_id=order_id, items=item, order_date=order_date, user_date=user_date,
                           order_status=order_status, order_type=order_type_1, combo_type="", bal_combo="",
                           order_address=order_address, total_amt=cartTotal, single_item="",payment_status=payment_status,meals_date=meals_data,order_address_customer_id=code_data.id,order_date_time=order_date_time)
        order_data.save()

    data = {"status":"success"}
    return JsonResponse({'data': data})

@csrf_exempt
def admin_ajax_order_subscription(request):
    today_date = date.today()
    Enddate = today_date + timedelta(days=7)
    next_seven_days = {}
    for nd in range(0,7):
        Enddate = today_date + timedelta(days=nd)
        next_seven_days[nd]=[Enddate.strftime("%Y-%m-%d"),Enddate.strftime("%A")]

    cart = request.POST['cart']
    order_type = request.POST['order_type']
    email = request.POST['user_id']
    cartTotal = request.POST['cartTotal']
    cart_list = cart.split("^^")
    cart1_list = []
    order_data = Order.objects.all()
    order_len = len(order_data)
    if order_len == 0:
        ord_id = 1
    else:
        ord_id = order_len + 1
    for cc in cart_list:
        if cc != "":
            cc_data = cc.split("--")
            cart1_list.append({"name":cc_data[0],"price":cc_data[1],"description":cc_data[2],"id":cc_data[0]})

    order_id = "S" + str(ord_id).zfill(7)
    order_date = date_1
    order_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    order_status = "In process"
    order_type_1 = order_type
    payment_status = "Not Paid"
    user_date = User_data.objects.filter(email=email).last()
    address = Address.objects.filter(user=user_date.id).filter(address_active="active").last()
    if address:
        order_address = address.address
        order_sub = address.pincode

    else:
        address = Address.objects.filter(user=user_date.id)
        order_address = address.address
        order_sub = address.pincode
    # ravi
    code_data = Code.objects.filter(name=order_sub.split("    ")[0]).filter(code=order_sub.split("    ")[1]).last()

    for nx_day in next_seven_days.values():
        if nx_day[1] in ["Sunday","Saturday"]:
            pass
        else:
            order_date = nx_day[0]
            for cart_data in cart1_list:
                item = cart_data['description']
                order_data = Order(order_id=order_id, single_item=item, items=cart_data['name'], order_date=order_date, user_date=user_date,
                                   order_status=order_status, order_type=order_type_1, combo_type="", bal_combo="",
                                   order_address=order_address, total_amt=cartTotal,payment_status=payment_status,order_address_customer_id=code_data.id,order_date_time=order_date_time)
                order_data.save()

    data = {"status":"success"}
    return JsonResponse({'data': data})
def order(request):
    id = request.POST['id']
    if request.method=="POST":
        pass
        # order_id = request.POST['email']
        # items = request.POST['name']
        # order_date = request.POST['password']
        # user_date = request.POST['service']
        # order_status = request.POST['email']
        # order_type = request.POST['name']
        # combo_type = request.POST['password']
        # bal_combo = request.POST['service']
        # order_address = request.POST['email']
        # total_amt = request.POST['name']
        # single_item = request.POST['password']
    user_date = User_data.objects.filter(id=2).last()

    order_data = Order(order_id="T000000004", items="Roti", order_date="2023-09-20", user_date=user_date, order_status="In process",order_type="Home Delivery",combo_type="",bal_combo="",order_address="Keysborough	3173",total_amt=19,single_item="")
    order_data.save()
    messages.success(request, 'Driver added successfully...')
    return render(request, 'order-details.html',{})

def admin_customers(request):
    customer_data = User_data.objects.filter(status=0).filter(user_type="Customer")
    context = {"customer_data":customer_data,}
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        user_data = User_data.objects.filter(email=email)
        if user_data:
            messages.error(request, 'This user already register. Please give another email!')
            return render(request, 'toh-admin/customers.html',context)
        else:
            if password == cpassword:
                try:
                    image = request.FILES['imgfile']
                    static_folder = os.path.join(settings.BASE_DIR, 'app\\static')
                    image_name = image.name.split(".")
                    img_name = image_name[0] + dt_string + "." + image_name[1]
                    image_path = os.path.join(static_folder, 'images', img_name)
                    with open(image_path, 'wb') as f:
                        for chunk in image.chunks():
                            f.write(chunk)
                except:
                    img_name=""
                user = User_data(name=name, password=password, email=email,user_type="Customer",mobile=mobile,image=img_name)
                user.save()
                # try:
                #     to = (request.data['email'],)
                #     subject = 'welcome to Teohome'
                #     message = f'Hi, thank you for Registering'
                #     email_from = settings.EMAIL_HOST_USER
                #     recipient_list = to
                #     send_mail(subject, message, email_from, recipient_list)
                # except:
                #     print("email send fail")
                messages.success(request, 'Customer added successfully..')
                return render(request, 'toh-admin/customers.html',context)
            else:
                messages.error(request, 'Password and confirm password was not same')
                return render(request, 'toh-admin/customers.html', context)
    else:
        return render(request, 'toh-admin/customers.html',context)

def admin_customer_dashboard(request):
    if request.method == "POST":
        services = request.POST['services']
        suburb = request.POST['suburb']
        user = request.POST['user']
        user_data = User_data.objects.filter(id=user).last()
        response = HttpResponse("Cookie Set")
        name = user_data.email.split("@")
        response.cookies['email'] = user_data.email
        response.cookies['name'] = name[0]
        response = render(request, 'menu.html', {"get_email": name[0]})
        response.set_cookie('last_connection', datetime.now())
        response.set_cookie('get_email', user_data.email)
        response.set_cookie('name', name[0])
        response.set_cookie('type', 'admintocustomer')
        return response

def admin_customers_profile(request,id):
    user_data = User_data.objects.filter(id=id).last()
    address_data = Address.objects.filter(user_id=user_data.id)
    order_data = Order.objects.filter(user_date=user_data.id).order_by('-id').filter(status=0)
    bal_data = Balance.objects.filter(user_data=user_data.id).filter(status=0)
    note_data = Note.objects.filter(user_data=user_data.id).filter(status=0)
    order_pd_data = Order.objects.filter(user_date=user_data.id).filter(payment_status="Not Paid").filter(status=0)
    un_paid_amt = 0
    for np in order_pd_data:
        un_paid_amt += float(np.total_amt)
    context = {"user_data":user_data,"address_data":address_data,"order_data":order_data,"id":id,"bal_data":bal_data,"note_data":note_data,"order_pd_data":order_pd_data,"un_paid_amt":un_paid_amt}

    return render(request, 'toh-admin/customer-profile.html',context)
def admin_customers_password(request,id):
    context = {"id":id}
    if request.method=='POST':
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            user = User_data.objects.filter(id=id).last()
            user.password=password
            user.save()
            messages.success(request, 'Password update successfully')
            return render(request, 'toh-admin/change-password.html', context)
        else:
            messages.error(request, 'Password and confirm password was not same')
            return render(request, 'toh-admin/change-password.html', context)

    return render(request, 'toh-admin/change-password.html',context)
def admin_customers_orders_details(request,id):
    order_details = Order.objects.filter(id=id).last()
    grand_total = float(order_details.total_amt) + float(order_details.order_delivery_price)
    return render(request, 'toh-admin/customer-order-details.html',{"order_details":order_details,"grand_total":grand_total})

def admin_customers_balance(request,id):
    if request.method == "POST":
        balance = request.POST['balance']
        transition_type = request.POST['transition']
        note = request.POST['note']

        user_data = User_data.objects.filter(id=id).last()

        bal = Balance(user_data=user_data, date=date_1, amount=balance, note=note, transition_type=transition_type)
        bal.save()

        return redirect('app:admin_customers_profile', id)

def admin_customers_note(request,id):
    if request.method == "POST":
        note = request.POST['note']
        user_data = User_data.objects.filter(id=id).last()
        note = Note(user_data=user_data, note=note)
        note.save()
        return redirect('app:admin_customers_profile', id)


def admin_users(request):
    user_data=Admin_user.objects.filter(status=0)
    return render(request, 'toh-admin/users.html',{"user_data":user_data})
def admin_add_users(request):
    if request.method=="POST":
        user_data = Admin_user.objects.filter(email=request.POST['email']).last()
        if user_data:
            messages.success(request, 'This user already register. Please give another email!')
        else:
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            mobile = request.POST['mobile']
            role = request.POST['role']
            try:
                image = request.FILES['imgfile']
                static_folder = os.path.join(settings.BASE_DIR, 'app\\static')
                image_name = image.name.split(".")
                img_name = image_name[0] + dt_string + "." + image_name[1]
                image_path = os.path.join(static_folder, 'images', img_name)
                with open(image_path, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
            except:
                img_name = ""
            user = Admin_user(name=name, password=password, email=email, role=role, mobile=mobile, image=img_name)
            user.save()

            # new_user = User.objects.create_user(username=name,password=password,email=email,)
            # # Save the user to the database
            # new_user.save()
            if not User.objects.filter(username=name).exists():
                # Create a new superuser
                superuser = User.objects.create_superuser(
                    username=name,
                    email=email,
                    password=password
                )

                # You can also set additional attributes for the superuser if needed
                # superuser.first_name = 'Admin'
                # superuser.last_name = 'User'
                superuser.save()
            messages.success(request, 'user added successfully...')

    return render(request, 'toh-admin/add-user.html',{})

def admin_sizes(request):
    if request.method=="POST":
        name = request.POST['name']
        size = Size.objects.filter(name=name)
        Size_data = Size.objects.filter(status=0)
        context = {"Size_data": Size_data,}
        if size:
            messages.success(request, 'size already added...')
        else:
            size_data = Size(name=name)
            size_data.save()
            messages.success(request, 'size added successfully...')
            Size_data = Size.objects.filter(status=0)
            context = {"Size_data": Size_data, }
        return render(request, 'toh-admin/sizes.html', context)
    else:
        Size_data = Size.objects.filter(status=0)
        context = {"Size_data": Size_data, }
        messages.success(request, '')

    return render(request, 'toh-admin/sizes.html',context)
def admin_sizes_delete(request,id):
    size_data = Size.objects.filter(id=id).last()
    size_data.status = 2
    size_data.save()
    size_dt = Size.objects.filter(status=0)
    context = {"Size_data": size_dt,
               }
    messages.success(request, 'Size deleted successfully.')
    return render(request, 'toh-admin/sizes.html', context)

def admin_variations(request):
    if request.method == "POST":
        name = request.POST['name']
        variations = Variations.objects.filter(name=name)
        variations_data = Variations.objects.filter(status=0)
        context = {"Variations_data": variations_data, }
        if variations:
            messages.success(request, 'Variations already added...')
        else:
            variations_data = Variations(name=name)
            variations_data.save()
            messages.success(request, 'Variations added successfully...')
            Variations_data = Variations.objects.filter(status=0)
            context = {"Variations_data": Variations_data, }
        return render(request, 'toh-admin/variations.html', context)
    else:
        Variations_data = Variations.objects.filter(status=0)
        context = {"Variations_data": Variations_data, }
        messages.success(request, '')
    return render(request, 'toh-admin/variations.html',context)
@csrf_exempt
def admin_ajax_variations_edit(request):
    id = request.POST['id']
    variation_data = Variations.objects.filter(id=id).last()
    data = {"name": variation_data.name,"id":id}
    return JsonResponse({'data': data})

@csrf_exempt
def admin_ajax_balance_edit(request):
    id = request.POST['id']
    bal_data = Balance.objects.filter(id=id).last()
    data = {"amount": bal_data.amount,"note": bal_data.note,"transition_type":bal_data.transition_type,"id":id}
    return JsonResponse({'data': data})
@csrf_exempt
def admin_ajax_note_edit(request):
    id = request.POST['id']
    note_data = Note.objects.filter(id=id).last()
    data = {"note": note_data.note,"id":id}
    return JsonResponse({'data': data})

@csrf_exempt
def admin_orders_ajax_order_make_paid(request):
    id = request.POST['id']
    order_data = Order.objects.filter(id=id).last()
    order_data.payment_status = "Completed"
    order_data.save()
    data = {"order_id": order_data.order_id,"id":id}
    return JsonResponse({'data': data})

def admin_variations_edit(request):
    if request.method == "POST":
        id = request.POST['vari_id']
        variation_data = Variations.objects.filter(id=id).last()
        variations = Variations.objects.filter(name=request.POST['aj_name'])

        if variations:
            messages.success(request, 'Variations already added...')
        else:
            variation_data.name = request.POST['aj_name']
            variation_data.save()
            messages.success(request, 'Variations Updated successfully.')

        Variations_data = Variations.objects.filter(status=0)
        context = {"Variations_data": Variations_data, }
        return render(request, 'toh-admin/variations.html', context)
    else:
        Variations_data = Variations.objects.filter(status=0)
        context = {"Variations_data": Variations_data, }
        return render(request, 'toh-admin/variations.html', context)
def admin_variations_delete(request,id):
    variations_data = Variations.objects.filter(id=id).last()
    variations_data.status = 2
    variations_data.save()
    variations_dt = Variations.objects.filter(status=0)
    context = {"Variations_data": variations_dt,
               }
    messages.success(request, 'Variations deleted successfully.')
    return render(request, 'toh-admin/variations.html', context)

def admin_subscription(request):
    return render(request, 'toh-admin/subscription.html',{})


def admin_subscription_plans(request):
    return render(request, 'toh-admin/subscription-plans.html',{})


def admin_catering_menu(request):
    if request.method == "POST":
        image = request.FILES['image']
        image_name = image.name.split(".")
        catering_img_name = image_name[0] + dt_string + "." + image_name[1]
        static_folder = os.path.join(settings.BASE_DIR, 'app\\static')
        image_path = os.path.join(static_folder, 'images', catering_img_name)
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        catering_data = Catering_menu(image=catering_img_name)
        catering_data.save()

        return redirect("app:admin_index")

def admin_promocode(request):
    if request.method == "POST":
        name = request.POST['promo_code']
        enddate = request.POST['enddate']
        endtime = request.POST['endtime']
        min_amount = request.POST['min_amount']
        discount = request.POST['discount']
        amount = request.POST['amount']
        customer = request.POST['customer']
        promocode = Promocodes.objects.filter(promo_code=name).last()
        user = User_data.objects.filter(id=customer).last()
        if promocode:
            messages.success(request, 'Promo code already added...')
        else:
            promocode_data = Promocodes(promo_code=name, end_date=enddate, end_time=endtime,
                                                  min_amt=min_amount, discount=discount, customer=user,
                                                  amount=amount)
            promocode_data.save()
            messages.success(request, 'Promo code added successfully...')
        promocode_data = Promocodes.objects.filter(Q(status=0) | Q(status=1))
        user_data = User_data.objects.filter(status=0)
        context = {"promocode_data": promocode_data,"user_data":user_data }
    else:
        promocode_data = Promocodes.objects.filter(Q(status=0) | Q(status=1))
        user_data = User_data.objects.filter(status=0)
        context = {"promocode_data": promocode_data,"user_data":user_data, }
    return render(request, 'toh-admin/promocode.html',context)

@csrf_exempt
def admin_ajax_promocode_edit(request):

    id = request.POST['id']
    promo_data = Promocodes.objects.filter(id=id).last()
    user_data = User_data.objects.filter(status=0)
    user_dt = []
    for i in user_data:
        user_dt.append({"name":i.name,"id":i.id})

    data = {"user_data":user_dt,"promo_code":promo_data.promo_code,"end_date":promo_data.end_date,"end_time":promo_data.end_time,"min_amt":promo_data.min_amt,"discount":promo_data.discount,"amount":promo_data.amount,"customer":promo_data.customer.id,"id":id}

    return JsonResponse({'data': data})

def admin_promocode_edit(request):
    if request.method == "POST":
        name = request.POST['aj_promocode']
        enddate = request.POST['aj_enddate']
        endtime = request.POST['aj_endtime']
        min_amount = request.POST['aj_minamt']
        discount = request.POST['aj_discount']
        amount = request.POST['aj_amt']
        customer = request.POST['aj_customer']
        id = request.POST['promo_id']
        promocode = Promocodes.objects.filter(promo_code=name).last()
        user = User_data.objects.filter(id=customer).last()
        promocode_data=Promocodes.objects.filter(id=id).last()
        if promocode:
            messages.success(request, 'Promo code already added...')
        else:
            promocode_data.promo_code = name
            promocode_data.end_date = enddate
            promocode_data.end_time = endtime
            promocode_data.min_amt = min_amount
            promocode_data.discount = discount
            promocode_data.amount = amount
            promocode_data.customer = user
            promocode_data.save()
            messages.success(request, 'Promo code Update successfully...')
        promocode_data = Promocodes.objects.filter(Q(status=0) | Q(status=1))
        user_data = User_data.objects.filter(status=0)
        context = {"promocode_data": promocode_data,"user_data":user_data }
    else:
        promocode_data = Promocodes.objects.filter(Q(status=0) | Q(status=1))
        user_data = User_data.objects.filter(status=0)
        context = {"promocode_data": promocode_data,"user_data":user_data, }
    return render(request, 'toh-admin/promocode.html',context)
def admin_promocode_completed(request,id):
    promocode_data = Promocodes.objects.filter(id=id).last()
    promocode_data.status = 1
    promocode_data.save()
    promocode_dt = Promocodes.objects.filter(Q(status=0) | Q(status=1))
    user_data = User_data.objects.filter(status=0)
    context = {"promocode_data": promocode_dt,"user_data":user_data }
    messages.success(request, 'Promo code deleted successfully.')
    return render(request, 'toh-admin/promocode.html', context)
def admin_promocode_delete(request,id):
    promocode_data = Promocodes.objects.filter(id=id).last()
    promocode_data.status = 2
    promocode_data.save()
    promocode_dt = Promocodes.objects.filter(Q(status=0) | Q(status=1))
    user_data = User_data.objects.filter(status=0)
    context = {"promocode_data": promocode_dt,"user_data":user_data }
    messages.success(request, 'Promo code deleted successfully.')
    return render(request, 'toh-admin/promocode.html', context)

def admin_salesreport(request):
    return render(request, 'toh-admin/index.html',{})
def admin_orderreport(request):
    return render(request, 'toh-admin/index.html',{})
def admin_itemreport(request):
    return render(request, 'toh-admin/index.html',{})
def admin_suburreport(request):
    return render(request, 'toh-admin/index.html',{})

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_data = Admin_user.objects.filter(email=email).filter(password=password).filter(status=0).last()
        username = user_data.name
        user = authenticate(username=username, password=password)
        if user:
            return redirect('/admin-index/')

        else:
            messages.error(request, 'Please Check Your User Name and Password !')
            return render(request, 'toh-admin/login.html')
    else:
        messages.error(request, '')
        return render(request, 'toh-admin/login.html',{})
    return render(request, 'toh-admin/login.html',{})
def admin_user_subscription_details(request):
    return render(request, 'toh-admin/user-subscription-details.html',{})

def admin_timing(request):
    if request.method == "POST":
        mon = request.POST['day']
        mon_open_time = request.POST['mon_open_time']
        mon_close_time = request.POST['mon_close_time']
        delivery = request.POST['delivery']

        timing_data = Timings(day=mon,open_time=mon_open_time,close_time=mon_close_time,delivery=delivery)
        timing_data.save()

        # try:
        #     tues = request.POST['tues']
        #     tues_open_time = request.POST['tues_open_time']
        #     tues_close_time = request.POST['tues_close_time']
        # except:
        #     pass
        #
        # wed = request.POST['wed']
        # wed_open_time = request.POST['wed_open_time']
        # wed_close_time = request.POST['wed_close_time']
        #
        # thu = request.POST['thu']
        # thu_open_time = request.POST['thu_open_time']
        # thu_close_time = request.POST['thu_close_time']
        #
        # fri = request.POST['fri']
        # fri_open_time = request.POST['fri_open_time']
        # fri_close_time = request.POST['fri_close_time']
        #
        # sat = request.POST['sat']
        # sat_open_time = request.POST['sat_open_time']
        # sat_close_time = request.POST['sat_close_time']
        #
        # sun = request.POST['sun']
        # sun_open_time = request.POST['sun_open_time']
        # sun_close_time = request.POST['sun_close_time']


    return render(request, 'toh-admin/timing.html',{})
def admin_closedate(request):
    return render(request, 'toh-admin/index.html',{})
def admin_sign_out(request):
    logout(request)
    response = render(request, 'toh-admin/login.html', {})
    return response


