# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm

from phones.models import Customer, Phone, Brand


class CustomerCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class PhoneForm(forms.ModelForm):

    new_brand = forms.CharField(max_length=100, required=False, label='New Brand')

    class Meta:
        model = Phone
        fields = ['brand', 'model', 'price', 'stock_quantity', 'photo', 'description']

    def clean(self):
        cleaned_data = super().clean()
        new_brand_name = cleaned_data.get('new_brand')

        if new_brand_name:
            brand, created = Brand.objects.get_or_create(name=new_brand_name)
            cleaned_data['brand'] = brand

        return cleaned_data

