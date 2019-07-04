from django.urls import path
from django.urls import reverse_lazy

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView as auth_views

from django.views.generic import TemplateView
#from django.urls import reverse_lazy

from . import views


urlpatterns = [
    path('home',views.home, name='home'),
    path('', views.HotelList.as_view(), name='hotel_list'),
    path('new', views.HotelCreate.as_view(), name='hotel_new'),
    path('view/<int:pk>', views.HotelView.as_view(), name='hotel_view'),
    #path('views/<int:pk>', views.HotelView.as_view(), name='hotel_view'),
    path('edit/<int:pk>', views.HotelUpdate.as_view(), name='hotel_edit'),
    path('delete/<int:pk>', views.HotelDelete.as_view(), name='hotel_delete'),
    path('signup', views.CustomerSignUpView.as_view(), name='signup'),
    path('adminsignup', views.AdminSignUpView.as_view(), name='signup'),
    path('adminarea', views.adminmethod, name='admin_area'),
    path('customerarea', views.customermethod, name='customer_area'),

    path('hotelbook/<int:pk>', views.HotelBook.as_view(), name='hotel_book'),
    #path('pp/<int:pk>', views.HotelBook.as_view(), name='hotel_book'),
    path('cust_list', views.CustList.as_view(), name='customer_list'),#this gives list of hotel to customers
    path('room_book/<int:id>', views.roombook, name='roombook'), #once you select hotel from CustList it redirects                          
                                                                 # here for booking process
    
    path('pricing/<int:id>', views.pricing, name='pricing'),
    path('logout', views.logout, name='logout'), #workig  logout
    path('login', auth_views.as_view(template_name="cr_app/login.html"), name='login'),
    
    #path('login', views.login_user, name='login'),
    #path('myview', views.my_view, name='myview'),
]