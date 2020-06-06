from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import p,order,orderItem

from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.



def store(request):
    product=p.objects.all()
    if request.user.is_authenticated:
        orders,created=order.objects.get_or_create(customer=request.user,complete=False)
        context={'product':product,'order':orders}
        return render(request,'shop/store.html',context)
    else:
        context={'product':product}
        return render(request,'shop/store.html',context)
    

@login_required(login_url='login/')
def cart(request):
    customer=request.user
    orders,created=order.objects.get_or_create(customer=customer,complete=False)
    items=orders.orderitem_set.all()
    context={'items':items,'order':orders}
    return render(request,'cart.html',context)

def checkout(request):
    customer=request.user
    orders,created=order.objects.get_or_create(customer=customer,complete=False)
    items=orders.orderitem_set.all()
    context={'items':items,'order':orders}
    return render(request,'checkout.html',context)

def about(request):
     return render(request,'sbout.html')

def contact(request):
    return render(request,'contactus.html')

class view(DetailView):
    #pro = p.objects.filter(P_id=id)
    #product={'p':pro[0]}
    #print(product)
    #return render(request,'shop/productview.html',product)
    model=p
    template_name='productview.html'


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        passs=request.POST['pass']
        user=auth.authenticate(username=username,password=passs)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"incorrect credentials")
            print('user not exsists')
            return redirect('login')
    else:
        return render(request,'login.html')


def signup(request):
    if request.method=='POST':
        firstname=request.POST['fname']
        lastname=request.POST['lname']
        username=request.POST['uname']
        email=request.POST['email']
        password=request.POST['pass']
        cpass=request.POST['conf_pass']
        print(password,cpass)
        if password==cpass:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username is in use")
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request,"email already exists")
                    print("email is in use")
                    return redirect('signup')
                else:
                    user=User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
                    user.save()
                    print("save")
                    return redirect('login')
        else:
            messages.info(request,"password Password not match")
            return redirect('signup')
    else:
        return render(request,'signup.html')



def logout(request):
    auth.logout(request)
    return redirect('/')

class profile(DetailView):
    model=User
    template_name='profile.html'


def update_cart(request,P_id):
    pro=p.objects.get(P_id=P_id)
    orders,created=order.objects.get_or_create(customer=request.user,complete=False)

    if orderItem.objects.filter(order=orders,product=pro).exists():
        print("exsists")
        orderItem.Update_quan.__get__(orderItem.objects.get(order=orders,product=pro))
    else:
        item,created=orderItem.objects.get_or_create(order=orders,product=pro,quantity=1)
        item.save()
    return redirect("/")


def update_cart_product(request,id):
    #this def is use to update cart from product view page
  
    pro=p.objects.get(P_id=id)
    orders,created=order.objects.get_or_create(customer=request.user,complete=False)

    if orderItem.objects.filter(order=orders,product=pro).exists():
        orderItem.Update_quan.__get__(orderItem.objects.get(order=orders,product=pro))
    else:
        item,created=orderItem.objects.get_or_create(order=orders,product=pro,quantity=1)
        item.save()
    return redirect("p_view",id)


def remove_product(request,id):
    #this def is use to update cart from product view page
    pro=p.objects.get(P_id=id)
    orders,created=order.objects.get_or_create(customer=request.user,complete=False)

    if orderItem.objects.filter(order=orders,product=pro).exists():
        print("exsists")
        orderItem.remove(orderItem.objects.get(order=orders,product=pro))
    return redirect("/")


def inc_quan(request,id):
    pro=p.objects.get(P_id=id)
    orders,created=order.objects.get_or_create(customer=request.user,complete=False)
    if orderItem.objects.filter(order=orders,product=pro).exists():
        orderItem.Update_quan.__get__(orderItem.objects.get(order=orders,product=pro))
    return redirect('cart')

def rem_quan(request,id):
    pro=p.objects.get(P_id=id)
    orders,created=order.objects.get_or_create(customer=request.user,complete=False)
    if orderItem.objects.filter(order=orders,product=pro).exists():
        orderItem.des_quan.__get__(orderItem.objects.get(order=orders,product=pro))
    return redirect('cart')