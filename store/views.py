from django.shortcuts import render, get_object_or_404, redirect
from store.models import Category, Product, Cart, Cart_Item, PerchaseOrder, OrderItem
# import file Form.py
from store.forms import SignUpForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm  # login
from django.contrib.auth import login, authenticate  # เช็ค login
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, InvalidPage
# บังคับ login
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe

# Create your views here.


def index(request, category_slug=None):
    products = None
    category_page = None
    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(available=True, category=category_page)
    else:
        products = Product.objects.all().filter(available=True)

    """
    set page หน้านึงมี สินค้ากี่รายการ
    9/6 = 2 หน้า
    """
    # จำนวนสินค้าในหนึ่งหน้า
    paginator = Paginator(products, 6)
    try:
        # GET.get = Query String
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        # เซตสินค้าต่อ 1 หน้า
        productperPage = paginator.page(page)
    except (EmptyPage, InvalidPage):
        productperPage = paginator.page(paginator.num_pages)  # ค่าสูงสุด

    return render(request, 'index.html', {'products': productperPage, 'category': category_page})


# Product Detial

def productPage(request, category_slug=None, product_slug=None):
    try:
        product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'Product.html', {'product': product})


# สร้าง Session
def _cart_id(request):
    # เช็คการสร้าง session
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# ถ้าจะกดซื้อสินค้า ต้อง login ก่อน (สร้างตะกร้า)
@login_required(login_url='Login')
# เพิ่มสินค้า ส่ง id สินค้าติดไปด้วย
def add_Cart(request, product_id):
    # ดึงสินค้า
    product = Product.objects.get(id=product_id)

    # สร้างตะกร้าสินค้า
    try:
        # มีตะกร้าสินค้าแล้ว
        cart = Cart.objects.get(cart_id=_cart_id(request))

    # ไม่มีตะกร้า
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        # ซื้อรายการสินค้าซ้ำ (เช็คจากตาราง Cart_Item)
        cart_item = Cart_Item.objects.get(product=product, cart=cart)
        # ต้องซื้อสินค้าไม่เกินจำนวนสต็อก
        if cart_item.Qty < cart_item.product.stock:
            cart_item.Qty += 1
            cart_item.save()
    # ซื้อครั้งแรก
    except Cart_Item.DoesNotExist:
        cart_item = Cart_Item.objects.create(
            product=product,
            cart=cart,
            Qty=1
        )
        cart_item.save()

    return redirect('cartdetial')


# คำนวนรายละเอียด ราคา ในตะกร้าสินค้า
def cartdetial(request):
    total = 0
    counter = 0  # จำนวนสินค้าในตะกร้า
    cart_item = None
    try:

        # Query ข้อมูลตะกร้าสินค้า โดยเช็คกับ session
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # โยนก้อนตะกร้าสินค้าไปเช็คใน cart_item (ดึงรายการสินค้าจากตะกร้าที่ส่งมา)
        cart_item = Cart_Item.objects.filter(cart=cart, active=True)
        for item in cart_item:
            total += (item.product.price*item.Qty)
            counter += item.Qty

    except Exception as e:
        pass

    # เพิ่มค่าให้ Stripe
    stripe.api_key = settings.SECRET_KEY
    stripe_total = int(total*100)
    description = "Payment Online"
    data_key = settings.PUBLIC_KEY

    # บันทึกข้อมูลบนเว็บ Stripe
    if request.method == "POST":
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            name = request.POST['stripeBillingName']
            address = request.POST['stripeBillingAddressLine1']
            city = request.POST['stripeBillingAddressCity']
            postcode = request.POST['stripeShippingAddressZip']

            # สร้าง customer ใน stripe
            customer = stripe.Customer.create(
                email=email,
                source=token
            )

            # สร้าง รายละเอียดจำนวนเงิน ใน stripe
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency='thb',
                description=description,
                customer=customer.id
            )

            # บันทึกข้อมูลใบสั่งซื้อ
            order = PerchaseOrder.objects.create(
                name=name,
                address=address,
                city=city,
                postcode=postcode,
                total=total,
                email=email,
                token=token
            )
            order.save()

            # บันทึกรายการสินค้าในใบสั่งซื้อ
            for item in cart_item:
                order_item = OrderItem.objects.create(
                    product = item.product.name,
                    qty = item.Qty,
                    price = item.product.price,
                    perchaseOrder = order
                )
                order_item.save()

                #ลดจำนวนสต็อกสินค้า
                product = Product.objects.get(id = item.product.id)
                product.stock = int(item.product.stock  - order_item.qty)
                product.save()
                item.delete()
            return redirect('Thankyou')


        except stripe.error.CardError as e:
            return False, e

    return render(request, 'Cart_detial.html', {
        'cart_item': cart_item,
        'total': total,
        'counter': counter,
        'data_key': data_key,
        'stripe_total': stripe_total,
        'description': description
    })


# ลบข้อมูลในตะกร้าสินค้า

def deleteCartdetial(request, product_id):
    # ตะกร้าสินค้า
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # สินค้าที่ต้องการลบ
    product = Product.objects.get(id=product_id)
    # ดึงข้อมูลที่ตรงกันออกมา
    cart_item = Cart_Item.objects.get(cart=cart, product=product, active=True)
    # ลบรายการสินค้า ออกจากตะกร้า
    cart_item.delete()
    return redirect('cartdetial')


# Register
def Register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # เช็คความถูกต้อง
        if form.is_valid():
            # บันทึกข้อมูล User
            form.save()

            # บันทึก Group Customer
            # ดึง Username มาใช้
            username = form.cleaned_data.get('username')

            # ดึงข้อมูล User จากฐานข้อมูล
            signUpUser = User.objects.get(username=username)
            # จัด Group
            customerGroup = Group.objects.get(name="Customer")
            # จับ User ลง Group
            customerGroup.user_set.add(signUpUser)
            return redirect('/')

    else:
        form = SignUpForm()
    return render(request, 'Register.html', {'form': form})


# Log in

def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # ยืนยันตัวตน เช็คในฐานข้อมูล
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('Register')

    else:
        form = AuthenticationForm()
    return render(request, 'Login.html', {'form': form})

# log out


def Logout(request):
    logout(request)
    return redirect('Login')


# ค้นหาข้อมูล
def search(request):
    status = True
    data_search = request.GET['title']
    # ค้นหาข้อมูลจากที่พิมมา
    products = Product.objects.filter(name__contains=data_search)
    return render(request, 'index.html', {'products': products, 'status': status})


#ประวัติการสั่งซื้อ
def orderHistory(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order = PerchaseOrder.objects.filter(email = email)
        return render(request ,'orderHistory.html' , {'orders': order })

#รายละเอียดสินค้าในใสั่งซื้อ
def orderDetail(request,order_id):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order = PerchaseOrder.objects.get(email = email , id = order_id)
        orderItem = OrderItem.objects.filter(perchaseOrder = order)
        return render(request ,'orderDetail.html' , {'orders': order , 'order_item' : orderItem })


#ขอบคุณลูกค้า
def Thankyou(request):
    return render(request , 'Thankyou.html')