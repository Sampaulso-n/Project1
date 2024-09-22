from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Contact
from .models import Registration
from .models import Product
from .models import  Cart,Wishlist
from .models import  Order
from .models import  Category





# Create your views here.
def index(request):
    men = Category.objects.filter(category_type = 'men')
    women = Category.objects.filter(category_type = 'women')
    context= {
        'men':men,
        'women':women,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context,request))

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def contact(request):
    if request.method =='POST':
        con_name = request.POST["name"]
        con_phn = request.POST["phone_number"]
        con_email = request.POST["email"]
        con_msg = request.POST["message"]

        con = Contact(
            contact_name = con_name,
            contact_pswd = con_phn,
            contact_email = con_email,
            contact_message = con_msg,
        )

        con.save()
    template = loader.get_template('contact.html')
    return HttpResponse(template.render({},request))

def login(request):
    if 'usersession' in request.session:
        return HttpResponseRedirect('/account')
  
    if request.method =='POST':
        log_email= request.POST["email"]
        log_paswrd = request.POST["password"]
        
        log = Registration.objects.filter(
            registration_email= log_email,
            registration_paswrd= log_paswrd,
        )
        if log:
            request.session ['usersession']=log_email
            return HttpResponseRedirect('/account')
        

    template = loader.get_template('login.html')
    return HttpResponse(template.render({},request))

def register(request):
    if 'usersession' in request.session:
        return HttpResponseRedirect('/account')
    if request.method== "POST":
         reg_name = request.POST["name"]
         reg_phn = request.POST["phone_number"]
         reg_email = request.POST["email"]
         reg_paswrd = request.POST["pswd"]

         reg = Registration (
              registration_name = reg_name,
              registration_phn = reg_phn,
              registration_email = reg_email,
              registration_paswrd = reg_paswrd,
         )
         reg.save()
         

    template = loader.get_template('register.html')
    return HttpResponse(template.render({},request))


def account(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    order =''
    user = request.session['usersession']
    if 'order' in request.GET:

        order = Order.objects.filter( order_user = user)
    
    register =''
    user = request.session['usersession']
    if 'register' in request.GET:
        register = Registration.objects.filter(registration_email=user)
    wishlist =''
    if 'wishlist' in request.GET:
        wishlist = Wishlist.objects.filter(wishlist_user=user)
    context ={
        'order':order,
        "register":register,
        "wishlist":wishlist,
    }

     
  

    template = loader.get_template('account.html')
    return HttpResponse(template.render(context,request))

def logout(request):
    if 'usersession'  in request.session:
        del request.session['usersession']
        return HttpResponseRedirect ('/login')
    
def addproduct(request):
        if request.method =='POST':
            pro_name = request.POST["product_name"]
            pro_image = request.FILES["product_image"]
            pro_price = request.POST["product_price"]
            pro_description = request.POST["product_description"]
            pro_category = request.POST['categoryname']

            pro =Product(
                    product_name = pro_name,
                    product_image = pro_image,
                    product_price = pro_price,
                    product_description = pro_description,
                    product_category_name = pro_category
            )
            pro.save()

        category = Category.objects.all()
        context={
            'category': category,
        }

        template = loader.get_template('addproduct.html')
        return HttpResponse(template.render(context,request)) 


def product(request):
    if 'cname' in request.GET:
        cname = request.GET['cname']
        products = Product.objects.filter(product_category_name = cname)
    else:
        products=Product.objects.all().values()

    context={
        'products':products
        }
    template = loader.get_template("product.html")
    return HttpResponse(template.render(context,request))

def viewwishlist(request): 
     wishlist = Wishlist.objects.all()
     context ={
         "wishlist":wishlist
     }
     template = loader.get_template("wishlist.html")
     return HttpResponse(template.render(context,request))

def wishlist(request,id):
    if 'usersession' not in request.session:
        return HttpResponseRedirect ('/login')
    exist=Wishlist.objects.filter(wishlist_proid=id,wishlist_user=request.session["usersession"])
    if  exist:
          pass
    else:
         pro = Product.objects.filter(id=id)[0]
         cart = Wishlist(wishlist_user = request.session["usersession"],
                wishlist_proid=pro.id,
                wishlist_name=pro.product_name,
                wishlist_price=pro.product_price,
                wishlist_image= pro.product_image,
                wishlist_amount=pro.product_price)
         cart.save() 
    return HttpResponseRedirect("/viewwishlist") 

def addtocart(request,id):
    if 'usersession' not in request.session:
        return HttpResponseRedirect ('/login')
    exist=Cart.objects.filter(cart_proid=id,cart_user=request.session["usersession"])
    if exist:
        exstcart=Cart.objects.filter(cart_proid=id,cart_user=request.session["usersession"])[0]
        exstcart.cart_qty+=1
        exstcart.cart_amount = exstcart.cart_qty*exstcart.cart_price
        exstcart.save()
    else:
         
         pro = Product.objects.filter(id=id)[0]

         cart = Cart(cart_user = request.session["usersession"],
                cart_proid=pro.id,
                cart_name=pro.product_name,
                cart_price=pro.product_price,
                cart_image= pro.product_image,
                cart_qty=1,
                cart_amount=pro.product_price)
         cart.save() 

    return HttpResponseRedirect("/cart")  


 



def cart(request):
     if 'usersession' not in request.session:
         return HttpResponseRedirect ('/login')
     #delete cart item
     if 'del' in request.GET:
         id = request.GET['del']
         delcart= Cart.objects.filter(id=id)[0]
         delcart.delete()
    
     #change cart quantity     

     if 'q' in request.GET:
          q=request.GET['q']
          cp=request.GET['cp']
          cart3=Cart.objects.filter(id=cp)[0]

          if q=='inc':
               cart3.cart_qty+=1 
          elif q=='dec':
                 if (cart3.cart_qty>1):
                     cart3.cart_qty-=1
          cart3.cart_amount = cart3.cart_qty*cart3.cart_price
          cart3.save()    

     user = request.session["usersession"]
     cart = Cart.objects.filter(cart_user=user).values()
     cart2 = Cart.objects.filter(cart_user=user)

     tot = 0
     for x in cart2:
         tot+=x.cart_amount

     shp = tot * 10/100
     gst = tot * 18/100

     gtot = tot+shp+gst

     request.session["tot"]= tot
     request.session['gst']= gst
     request.session["shp"]= shp
     request.session["gtot"]= gtot

     context={
         'cart':cart,
         'tot':tot,
         'shp':shp,
         'gst':gst,
         'gtot':gtot
     }




     template = loader.get_template("cart.html")
     return HttpResponse(template.render(context,request))

def checkout (request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    co = 0
    adrs = dtype = ""
 
 #stp4 : After order submit
    if 'dlv_adrs' in request.POST:
        adrs = request.POST["dlv_adrs"]
        dtype = request.POST["dlv_type"]
        co=1

    user = request.session ["usersession"]   

    #step1:delete old data from orders
    oldodr=Order.objects.filter(order_user=user,order_status=0)
    oldodr.delete()

    #step2 : add cart data to table

    cart = Cart.objects.filter(cart_user=user)
    for x in cart:
        odr = Order(order_user = x.cart_user,
                    order_name = x.cart_name,
                    order_price=x.cart_price,
                    order_image=x.cart_image,
                    order_qty=x.cart_qty,
                    order_amount=x.cart_amount,
                    order_address=adrs,
                    order_dlvtyp =dtype,
                    order_status=0
                    )
        odr.save()

    #Step3 display order data
    order = Order.objects.filter(order_user=user,order_status=0).values()

    tot=request.session["tot"]
    gst=request.session["gst"]
    shp=request.session['shp']
    gtot=request.session["gtot"]
    # co=request.session["co"]

    context={
        'order': order,
        'tot' : tot ,
        'shp' : shp ,
        'gst' : gst ,
        'gtot' : gtot ,
        'co'  : co ,
    }
    
    template = loader.get_template('checkout.html')
    return HttpResponse (template.render(context,request))

def confirmorder(request):
    user = request.session['usersession']
    order = Order.objects.filter(order_user=user,order_status=0)
    for x in order:
        x.order_status=1
        x.save()
    template = loader.get_template("confirmorder.html")
    return HttpResponse(template.render({},request))

def myorders(request):
    user = request.session["usersession"]
    order = Order.objects.filter(order_user=user,order_status=1)
    context = {
        'order': order
    }    
    template = loader.get_template("myorders.html")
    return HttpResponse(template.render(context,request))

def addcategory(request):
    if request.method == 'POST':
        cat_name=request.POST["category_name"]
        cat_image=request.FILES["category_image"]

        cat =Category(
                    category_name = cat_name,
                    category_image = cat_image,
                )
        cat.save()


    template = loader.get_template("addcategory.html")
    return HttpResponse(template.render({},request))








            
                    
   




