# Import forms
from django import forms

from .models import Hotel
from .models import User_t
from .models import Pricing

from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User

class HotelForm(forms.ModelForm):

    # The solution originally retrieved from
    #
    # https://stackoverflow.com/questions/33452278/how-to-add-bootstrap-class-to-django-createview-form-fields-in-the-template
    #
    # Thanks to César

    def __init__(self, *args, **kwargs):
        super(HotelForm, self).__init__(*args, **kwargs)
        self.fields['hotel_name'].widget.attrs = {
            'class': 'form-control input-lg'
        }
        self.fields['city_name'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['rooms'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Hotel
        fields = ('hotel_name', 'city_name', 'rooms')

class PriceForm(forms.ModelForm):

    class Meta:
        model = Pricing
        fields = ('starting_price', 'business_suite_price','presedential_suite_price')


class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User_t

    def save(self, commit=True):
        user_type = super().save(commit=False)
        user_type.is_customer = True
        if commit:
            user_type.save()
        return user_type



class AdminSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User_t

    def save(self, commit=True):
        user_type = super().save(commit=False)
        user_type.is_admin = True
        if commit:
            user_type.save()
        return user_type