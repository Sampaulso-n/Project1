from django.contrib import admin
from .models import Contact
from .models import Registration
from .models import Product
from .models import Cart , Order , Wishlist ,Category

admin.site.register(Contact)
admin.site.register(Registration)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Wishlist)
admin.site.register(Category)



