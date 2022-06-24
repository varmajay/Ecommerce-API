from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import*
# Register your models here.
@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['email','role','gender','phone','address','profile','id']

@admin.register(UserToken)
class AdminUserToken(admin.ModelAdmin):
    list_display = ['user',]


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['product_name','category','quantity','price','description','pic','id']



@admin.register(Mycart)
class AdminMycart(admin.ModelAdmin):
    list_display = ['user','product','quantity']




@admin.register(Buyproduct)
class AdminBuyproduct(admin.ModelAdmin):
    list_display = ['buyer','product','address','status']
