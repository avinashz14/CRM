from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import *
from  .filters import orderFilter
from .form import CustomerForm, OrderForm, CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only
# Create your views here.

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form  = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user,) 
            print("successfully")
            username = form.cleaned_data['username']
            print(username)
            form = CreateUserForm()
            messages.success(request, 'Successfully account was create for ' + username)
            return redirect('login')
            
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.warning(request, 'Invalid Login Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    messages.info(request, 'Your are logout!')
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    return redirect('dashboard')

@login_required(login_url='login')
@admin_only
def dashboard(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    orders=  orders.order_by('-id')[:5]
    context ={
        'products' : products,
        'customers' : customers,
        'orders' : orders,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','stuff'])
def products(request):
    products = Product.objects.all()
    print(products)
    context ={
        'products':products,
    }
    return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request, id):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()
    
    context ={
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,

    }
    return  render(request, 'accounts/user_page.html', context) 


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','stuff'])
def customer(request, id):

    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    total_order = orders.count()    
    print(customer)

    order_filter = orderFilter(request.GET, queryset=orders)
    orders = order_filter.qs

    context ={
        'customer' : customer,
        'orders' : orders,
        'total_order':total_order,
        'order_filter':order_filter,
    }
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','stuff'])
def createCustomer(request):

    form = CustomerForm()
    if request.method=='POST':
        form = CustomerForm(request.POST);
        if form.is_valid():
            form.save()
            print(form.as_p)
            return redirect('dashboard')

    context = {
        'form':form,
    }
    return render(request, 'accounts/create_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','stuff'])
def updateCustomer(request, id):
    
    customer = Customer.objects.get(id=id)
    form = CustomerForm(instance=customer)
    print(customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer', id=id)
    context = {
        'form':form,
    }
    return render(request, 'accounts/create_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','stuff'])
def createOrder(request, id):
    customer = Customer.objects.get(id=id)
    print(customer)
    form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        form  = OrderForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('dashboard')

    context = {
        'form':form,
    }
    return render(request, 'accounts/create_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','stuff'])
def updateOrder(request, id):

    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    print(order)
    if request.method == 'POST':
        form  = OrderForm(request.POST,instance=order)
        if(form.is_valid()):
            form.save()
            return redirect('dashboard')

    context = {
        'form':form,
    }
    return render(request, 'accounts/create_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','stuff'])
def deleteOrder(request, id):

    order = Order.objects.get(id=id)
    print(order)

    if request.method=='POST':
        order.delete()
        return redirect('dashboard')

    context = {
        'order':order,
    }
    return render(request, 'accounts/delete_order.html', context)
