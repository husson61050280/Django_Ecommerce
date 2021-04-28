"""djangoEcomerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('Product', views.Product),
    path('', views.index, name='home'),
    path('Category/<slug:category_slug>',
         views.index, name="product_by_category"),
    path('Product/<slug:category_slug>/<slug:product_slug>',
         views.productPage, name="product_detail"),
    path('cart/add/<int:product_id>',views.add_Cart,name="addCart"),
    path('cartdetial',views.cartdetial, name="cartdetial"),
    path('cart/delete/<int:product_id>',views.deleteCartdetial,name="delCart"),
    path('account/Register',views.Register,name="Register"),
    path('account/Login',views.Login,name="Login"),
    path('account/Logout',views.Logout,name="Logout"),
    path('search/',views.search,name="search"),
    path('orderHistory/', views.orderHistory ,name="orderHistory"),
    path('orderDetail/<int:order_id>',views.orderDetail , name="orderDetail"),
    path('cart/Thankyou',views.Thankyou,name="Thankyou")
]



if settings.DEBUG:
    # /media/product
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # /static/
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    # รวมแล้วจะได้แบบนี้
    # /static/media/product/iphone.jpg
