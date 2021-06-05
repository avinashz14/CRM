from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from  .filters import orderFilter


from .form import CustomerForm, OrderForm
# Create your views here.

def home(request):
    return render(request, 'accounts/home.html')


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


def products(request):
    products = Product.objects.all()
    print(products)
    context ={
        'products':products,
    }
    return render(request, 'accounts/products.html', context)


def customer(request, id):

    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    total_order = orders.count()    
    print(customer)

    order_filter = orderFilter()

    context ={
        'customer' : customer,
        'orders' : orders,
        'total_order':total_order,
        'order_filter':order_filter,
    }
    return render(request, 'accounts/customer.html', context)



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
