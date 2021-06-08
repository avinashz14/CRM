from django.http.response import HttpResponse
from django.urls import path

#from django.urls.resolvers import URLPattern 
from . import views 


urlpatterns =[
    path('', views.home, name='home'),
    path('user/<int:id>/', views.userPage, name='user_page'),
    path('user/setting', views.userSettingPage, name='user_setting'),

    path('products/', views.products, name='products'),
    path('customer/<int:id>/', views.customer, name='customer'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    
    
    path('create_customer/', views.createCustomer, name='create_customer'),
    path('update_customer/<int:id>/', views.updateCustomer, name='update_customer'),

    path('create_order/<int:id>/', views.createOrder, name='create_order'),
    path('update_order/<int:id>/', views.updateOrder, name='update_order'),
    path('delete_order/<int:id>/', views.deleteOrder, name='delete_order'),

]
