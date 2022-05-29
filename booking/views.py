from audioop import reverse
from calendar import c
from datetime import datetime
import imp
from locale import currency
from re import X, template
from django.shortcuts import render
from matplotlib import container
from matplotlib.style import use
from requests import request
from django.urls import reverse_lazy
from urllib3 import HTTPResponse
from .models import Offers, Passenger, UserDetails, Places, Flightroutes, Flights, Ticket, Passenger
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.views.decorators.csrf import csrf_protect
import random
import string
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.shortcuts import redirect
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.

client = razorpay.Client(auth=('rzp_test_WEXoLQRsQcTbCC', 'OS28p1yu4AWw7O8OydDfMm0y'))
def index(request):
    offersData = Offers.objects.all()
    placesData = Places.objects.all()
    today = date.today()
    tDate = today.strftime("%Y-%m-%d") 
    tDate = str(tDate)
    print("--------------->",tDate)
    data = {
        'offersdata': offersData,
        'placesdata': placesData,
        'mindate':tDate+""
    }
    #sendEmail("subject","message","lakshaykumar2193@gmail.com")
    print("--------------->",data['mindate'])

    return render(request=request, template_name="booking/index.html", context=data)

user=""

def addflights(request):
    routes = Flightroutes.objects.values()
    data={}
    data['routes'] = routes
    print(routes)
    if(request.method == "POST"):
        fno = request.POST.get('flightno')
        route = request.POST.get('route')
        dtime = request.POST.get('dtime')
        atime = request.POST.get('atime')
        basefare = request.POST.get('basefare')
        try:
            routeAdded = Flightroutes.objects.only('routeno').get(routeno=route)
            flightdets = Flights(flightno=fno,routeno=routeAdded,departure=dtime,arrival=atime,basefare=basefare)
            flightdets.save()
            data['alert'] = '<div class="alert alert-success" ><strong>Wowww!</strong><br> Data Added</button></div>'
        except Exception as e:
            data['alert'] = '<div class="alert alert-danger"><strong>Nope!</strong><br> Some error occured - '+ str(e) +'</button></div>'



    return render(request=request,template_name="booking/addflights.html",context=data)

def login(request):
    username = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    data = {
        'alert': '<div class="alert alert-danger alert-dismissible fade show" role="alert"><strong>Oops!</strong><br> Check Username and Password again</button></div>'

    }
    if user is not None:
        auth_login(request, user)
        print("USERRRRR EXISTS")
        request.session['username'] = str(username)
        print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",user)
        print("------------------------>", request.session['username'])
        return render(request=request, template_name="booking/index.html")
    else:
        print("NOT EXISTANT - ", username, " -- ", password)

    return render(request=request, template_name="booking/signin.html", context=data)


def registeruser(request):
    if(request.method == "POST"):
        name = request.POST.get('name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        messageshown = ""
        data = {
            'alert': '<div class="alert alert-success alert-dismissible fade show" role="alert"><strong>Woohoo!</strong><br> You are registered</button></div>'

        }
        if(pass1 == pass2 and len(pass1) > 8):
            messageshown = "Make sure your password matches and have length greator than 8 characters"

            try:
                usd = UserDetails(name=name, emailid=email, dob=dob,
                                  contactno=phone, password=pass1, verified="no")
                usd.save()
                cusd = User.objects.create_user(email, email, pass1)
                cusd.first_name = name.split()[0]
                cusd.last_name = name.split()[1]
                cusd.save()
                user = authenticate(username=email, password=pass1)
                auth_login(request, user)
                request.session['username'] = str(email)
                print("USERRRRR EXISTS")
                message = "Hello "+name+"\n Yoy have successfully registered on F5 Airlines. Please verify yourself from the link given. \nLink - http://localhost:8000/verifyuser?email="+email+". \n Thankyou\nTeam\nF5 Airlines"
                subject = "Verification Email | F5 Airlines"
                #sendEmail(subject,message,str(email))
                return render(request=request, template_name="booking/index.html")

            except Exception as e:
                print("&*"*15,e)
                data['alert'] = '<div class="alert alert-danger alert-dismissible fade show" role="alert"><strong>Oops!</strong><br>Someone already registered with this email ID and Contact No</button></div>'
        else:
            data['alert'] = '<div class="alert alert-warning alert-dismissible fade show" role="alert"><strong>Oops!</strong><br>' + \
                'Make sure your password matches and have more than 8 characters' + '</button></div>'

    return render(request=request, template_name="booking/register.html", context=data)


def userprofile(request):
    data={}
    username = request.session['username']
    userdet = UserDetails.objects.filter(emailid=username).values()[0]
    print("^"*20)
    print(userdet)
    print("^"*20)
    data['name'] = userdet['name']
    data['contactno'] = userdet['contactno']
    data['dob'] = userdet['dob'].strftime("%Y-%m-%d")
    data['emailid'] = userdet['emailid']
    data['password'] = userdet['password']
    if(request.method == "POST"):
        print("POST CLICKED")
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        contact = request.POST.get('phone')
        dob = request.POST.get('dob')
        
        
        usr = UserDetails.objects.get(emailid=username)
        usr.name = name
        usr.emailid = email
        usr.contactno = contact
        usr.dob = dob
        
        usr.save()
        data['alert'] = '<div class="alert alert-success" role="alert">Data is updated</div>'

            

    return render(request=request, template_name="booking/userprofile.html",context=data)


def signin(request):
    return render(request=request, template_name="booking/signin.html")


def logout(request):
    django_logout(request)
    return render(request=request, template_name="booking/index.html")


def signup(request):
    return render(request=request, template_name="booking/register.html")



def flightdetails(request):
    origin = request.GET['origin']
    destination = request.GET['destination']
    depart = request.GET['depart']
    passen = request.GET['passen']
    origin = origin[0:3]
    destination = destination[0:3]
    year = int(depart.split("-")[0])
    month = int(depart.split("-")[1])
    day = int(depart.split("-")[2])
    try:
        route = Flightroutes.objects.filter(origin=origin).filter(
            destination=destination).values()
        print("----------->", route)

        availableflights = Flights.objects.filter(
            routeno=route[0]['routeno']).values()
        print("----------->", availableflights)

    except Exception as e:
        print("Error - ", e)
        availableflights = {}
    


    data = {
        'from': origin,
        'destination': destination,
        'availableflights': availableflights,
        'date': str(day)+"-"+str(month)+"-"+str(year),
        'passen': passen
    }

    if(request.method == "POST"):
        minprice = int(request.POST.get('minprice'))
        maxprice = int(request.POST.get('maxprice'))
        sortby = request.POST.get('sortby')
        sortby = '-'+str(sortby)
        shownflights = availableflights
        shownflights = shownflights.order_by(sortby)
        filteredflights = []
        for i in shownflights:
            if(i['basefare']>=minprice and i['basefare']<=maxprice):
                filteredflights.append(i)
        
        data['availableflights'] = filteredflights
        
        
        
        
        

    return render(request=request, template_name="booking/flightdetails.html", context=data)


def passengerdetails(request):
    flightid = request.GET['flightdet']
    date = request.GET['date']
    passen = request.GET['passen']
    itenery = Flights.objects.filter(flightno=flightid).values()
    route = Flightroutes.objects.filter(
        routeno=itenery[0]['routeno_id']).values()[0]
    amount = int(itenery[0]['basefare'])*int(passen)
    amount = amount+(349*int(passen))+(0.05*amount)+(0.082*amount)+300
    noOfPassengers = passen
    passen = [x for x in range(int(passen))]
    couponcode = ""
    data = {}
    couponCodes = Offers.objects.values()
    
    try:
        print("------>", itenery, " ############# ", route)
        data = {
            'itenery': itenery,
            'origin': route['origin_id'],
            'dest': route['destination_id'],
            'date': date,
            'passen': passen,
            'amount': round(amount),
            'cCodes':couponCodes
        }
        print("-----------------------------)", data)
    except:
        print("Some error")


    if 'payment' in request.POST:
        if(request.POST.get('coupon')):

            couponcode = request.POST.get('coupon')
            category = request.POST.get('category')
            if(int(category) == 1):
                amount = amount+(0.5*amount)
            elif(int(category) == 2):
                amount = amount*2

            data['amount'] = round(amount)
            try:
                offersCode = Offers.objects.filter(
                    code=couponcode.upper()).values()[0]
                print("----------->", offersCode)
                maxdis = offersCode['maxdis']
                amount = amount-int(maxdis)
                data['amount'] = round(amount)
                data['coupon'] = "-"+str(round(maxdis))
            except Exception as e:
                print("Error - ", e)
            
            try:
                if(request.session['username']):
                    a = 5
                    userdetails = []
                    email = request.session['username']
                    pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                    print(pnr)
                    data['pnr']=pnr

                    category = request.POST.get('category')
                    couponcode = request.POST.get('coupon')
                    for i in range(len(passen)):
                        passengerName = request.POST.get('name'+str(i))
                        userdetails.append(passengerName)
                        passengerAge = request.POST.get('dob'+str(i))
                        userdetails.append(passengerAge)

                    amount = round(amount)

                    print("--------------------->", userdetails)

                    bookingID = ''.join(random.choices(string.digits, k=10))
                    ticket = Ticket(pnr=pnr, contact=request.session['username'],flightdate=date,flightno=flightid,booking=int(bookingID),paidamt=amount)
                    ticket.save()
                    maxusers = len(userdetails)
                    for i in range(0,maxusers-1,2):
                        name = userdetails[i]
                        dob = userdetails[i+1]
                        pnrfk = Ticket.objects.only('pnr').get(pnr=pnr)
                        passengeradd = Passenger(name=name,dob=dob,pnr=pnrfk,bookingID=bookingID)
                        passengeradd.save()
                    amount = int(amount)
                    data['rzpamt'] = amount*100
                    red_url = "/payment?amount="+str(amount)+"&coupon="+str(couponcode)
                    return redirect(red_url)     
                else:
                    data['alert'] = '<div class="alert alert-danger" role="alert">Please login first!</div>'
            except:
                data['alert'] = '<div class="alert alert-danger" role="alert">Please login first!</div>'
    
        else:
            try:
                if(request.session['username']):
                    a = 5
                    userdetails = []
                    email = request.session['username']
                    pnr = ''.join(random.choices(
                        string.ascii_uppercase + string.digits, k=5))
                    data['pnr']=pnr

                    category = request.POST.get('category')
                    couponcode = request.POST.get('coupon')
                    for i in range(len(passen)):
                        passengerName = request.POST.get('name'+str(i))
                        userdetails.append(passengerName)
                        passengerAge = request.POST.get('dob'+str(i))
                        userdetails.append(passengerAge)

                    amount = round(amount)

                    print("--------------------->", userdetails)
                    bookingID = ''.join(random.choices(string.digits, k=10))
                    ticket = Ticket(pnr=pnr, contact=request.session['username'],flightdate=date,flightno=flightid,booking=int(bookingID),paidamt=amount)
                    ticket.save()
                    maxusers = len(userdetails)
                    for i in range(0,maxusers-1,2):
                        name = userdetails[i]
                        dob = userdetails[i+1]
                        pnrfk = Ticket.objects.only('pnr').get(pnr=pnr)
                        passengeradd = Passenger(name=name,dob=dob,pnr=pnrfk,bookingID=bookingID)
                        passengeradd.save()
                    data['rzpamt'] = amount*100
                    red_url = "/payment?amount="+str(amount)+"&coupon="+str(couponcode)
                    return redirect(red_url)
                    
                else:
                    data['alert'] = '<div class="alert alert-danger" role="alert">Please login first!</div>'
    
            except:
                data['alert'] = '<div class="alert alert-danger" role="alert">Please login first!</div>'
    

    data['pnr']=''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
   
    return render(request=request, template_name="booking/passengerdetails.html", context=data)


def payment(request):
    amount = request.GET['amount']
    coupon = request.GET['coupon']
    amount = int(amount)
    data={}
    orderamount = amount*100
    ordercurrency = "INR"
    paymentOrder = client.order.create(dict(amount=orderamount,currency=ordercurrency,payment_capture=1))
    paymentOrderID = paymentOrder['id']
    data['orderid'] = paymentOrderID
    data['rzpamt'] = orderamount
    data['coupon'] = coupon
    data['amount'] = amount
    return render(request=request,template_name="booking/payment.html", context=data) 


def pnrstatus(request):
    data={}
    if(request.method == "POST"):
       
        pnr = request.POST.get('pnr')
        pnrdata = Ticket.objects.filter(pnr=pnr).order_by('-id').values()[0]
        print(pnrdata)
        data['flightdate'] = pnrdata['flightdate']
        data['flightno'] = pnrdata['flightno']
        data['email'] = pnrdata['contact']
        data['bookingid'] = pnrdata['booking']
        passengers = Passenger.objects.filter(pnr_id=pnrdata['id']).values()
        data['passengers'] = passengers
        print("____"*10,passengers)
    
    return render(request=request, template_name="booking/pnrstatus.html",context=data)


def usertrips(request):
    print("------------------------>",request.session['username'])
    contact = request.session['username']
    data={}
    passengerdata={}
    userpnrs = Ticket.objects.filter(contact=contact).order_by('-id').values()
    passengers = Passenger.objects.values()
    data['userpnrs'] = userpnrs
    
    # for i in userpnrs:
       
    #     id = int(i['id'])
    #     pnr = i['pnr']
    #     print(pnr)
    #     passengers = Passenger.objects.values()
    #     print("^&"*10,passengers)
        
    #     data['passengers'] = passengers
    data['passengers']=passengers
    print("-"*15)
    print(passengers)
    print("-"*15)
            
    
        
        
    


    return render(request=request, template_name="booking/usertrips.html", context=data)


def success(request):
    return render(request=request, template_name="booking/paymentsuccess.html")


def ticket(request):
    pnr = request.GET['pnr']
    data={}
    ticket = Ticket.objects.filter(pnr=pnr).order_by('-id').values()
    data['pnr'] = pnr
    
    
    passengers = Passenger.objects.values()
    data['contact']= ticket[0]['contact']
    data['flightno'] = ticket[0]['flightno']
    data['flightdate'] = ticket[0]['flightdate']
    data['booking'] = ticket[0]['booking']
    route = (Flights.objects.filter(flightno=ticket[0]['flightno']).values())[0]['routeno_id']
    origin = (Flightroutes.objects.filter(routeno=route).values())[0]['origin_id']
    destination = (Flightroutes.objects.filter(routeno=route).values())[0]['destination_id']
    data['origin'] = origin
    data['destination'] = destination
    passengers = Passenger.objects.filter(pnr_id=ticket[0]['id']).values()
    print(ticket)
    data['userpnrs'] = ticket
    print("^"*10)
    print(passengers)
    print("^"*10)
    data['passengers']=passengers
    data['paidamt'] = ticket[0]['paidamt']
    return render(request=request, template_name="booking/ticket.html",context=data)


def verifyuser(request):
    result = "Error while verifying user"
    try:
        email = request.GET['email']
        usr = UserDetails.objects.get(emailid=email)
        usr.verified = "yes"
        usr.save()
        result = "Wooho! User Verified"
    except Exception as e:
        result="Some Error Occured = "+str(e)

    return HttpResponse(result)

def sendEmail(subject,message,receiversemail):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [receiversemail,]
    print(recipient_list)
    send_mail(subject,message,email_from,recipient_list)

def PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeView
    success_url = reverse_lazy('localhost:8000/index')