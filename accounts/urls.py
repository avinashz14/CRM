from django.http.response import HttpResponse
from django.urls import path

#from django.urls.resolvers import URLPattern 
from . import views 


urlpatterns =[
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customers/', views.customers, name='customers'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
