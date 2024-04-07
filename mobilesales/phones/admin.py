from django.contrib import admin
from .models import Brand, Phone, Customer, Order, OrderItem

admin.site.register(Brand)
admin.site.register(Phone)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
