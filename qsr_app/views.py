from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import product, Cart, Order, custadd, User
from django.db.models import Q
from django.http import JsonResponse
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
def home(request):
    #userid=request.user.id
    #print('id of logged in user:',userid)
    #print('result:', request.user.is_authenticated)
    p=product.objects.filter(is_active=True)
    c=Cart.objects.filter(uid=request.user.id)
    np=len(c)
    print(p)
    context={}
    context['products']=p
    context['quantity']=np
    return render(request,'home.html',context)


def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=='' or upass=='' or ucpass=='':
            context['errmsg']='fields can not be Empty'
            return render(request,'register.html',context)
        elif upass != ucpass:
            context['errmsg']="Passwords didn't match"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname,)
                u.set_password(upass)
                u.save()
                context['success']='User created successfully. Please login'
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']='User with same Username already exist !'
                return render(request,'register.html',context)
                
    else:
        return render(request,'register.html')

def user_login(request):
    if request.method=='POST':
        un=request.POST['uname']
        up=request.POST['upass']
        context={}
        context['user']=un
        #print(up,'--',un)
        #return HttpResponse('data fetched')
        context={}
        if un==''or up=='':
            context['errmsg']='fields can not be empty'
            return render(request,'login.html',context)
        else:
            u=authenticate(username=un,password=up)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errmsg']='Invalid Username & Password'
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')
    
def lg(request):
    logout(request)
    return redirect('/home')

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        #print(pid)
        #print(userid)
        u=User.objects.filter(id=userid)
        #print(u[0])
        p=product.objects.filter(id=pid)
        #print(p[0])
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2) #return query set-[]
        n=len(c)
        context={}
        context['products']=p
        context['quantity']=n
        if n==1:
            context['msg']='Product Already Exist in Cart!!'
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']='Product Added Successfully'
        return render(request,'home.html',context)
        # return HttpResponse('product added to cart')
    else:
        return redirect('/login')
    
def cart(request):
    c=Cart.objects.filter(uid=request.user.id)
    #print(c) # two objects
    #(c[0].uid) # this is user object - id of c-0 /index no. 0
    #(c[0].pid.name) # this is productobjects
    #print(c[0].pid.price)
    s=0
    np=len(c)
    #print(np)
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price*x.qty
    context={}
    context['data']=c
    context['total']=s
    context['n']=np
    return render(request,'cart.html',context)
    



def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty + 1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty - 1
            c.update(qty=t)
    #return HttpResponse('quantity')
    return redirect('/cart')

def orderpg(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    #print(oid)
    for x in c:
        o=Order.objects.create(ord_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    context={}
    context['data']=orders
    s=0
    np=len(orders)
    for x in orders:
        s=s+x.pid.price*x.qty
    context['total']=s
    context['n']=np
    return render(request,'orderpage.html',context)   

def delivery(request):
    
    return render(request,'delivery.html')

def address(request):
    if request.method=='POST':
        n=request.POST['name']
        email=request.POST['email']
        mobile1=request.POST['mob']
        adds1=request.POST['add1']
        adds2=request.POST['add2']
        pin=request.POST['zip']
        
        if n =='' or email =='' or mobile1 =='':
            context={}
            context['errmsg']='fields can not be Empty'
            return render(request,'delivery.html',context)
        else:
            c=custadd.objects.create(name=n,mobile=mobile1,add1=adds1,add2=adds2,zip=pin)
            c.save()
            return redirect('/payment',context)
    else:
        return render(request,'delivery.html')
    
def payment(request):
    uemail=request.user.username
    print(uemail)
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    
    np=len(orders)
    for x in orders:
        s=s + x.pid.price*x.qty
        oid=x.ord_id

    client = razorpay.Client(auth=("rzp_test_vHkTcKqaLhdcim", "G8QU0ji9TdPNlMtopg1ZhH6b"))
    data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    #print(payment)
    #return HttpResponse('success')
    context={}
    context['data']=payment
    context['uemail']=uemail
    return render(request,'payment.html',context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')

def removep(request,cid):
    c=Order.objects.filter(id=cid)
    c.delete()
    return redirect('/orderpg')


def sndmail(request,uemail):
    print('-----------',uemail)
    msg="order details"
    send_mail(
        'Sweet store -order placed successfully',
        msg,
        'c.shan8@gmail.com',
        [uemail],
        fail_silently=False,
)
    return render(request,"shopparcel.html")

def shopparcel(request):
    l=Order.objects.filter(uid=request.user.id)
    for x in l:
        oid=x.ord_id
    context={}
    context['orderid']=oid
    return render(request,'shopparcel.html',context)

    
def wait(request):
    l=Order.objects.filter(uid=request.user.id)
    for x in l:
        oid=x.ord_id
    context={}
    context['orderid']=oid
    return render(request,'wait.html',context)



def Cashp(request):
    return render(request,'shopparcel.html')

def Cashd(request):
    return render(request,'wait.html')

def Cashe(request):
    l=Order.objects.filter(uid=request.user.id)
    for x in l:
        oid=x.ord_id
    context={}
    context['orderid']=oid
    return render(request,'storedine.html',context)

def contact(request):
    return render(request,'contactus.html')

def aboutus(request):
    return render(request,'aboutus.html')

def reports(request):
    c=Cart.objects.filter(uid=request.user.id)
    #print(c) # two objects
    #(c[0].uid) # this is user object - id of c-0 /index no. 0
    #(c[0].pid.name) # this is productobjects
    #print(c[0].pid.price)
    s=0
    np=len(c)
    #print(np)
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price*x.qty
    order=Order.objects.filter(uid=request.user.id)
    context={}
    context['data']=c
    context['total']=s
    context['n']=np
    context['ord']=order
    return render(request,'reports.html',context)

