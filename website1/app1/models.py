from django.db import models

# Create your models here.
class Contact(models.Model):
    contact_name = models.CharField(max_length=255)
    contact_pswd = models.CharField(max_length=255,default='')
    contact_email = models.EmailField(max_length=255)
    contact_message = models.TextField()

    def __str__(self) :
        return self.contact_name

class Registration(models.Model):
    registration_name = models.CharField(max_length=255)
    registration_phn = models.CharField(max_length=255)
    registration_email = models.EmailField(max_length=255)
    registration_paswrd = models.CharField(max_length=255,default='')

    def __str__(self) :
        return self.registration_name

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_image = models.FileField(null=True,upload_to="products")
    product_price = models.FloatField()
    product_description = models.TextField()
    product_category_name = models.CharField(max_length=255,default='',null=True)
    
    
    def __str__(self) :
        return self.product_name
    
class Cart(models.Model):
    cart_user =  models.CharField(max_length=250,default=None)
    cart_proid = models.IntegerField(null= True)
    cart_name = models.CharField(max_length=250)
    cart_price  = models.FloatField(max_length=250)
    cart_image = models.FileField(null=True)
    cart_qty = models. IntegerField()
    cart_amount = models.FloatField()    
    def __str__(self) :
        return self.cart_name
    
class Wishlist(models.Model):
   wishlist_user =  models.CharField(max_length=250,default=None)
   wishlist_proid = models.IntegerField(null= True)
   wishlist_name = models.CharField(max_length=250)
   wishlist_price  = models.FloatField(max_length=250)
   wishlist_image = models.FileField(null=True)
   wishlist_amount = models.FloatField()

   def __str__(self):
        return self.wishlist_name



class Order(models.Model):
    order_user = models.CharField(max_length=250,default=None)
    order_name = models. CharField(max_length=250)
    order_price = models.FloatField(max_length=250)
    order_image = models.FileField(max_length=255,null=True)
    order_qty = models.IntegerField()
    order_amount = models.FloatField()
    order_address = models .TextField(max_length=255,null=True)
    order_dlvtyp = models.CharField(max_length=255,null=True)
    order_status = models.IntegerField(default=0)

    def __str__(self):
        return self.order_name
    
    
class Category(models.Model):
    category_name = models.CharField(max_length=250,default=None)
    category_image = models.FileField(max_length=255,null=True)
    category_type = models.CharField(max_length=100,default="men")
     
    def __str__(self):
        return self.category_name