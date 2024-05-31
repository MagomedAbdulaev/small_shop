from django.urls import path
from .views import *

app_name = 'shop'


urlpatterns = [
    path('product_detail/<slug:product_detail_slug>/', product_detail, name='product_detail'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_profile, name='logout'),
    path('categories/', categories, name='categories'),
    path('cart_fetch/', cart_fetch),
    path('activate/<uidb64>/<token>/<str:mail>/', order_payment, name='order_payment'),
    path('order/', order, name='order'),
    path('cart/', cart, name='cart'),
    path('', home, name='home'),
]
