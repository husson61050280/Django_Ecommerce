from store.models import Category , Cart , Cart_Item
from store.views import _cart_id

#ทุกหน้าสามารถเข้าถึงตัวแปรได้  ให้นำมาไว้ที่นี่ (Context_processer)

def menu_links(request):
    links = Category.objects.all()
    return dict(links = links)

#คำนวนจำนวนสินค้าในตะกร้า
def count_cart(request):
    item_count = 0 #จำนวนสินค้าในตะกร้า

    if 'admin' in request.path:
        return {}
    else :
        #เช็คว่ามีตะกร้าสินค้าไหม
        try:
             #Query ข้อมูลตะกร้า
            cart = Cart.objects.get(cart_id = _cart_id(request))
            #โยนก้อนตะกร้าสินค้าไปเช็คใน cart_item (ดึงรายการสินค้าจากตะกร้าที่ส่งมา)
            cart_item = Cart_Item.objects.all().filter(cart = cart , active=True)
            for item in cart_item :
                item_count += item.Qty

        except Cart.DoesNotExist:
            item_count = 0 #จำนวนสินค้าในตะกร้า
              

    return dict(item_count = item_count)
