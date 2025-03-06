from django.contrib import admin
from .models import User,Category,Product,ProductImage,Cart,CartItem,Vendor,Slider,Order,OrderItem
# Register your models here.

admin.site.register(User)

admin.site.register(Category)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(ProductImage)

admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.register(Vendor)
admin.site.register(Slider)

admin.site.register(Order)
admin.site.register(OrderItem)