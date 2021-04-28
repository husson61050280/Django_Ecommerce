from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    # self เหมือน this ใน JAVA
    def __str__(self):
        return self.name

    class Meta:
        # เรียงลำดับข้อมูล (ตัวอักษรที่มาก่อน)
        ordering = ('name',)
        # เปลี่ยนชื่อด้านในจาก Category เป็น ข้อมูลประเภทสินค้า
        verbose_name_plural = 'หมวดหมู่'
        verbose_name = 'ข้อมูลประเภทสินค้า'

    def get_url(self):
        return reverse('product_by_category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product", blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        # เรียงลำดับข้อมูล (ตัวอักษรที่มาก่อน)
        ordering = ('name',)
        # เปลี่ยนชื่อด้านในจาก Category เป็น ข้อมูลประเภทสินค้า
        verbose_name_plural = 'ข้อมูลสินค้า'
        verbose_name = 'สินค้า'

    def __str__(self):
        return self.name

    #เอาไว้เป็นลิงค์ไปยังหน้า product detial
    def get_url(self):
        return reverse('product_detail' , args=[self.category.slug ,self.slug])


#ตะกร้าสินค้า
class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    #แสดง id ตะกร้าสินค้า
    def __str__(self):
        return self.cart_id
    
    class Meta:
        #สร้างชื่อตาราง
        db_table='Cart'
        ordering=('date_added',)
        verbose_name = 'ข้อมูลสินค้าในตะกร้า'
        verbose_name_plural = 'ข้อมูลตะกร้าสินค้า'
    

#รายการสินค้าในตะกร้า
class Cart_Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart =  models.ForeignKey(Cart, on_delete=models.CASCADE)
    Qty = models.IntegerField()
    #active แสดงสถานะรายการสินค้า
    active = models.BooleanField(default=True)

    class Meta:
        #สร้างชื่อตาราง
        db_table = 'Cart_Item'
        # ordering=('date_added',)

        #ตั้งชื่อ
        verbose_name = 'ข้อมูลสินค้า'
        verbose_name_plural = 'ข้อมูลรายการสินค้าในตะกร้า'
    

    #หาผลรวมรายการสินค้าแต่ละชิ้นว่ามีราคารวมเท่าไร
    #self เป็นตัวที่เราส่งค่ามา
    def sub_total(self):
        return self.product.price * self.Qty 
    
    #นำชื่อสินค้ามาแสดง
    def __str__(self):
        return self.product.name


#Model ใบสั่งซื้อ
class PerchaseOrder(models.Model):
    name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=255, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(max_length=250,blank=True)
    token = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #ตั้งค่าตาราง
    class Meta :
        #ชื่อตาราง
        db_table = 'PerchaseOrder'
        # เรียงลำดับข้อมูล (ตาม id)
        ordering = ('id',)

    #แสดงผลรหัสใบสั้งซื้อ
    def __str__ (self):
        return str(self.id)


#Model รายการสินค้าในใบสั่งซื้อ
class OrderItem(models.Model):
    product = models.CharField(max_length=255)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    perchaseOrder = models.ForeignKey(PerchaseOrder,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    #ตั้งค่าตาราง
    class Meta :
        #ชื่อตาราง
        db_table = 'OrderItem'
        # เรียงลำดับข้อมูล (ตาม id)
        ordering = ('id',)
    
    def sub_total(self):
        return self.qty*self.price

    
    #แสดงผลรหัสใบสั้งซื้อ
    def __str__ (self):
        return str(self.id)
