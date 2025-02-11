from django.contrib import admin
from .models import Product,Customer, Billing, Billing_Item



admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Billing)
admin.site.register(Billing_Item)