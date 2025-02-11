from django.urls import path
from .  import views

urlpatterns = [
    
    path('',views.home,name='home'),

    #product
    path('product/',views.product,name='product'),
    path('product/add-product/', views.add_product, name="add_product"),
    path('product/edit-product/', views.edit_product, name="edit_product"),
    path('product/fetch-products/', views.fetch_products, name="fetch_products"),

    #customer
    path('customer/',views.customer,name='customer'),
    path('customer/add-customer/', views.add_customer, name="add_customer"),
    path('customer/edit-customer/', views.edit_customer, name="edit_customer"),
    path('customer/fetch-customers/', views.fetch_customers, name="fetch_customers"),

    #bill
    path('bill/',views.bill,name='bill'),
    path('fetch_all_customers/', views.fetch_all_customers, name='fetch_all_customers'),
    path("bill/search_customers/", views.search_customers, name="search_customers"),
    path("bill/search_products/", views.search_products, name="search_products"),
    path("bill/submit_bill/", views.submit_invoice, name="submit_invoice"),
    path('fetch-billing-customers/', views.fetch_billing_customers, name='fetch_billing_customers'),
    path('fetch-billing-details/<int:billing_id>/', views.fetch_billing_details, name='fetch_billing_details')
   
]

    
