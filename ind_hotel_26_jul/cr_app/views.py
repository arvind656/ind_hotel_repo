# i was facing a huge problem @login_required was not working, then 
# i changed the code and run the, it showed some error, then again i restored
# it to previous code and this time, without doing anything @login_required was working.
# The basic problem was the custom logout that i wrote was actually not working. 



# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Import Generic View for listing (r operation)
from django.views.generic import ListView, DetailView

# Import Generic View for creating, updating and deleting (cud operations)
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Resolving URLs
from django.urls import reverse_lazy

# Import Book Model
from cr_app.models import Hotel

# Import Book Form
from cr_app.forms import HotelForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
#from django.urls import reverse
from .models import User_t
from cr_app.forms import CustomerSignUpForm
from cr_app.forms import AdminSignUpForm
from cr_app.forms import PriceForm

from django.contrib.auth import login, authenticate 
from .decorators import customer_required

from django.contrib import auth
#from django.contrib.auth import login, authenticate,logout 

from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth import authenticate

#from . models import my_custom_sql
from django.db import connection
from . decorators import admin_required
from django.views.generic import TemplateView


@login_required
@admin_required
def adminmethod(request):
    return render(request, 'cr_app/admin.html')

@login_required
@customer_required
def customermethod(request):
    return render(request, 'cr_app/customer.html')


def logout(request):
    auth.logout(request)
      
    return redirect(home)  
        

@login_required(login_url = '/login')#there we should not give cr_admin/login as cr_admin will be added automatically django
def home(request):
    
    #my_custom_sql()
    return render(request, 'cr_app/home.html')



@method_decorator(login_required,name='dispatch')
class HotelList(ListView):
    #if (row == 'customer'):
    model = Hotel

@method_decorator(login_required,name='dispatch')
class CustList(HotelList):#ListView,TemplateView): #this gives list of hotel to customers
    
    model = Hotel  
    template_name = 'cr_app/cus_hotellist.html'
    #success_url = reverse_lazy('hotel_list')         

@method_decorator(login_required, name='dispatch')
class HotelView(DetailView):
    model = Hotel

@method_decorator([login_required, admin_required], name='dispatch')
class HotelCreate(CreateView):
    model = Hotel
    form_class = HotelForm
    # Setting returning URL
    success_url = reverse_lazy('hotel_list')
    #success_url = reverse_lazy('hotel_new')

@method_decorator([login_required, admin_required], name='dispatch')
class HotelUpdate(UpdateView):
    model = Hotel
    form_class = HotelForm
    # Setting returning URL
    success_url = reverse_lazy('hotel_list')

@method_decorator([login_required, customer_required], name='dispatch')
class HotelBook(UpdateView):
    model = Hotel
    form_class = HotelForm
    # Setting returning URL
    #success_url = reverse_lazy('hotel_list') 


def pricelist(request):
    from cr_app.models import Hotel
    entry = Hotel.objects.get(pk=id)
    from cr_app.models import Pricing
    pricing_obj = Pricing.objects.all
    context = {'prices_obj': pricing_obj,'hotel_obj' :entry}
    return render (request, 'cr_app/pricelist.html',context)


def pricing(request,id):
    print('iiiiiiiiiiiidddddddddddd')
    print (id) 

    from cr_app.models import Hotel
    entry = Hotel.objects.get(pk=id)
    print(entry)
    print(entry.rooms)
    from cr_app.forms import PriceForm
    from cr_app.models import Pricing
    pricing_obj = Pricing.objects.get(pk=id)
    print(pricing_obj)
    print(pricing_obj.rooms) 
    if request.method == 'POST':
        uform = PriceForm(data = request.POST)
        if uform.is_valid():
            uform.save()
            return redirect(pricelist)   
        else: 
            message = 'something is missing'
            context = {'operation_message':message,'hotel_object': entry,'form':PriceForm}
            return render (request, 'cr_app/pricing.html',context)
    else:
         
        message = 'Fill in the pricing details'
        context = {'operation_message':message,'hotel_object': entry,'form':PriceForm}
        return render (request, 'cr_app/pricing.html',context)




def roombook(request,id):
    print('iiiiiiiiiiiidddddddddddd')   #once you select hotel from CustList it redirects her for booking
    print (id)                          # process

    from cr_app.models import Hotel
    entry = Hotel.objects.get(pk=id)
    print(entry)
    print(entry.rooms)
    #cheese_blog = entry.objects.get('hotel_name')
    #print(cheese_blog)
    #entry.blog = cheese_blog
    #entry.save()

    #context = { 'id':id,'room':entry.rooms}
    context = {'hotelobject':entry}
    return render(request, 'cr_app/customer.html',context)
    
          

# Delete View
class HotelDelete(DeleteView):
    model = Hotel
    # Setting returning URL
    success_url = reverse_lazy('hotel_list')



class CustomerSignUpView(CreateView):
    model = User_t
    form_class = CustomerSignUpForm
    template_name = 'cr_app/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class AdminSignUpView(CreateView):
    #model = Blog_j
    model = User_t
    form_class = AdminSignUpForm
    template_name = 'cr_app/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
