from django.db import models
from django.utils import timezone
from django.utils.timezone import now




class Product(models.Model):
    product_name = models.CharField(max_length=100)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    

class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    company_name = models.CharField(max_length=100,null=True)
    company_gst = models.CharField(max_length=15,null=True)
    company_phone = models.CharField(max_length=15,null=True)
    company_address = models.CharField(max_length=200,null=True)

        

class Billing(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    def __str__(self):
        return f"{self.customer} - {self.date.strftime('%d-%m-%Y')}"

    class Meta:
        ordering = ['-id']




class Billing_Item(models.Model):
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE, related_name="billing_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField(default=now)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
      return f"{self.billing_id} - {self.date.strftime('%d-%m-%Y')}"
