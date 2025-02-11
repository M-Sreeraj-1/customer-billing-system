from datetime import date, datetime, timezone
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Product,Customer, Billing, Billing_Item
from django.db.models import Count
from django.utils.timezone import now
from django.db.models.functions import Lower
import json
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    return render(request,'home.html')


# product

def product(request):
    return render(request,'product.html')



def add_product(request):
    if request.method == "POST":
        product_name = request.POST.get('product_name', '').strip()
        price = request.POST.get('price', '').strip()
        tax = request.POST.get('tax', '').strip()
        
        
        errors = {}

        
        if not product_name:
            errors['product_name'] = "Product name is required."
        elif Product.objects.filter(product_name__iexact=product_name).exists():
            errors['product_name'] = "Product already exists."
        if product_name:
            if product_name.find(" ") == -1:
                if not product_name.isalpha():
                        errors['product_name'] = "Only Alphabets required." 
            else:
                seperate=product_name.split()
                for i in range(len(seperate)):
                    if not seperate[i].isalpha():
                        errors['product_name'] = "Only Alphabets required." 

        if not price:
            errors['price'] = "Price is required."
        else:
            try:
                price = float(price)
                if price <= 0:
                    errors['price'] = "Price must be greater than 0."
            except ValueError:
                errors['price'] = "Invalid price format."

        if not tax:
            errors['tax'] = "Tax is required."
        else:
            try:
                tax = float(tax)
                if tax < 0:
                    errors['tax'] = "Tax cannot be negative."
            except ValueError:
                errors['tax'] = "Invalid tax format."

        if errors:
            return JsonResponse({"status": "error", "errors": errors})
        
        Product.objects.create(
            product_name=product_name,
            price=price,
            tax=tax
        )
        return JsonResponse({"status": "success", "message": "Product added successfully."})


def edit_product(request):
    if request.method == "POST":
        product_id = request.POST.get('id', '').strip()
        product_name = request.POST.get('product_name', '').strip()
        price = request.POST.get('price', '').strip()
        tax = request.POST.get('tax', '').strip()

        errors = {}

       
        if not product_id or not Product.objects.filter(id=product_id).exists():
            errors['edit_product_id'] = "Invalid product ID."

        if not product_name:
            errors['edit_product_name'] = "Product name is required."
        elif Product.objects.filter(product_name__iexact=product_name).exclude(id=product_id).exists():
            errors['edit_product_name'] = "Product already exists."
        
        if product_name:
            if product_name.find(" ") == -1:
                if not product_name.isalpha():
                        errors['edit_product_name'] = "Only Alphabets required." 
            else:
                seperate=product_name.split()
                for i in range(len(seperate)):
                    if not seperate[i].isalpha():
                        errors['edit_product_name'] = "Only Alphabets required." 

        if not price:
            errors['edit_price'] = "Price is required."
        else:
            try:
                price = float(price)
                if price <= 0:
                    errors['edit_price'] = "Price must be greater than 0."
            except ValueError:
                errors['edit_price'] = "Invalid price format."

        if not tax:
            errors['edit_tax'] = "Tax is required."
        else:
            try:
                tax = float(tax)
                if tax < 0:
                    errors['edit_tax'] = "Tax cannot be negative."
            except ValueError:
                errors['edit_tax'] = "Invalid tax format."

        if errors:
            return JsonResponse({"status": "error", "errors": errors})

        product = get_object_or_404(Product, id=product_id)
        product.product_name = product_name
        product.price = price
        product.tax = tax
        product.save()
        return JsonResponse({"status": "updated", "message": "Product updated successfully."})
    


def fetch_products(request):
    search = request.GET.get("search", "")
    sort = request.GET.get("sort", "")
    order = request.GET.get("order", "asc") 
    page = int(request.GET.get("page", 1))  
    size = int(request.GET.get("size", 10))  

    
    products = Product.objects.all().order_by("-id")

    
    

   
    if sort:
        products = Product.objects.annotate(
        sort_field=Lower(sort)
        ).order_by(f"{'' if order == 'asc' else '-'}sort_field")

    if search:
        products = products.filter(product_name__istartswith=search)

    
    total_products = products.count()
    start = (page - 1) * size
    end = start + size
    products = products[start:end]

    
    product_data = list(products.values())
    return JsonResponse({
        "products": product_data,
        "total": total_products,
        "page": page,
        "size": size
    })





# Customer

def customer(request):
    return render(request,'customer.html')


def add_customer(request):
    if request.method == "POST":

        
        errors = {}
        required_fields = ['customer_name', 'email', 'phone','address']
        
        email_value=request.POST['email'].strip()
        email_required=request.POST['email'].strip().find("@")

        for field in required_fields:
            if not request.POST.get(field, "").strip():
                errors[field] = f"{field.replace('_', ' ').capitalize()} is required."

        if Customer.objects.filter(customer_name__iexact=request.POST['customer_name'].strip()).exists():
            errors['customer_name'] = "Customer name already exists."
        
        if Customer.objects.filter(email__iexact=request.POST['email']).exists():
            errors['email'] = "Email already exists."
        
        if Customer.objects.filter(phone__iexact=request.POST['phone'].strip()).exists():
            errors['phone'] = "Phone number already exists."

        if  request.POST['customer_name'].strip():

            if request.POST['customer_name'].strip().find(" ") == -1:
                if not request.POST['customer_name'].strip().isalpha():
                        errors['customer_name'] = "Only Alphabets required." 
            else:
                seperate=request.POST['customer_name'].strip().split()
                for i in range(len(seperate)):
                    if not seperate[i].isalpha():
                        errors['customer_name'] = "Only Alphabets required." 
        if request.POST['phone'].strip():
            if not request.POST['phone'].strip().isdigit():
                errors['phone'] = "Only numbers required."

        if request.POST['email'].strip():
            if email_required == -1:
                errors['email'] = "Include '@' in the email address. '"+email_value+"' is missing an '@'."
            elif request.POST['email'].strip().find(" ") != -1:
                errors['email'] = "No in-between space required."
            else:
                if request.POST['email'].strip().endswith("@"):
                    errors['email'] = "please enter a part following '@'. '"+email_value+"' is incomplete."

        if request.POST['phone'].strip().isdigit():
            if len(request.POST['phone'].strip()) !=10:
                errors['phone'] = "10 digits required"
        
        if request.POST['company_phone'].strip():
            if not request.POST['company_phone'].strip().isdigit():
                errors['company_phone'] = "Only numbers required."
            if request.POST['company_phone'].strip().isdigit():
                if len(request.POST['company_phone'].strip()) !=10:
                    errors['company_phone'] = "10 digits required"

            if request.POST.get('company_phone').strip() == request.POST['phone'].strip():
                errors['company_phone'] = "phone number Matches!."
                errors['phone'] = "phone number Matches!."

            if Customer.objects.filter(company_phone__iexact=request.POST['phone'].strip()).exists() :
                errors['phone'] = "Phone number is already exists."
            

        
        company=['company_name','company_gst','company_phone','company_address']
        
        for i in range(0,len(company)):
            if request.POST[company[i]].strip():
                clone=[]
                clone.append(company.copy())
                clone[0].remove(company[i])
                for j in range(0,len(clone[0])):
                    if request.POST[clone[0][j]] == "":
                        
                        seperate=clone[0][j].replace("_"," ")
                        errors[clone[0][j]] =  f"please fill {seperate}."

        if request.POST['company_name'].strip() and request.POST['company_gst'].strip(): 
            if request.POST['company_name'].strip().find(" ") == -1:
                if not request.POST['company_name'].strip().isalpha():
                        errors['company_name'] = "Only Alphabets required." 
            else:
                seperate=request.POST['company_name'].strip().split()
                for i in range(len(seperate)):
                    if not seperate[i].isalpha():
                        errors['company_name'] = "Only Alphabets required." 
                      
            if Customer.objects.filter(company_name__iexact=request.POST['company_name'].strip(),company_gst__iexact=request.POST['company_gst'].strip()).exists():
                errors['company_name'] = "Name already exists."
                errors['company_gst'] ="GST already exists."

        if request.POST['company_name'].strip() : 

            if request.POST['company_name'].strip().find(" ") == -1:
                if not request.POST['company_name'].strip().isalpha():
                        errors['company_name'] = "Only Alphabets required." 
            else:
                seperate=request.POST['company_name'].strip().split()
                for i in range(len(seperate)):
                    if not seperate[i].isalpha():
                        errors['company_name'] = "Only Alphabets required."           
    
            if Customer.objects.filter(company_name__iexact=request.POST['company_name'].strip()).exists():
                errors['company_name'] = "Name already exists."
        
        if request.POST['company_gst'].strip() :          
            if Customer.objects.filter(company_gst__iexact=request.POST['company_gst'].strip()).exists():   
                errors['company_gst'] ="GST already exists."

        if request.POST['company_phone'].strip() :      
            if Customer.objects.filter(company_phone__iexact=request.POST['company_phone'].strip()).exists():   
                errors['company_phone'] ="Phone number already exists."

        if errors:
            return JsonResponse({"status": "error", "errors": errors})       
        

        Customer.objects.create(
            customer_name=request.POST['customer_name'].strip(),
            email=request.POST['email'],
            phone=request.POST['phone'].strip(),
            address=request.POST['address'].strip(),
            company_name=request.POST['company_name'].strip(),
            company_gst=request.POST['company_gst'].strip(),
            company_phone=request.POST['company_phone'].strip(),
            company_address=request.POST['company_address'].strip()
        )
        return JsonResponse({"status": "success", "message": "Customer added sucessfully."})

def edit_customer(request):
    if request.method == "POST":

        errors = {}
        required_fields = ['customer_name', 'email', 'phone', 'address']

        email_value=request.POST['email'].strip()
        email_required=request.POST['email'].strip().find("@")
        
        for field in required_fields:
            if not request.POST.get(field, "").strip():
                errors["edit_"+field] = f"{field.replace('_', ' ').capitalize()} is required."

        if Customer.objects.filter(customer_name__iexact=request.POST['customer_name'].strip()).exclude(id=request.POST['id']).exists():
            errors['edit_customer_name'] = "Customer name already exists."
        
        if Customer.objects.filter(email__iexact=request.POST['email']).exclude(id=request.POST['id']).exists():
            errors['edit_email'] = "Email already exists."
        
        if Customer.objects.filter(phone__iexact=request.POST['phone'].strip()).exclude(id=request.POST['id']).exists():
            errors['edit_phone'] = "Phone number already exists."

        if  request.POST['customer_name'].strip():
            if request.POST['customer_name'].strip().find(" ") == -1:
                if not request.POST['customer_name'].strip().isalpha():
                        errors['edit_customer_name'] = "Only Alphabets required." 
            else:
                seperate=request.POST['customer_name'].strip().split()
                for i in range(len(seperate)):
                    if not seperate[i].isalpha():
                        errors['edit_customer_name'] = "Only Alphabets required."  

        if request.POST['email'].strip():
            if email_required == -1:
                errors['edit_email'] = "Include '@' in the email address. '"+email_value+"' is missing an '@'."
            elif request.POST['email'].strip().find(" ") != -1:
                errors['edit_email'] = "Remove in-between space."
            else:
                if request.POST['email'].strip().endswith("@"):
                    errors['edit_email'] = "please enter a part following '@'. '"+email_value+"' is incomplete."

        if not request.POST['phone'].strip().isdigit():
            errors['edit_phone'] = "Only numbers required."

        if request.POST['phone'].strip().isdigit():
            if len(request.POST['phone'].strip()) !=10:
                errors['edit_phone'] = "10 digits required"

        if Customer.objects.filter(company_phone__iexact=request.POST['phone'].strip()).exists() :
                errors['edit_phone'] = "Phone number already exists."
        

        company=['company_name','company_gst','company_phone','company_address']
        
        for i in range(0,len(company)):
            if request.POST[company[i]].strip():
                clone=[]
                clone.append(company.copy())
                clone[0].remove(company[i])
                for j in range(0,len(clone[0])):
                    
                    if request.POST[clone[0][j]] == "":
                        
                        seperate=clone[0][j].replace("_"," ")
                        errors["edit_"+clone[0][j]] = f"please fill {seperate}."


        if request.POST['company_name'].strip() and request.POST['company_gst'].strip():

            if Customer.objects.filter(company_name__iexact=request.POST['company_name'].strip(),company_gst__iexact=request.POST['company_gst'].strip()).exclude(id=request.POST['id']).exists():
                errors['edit_company_name'] = "Name already exists."
                errors['edit_company_gst'] ="GST already exists."

        if request.POST['company_name'].strip() :
            if request.POST['company_name'].strip().find(" ") == -1:
                if not request.POST['company_name'].strip().isalpha():
                        errors['edit_company_name'] = "Only Alphabets required." 
            else:
                seperate=request.POST['company_name'].strip().split()
                for i in range(len(seperate)):
                    if not seperate[i].isalpha():
                        errors['edit_company_name'] = "Only Alphabets required." 

            if Customer.objects.filter(company_name__iexact=request.POST['company_name'].strip()).exclude(id=request.POST['id']).exists():
                errors['edit_company_name'] = "Name already exists."
        if request.POST['company_gst'].strip() :    
            if Customer.objects.filter(company_gst__iexact=request.POST['company_gst'].strip()).exclude(id=request.POST['id']).exists():   
                errors['edit_company_gst'] ="GST already exists."
        
        if request.POST['company_phone'].strip():
            if not request.POST['company_phone'].strip().isdigit():
                errors['edit_company_phone'] = "Only numbers required."
            if request.POST['company_phone'].strip().isdigit():
                if len(request.POST['company_phone'].strip()) !=10:
                    errors['edit_company_phone'] = "10 digits required"
            if request.POST.get('company_phone').strip() == request.POST['phone'].strip():
                errors['edit_company_phone'] = "phone number Matches!."
                errors['edit_phone'] = "phone number Matches!."


            if Customer.objects.filter(company_phone__iexact=request.POST['company_phone'].strip()).exclude(id=request.POST['id']).exists():   
                errors['edit_company_phone'] ="Phone number already exists."
            
        if errors:
            return JsonResponse({"status": "error", "errors": errors})

            
        customer = Customer.objects.get(id=request.POST['id'])
        customer.customer_name = request.POST['customer_name'].strip()
        customer.email = request.POST['email'].strip()
        customer.phone = request.POST['phone'].strip()
        customer.address = request.POST['address'].strip()
            
        customer.company_name = request.POST['company_name'].strip()
        customer.company_gst = request.POST['company_gst'].strip()
        customer.company_phone = request.POST['company_phone'].strip()
        customer.company_address = request.POST['company_address'].strip()

        customer.save()
        return JsonResponse({"status": "updated", "message": "Customer updated sucessfully."})



def fetch_customers(request):
    search = request.GET.get("search", "")
    sort = request.GET.get("sort", "id")  
    order = request.GET.get("order", "asc")
    page = int(request.GET.get("page", 1)) 
    size = int(request.GET.get("size", 10))  


    if sort != 'id':
        customers =  Customer.objects.annotate(
            sort_field=Lower(sort)
        ).order_by(f"{'' if order == 'asc' else '-'}sort_field")
    else:
        customers =  Customer.objects.order_by(f"{'' if order == 'asc' else '-'}{sort}")

    if search:
        customers = customers.filter(
            Q(customer_name__istartswith=search) | 
            Q(phone__istartswith=search) | 
            Q(email__istartswith=search) | 
            Q(address__istartswith=search) |
            Q(company_name__istartswith=search) 
        )

    paginator = Paginator(customers, size)
    page_obj = paginator.get_page(page)

    customers_data = list(page_obj.object_list.values())
    return JsonResponse({
        "customers": customers_data,
        "total_pages": paginator.num_pages,
        "current_page": page,
        "page_size": size,
        "total_items": paginator.count,
    })



#bill

def bill(request):
    return render(request,'bill.html')



def fetch_all_customers(request):
    if request.method == "GET":
        customers = Customer.objects.all().values("customer_name","phone","company_name")
        return JsonResponse({"customers": list(customers)})
    return JsonResponse({"customers": []})



def search_customers(request):
    if request.method == "GET" and "query" in request.GET:
        query = request.GET["query"].strip()
        customers = Customer.objects.filter(customer_name__istartswith=query).values("customer_name","phone","company_name")
        return JsonResponse({"customers": list(customers)})
    return JsonResponse({"customers": []})





def search_products(request):
    query = request.GET.get('query', '').strip()
    products = Product.objects.filter(product_name__istartswith=query).values('id','product_name', 'tax', 'price')
    return JsonResponse({'products': list(products)})




def submit_invoice(request):
    if request.method == "POST":
        data = json.loads(request.body)
        errors = []

        if not Customer.objects.filter(customer_name__iexact =data.get("customerName").strip()).exists():
            errors.append({"field": "customer", "message": "customer doesn't exists."})
        
        for item in data.get("productDetails", []):
            product_name = item["productName"]
            product_price = item["price"]
            product_quantity = item["quantity"]
            if not Product.objects.filter(product_name =product_name.strip()).exists():
               errors.append({"field": "product",  "message": "product doesn't exists."})
            if not product_quantity.isnumeric():
               errors.append({"field": "product",  "message": "please provide valid quantity"})

            if Product.objects.filter(product_name =product_name).exists():
               if not Product.objects.filter(product_name =product_name,price=product_price).exists():
                  errors.append({"field": "product",  "message": " please select the product from the dropdown list."})

        if errors:
            return JsonResponse({"status": "error", "errors": errors})
        
        customer_name = data.get("customerName")
        customer = get_object_or_404(Customer, customer_name=customer_name)

        date = data.get("date")
        grand_total = data.get("grandTotal")
        tax_total = data.get("totalTax")
        billing = Billing.objects.create(customer=customer, grand_total=grand_total,tax_total=tax_total, date=date)

        
        for item in data.get("productDetails", []):
            product_name = item["productName"]
            product = get_object_or_404(Product, product_name=product_name)

            Billing_Item.objects.create(
                billing=billing,
                product=product,
                quantity=int(item["quantity"]),
                sub_total=float(item["subtotal"]),
                date=billing.date
            )

        return JsonResponse({"status":"success","message": "Invoice submitted successfully!."}, status=200)

    return JsonResponse({"message": "Invalid request method."}, status=405)






def fetch_billing_customers(request):
    search_query = request.GET.get('search', '').strip()
    sort_field = request.GET.get('sortField', 'id')  
    sort_order = request.GET.get('sortOrder', 'asc')
    page_number = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('size', 10))


    billing_data = (
        Billing.objects.select_related('customer')
        .annotate(item_count=Count('billing_products')) 
        .order_by('-id')    
     )
    if search_query.find('/'):
        seperation=search_query.split('/')
        wantedDate=""
        for i in range(len(seperation),0,-1):
            if i == 1:
                if len(str(seperation[i-1])) == 2:
                    wantedDate+=seperation[i-1]+"-"
                    search_query=wantedDate[0:len(wantedDate)-1]
            elif i == 2:
                if len(str(seperation[i-1])) == 2:
                    wantedDate+=seperation[i-1]+"-"
                    search_query=wantedDate[0:len(wantedDate)-1]
            elif i == 3 :
                if len(str(seperation[i-1])) == 4:
                    wantedDate+=seperation[i-1]+"-"
                    search_query=wantedDate[0:len(wantedDate)-1]
            
            
    

    if search_query:
        billing_data = billing_data.filter(Q(customer__customer_name__istartswith=search_query) | Q(date__icontains=search_query))
    

    if sort_field not in ['customer__customer_name', 'item_count', 'grand_total','date']:
        sort_field = 'id' 

    if sort_field == 'customer__customer_name':
        billing_data = billing_data.annotate(
            sort_field=Lower('customer__customer_name')
        )
        sort_field = 'sort_field'

    if sort_order == 'desc':
        sort_field = f'-{sort_field}'
    else:
        billing_data = billing_data.order_by('-id')

    billing_data = billing_data.order_by(sort_field)

    

    paginator = Paginator(billing_data, page_size)
    page = paginator.get_page(page_number)

    customers = [
        {
            'customer_name': billing.customer.customer_name,
            'billing_id': billing.id,
            'date': billing.date.strftime('%d/%m/%Y'),
            'item_count': billing.item_count,
            'grand_total': float(billing.grand_total)
        }
        for billing in page.object_list
    ]

    return JsonResponse({
        'customers': customers,
        'total_pages': paginator.num_pages,
        'current_page': page.number,
        'page_size': page_size
    })







def fetch_billing_details(request, billing_id):
    try:
        
        billing = Billing.objects.get(id=billing_id)
        customer = billing.customer
        billing_items = Billing_Item.objects.filter(billing=billing)
        
        
        billing_data = {
            'company_name':customer.company_name,
            'customer_name': customer.customer_name,
            'customer_email': customer.email,
            'customer_phone': customer.phone,
            'customer_address': customer.address,
            'date': billing.date.strftime('%d/%m/%Y'),
            'grand_total': str(billing.grand_total),
            'tax_total': str(billing.tax_total),
            'items': []
        }
        
        for item in billing_items:
            product = item.product
            billing_data['items'].append({
                'product_name': product.product_name,
                'quantity': item.quantity,
                'price': str(product.price),
                'tax': str(product.tax),
                'sub_total': str(item.sub_total)
            })
        
        return JsonResponse({'billing_data': billing_data})
    
    except Billing.DoesNotExist:
        return JsonResponse({'error': 'Billing record not found.'}, status=404)

