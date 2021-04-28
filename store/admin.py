from django.contrib import admin
from store.models import Category,Product,Cart,Cart_Item,OrderItem,PerchaseOrder

"""
ตกแต่งหน้า Admin นำคอลัมมาแสดง
"""
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price' , 'stock' , 'created', 'updated']
    list_per_page = 5
    #แก้ไขคอลัมนั้นๆได้เลย
    list_editable=['price','stock']

#ใบสั่งซื้อ
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name' , 'email', 'total', 'token','created','updated'] 
    list_per_page = 5
    #แก้ไขคอลัมนั้นๆได้เลย

#รายการสินค้าในใบสั่งซื้อ
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product' , 'price', 'qty' , 'perchaseOrder','created','updated'] 
    list_per_page = 5
    #แก้ไขคอลัมนั้นๆได้เลย




# Register your models here.

#เพื่อให้ สามารถเช็คได้ ใน /admin
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(Cart_Item)
admin.site.register(PerchaseOrder , OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)


#วิธีอัพตารางขึ้น (migrationfile)
"""
python manage.py makemigrations
(เอาตารางขึ้น database)
python manage.py migrate

"""


# Create superuser(admin)
# python manage.py createsuperuser

