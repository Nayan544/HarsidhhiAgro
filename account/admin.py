from django.contrib import admin
from .models import User,Category,Product,Cart,CartItem,Vendor,Slider
# Register your models here.

admin.site.register(User)

admin.site.register(Category)

admin.site.register(Product)

admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.register(Vendor)
admin.site.register(Slider)