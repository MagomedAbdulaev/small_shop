# coding=windows-1251
import datetime
import json
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Sum, F, Case, When
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from .forms import *


def home(request):

    products = Product.objects.all()
    paginator = Paginator(products, 4)  # По 4 на каждую страницу
    page_number = request.GET.get('page')  # номер страницы
    page_obj = paginator.get_page(page_number)  # сама страница
    context = {
        'title': 'Главная страница',
        'page_obj': page_obj,
    }
    if request.GET.get('filter'):
        products_filter = Product.objects.annotate(
            effective_price=Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=models.PositiveBigIntegerField()
            )
        )

        # Найти товар с минимальной эффективной ценой
        min_price_product = products_filter.order_by('effective_price').first()

        # Найти товар с максимальной эффективной ценой
        max_price_product = products_filter.order_by('-effective_price').first()

        # Найти сумму всех остатков
        total_remainder = Product.objects.aggregate(Sum('remainder'))['remainder__sum']
        context['max_price_product'] = max_price_product
        context['min_price_product'] = min_price_product
        context['total_remainder'] = total_remainder

    return render(request, 'home.html', context)


def product_detail(request, product_detail_slug):

    product = Product.objects.get(slug=product_detail_slug)

    context = {
        'title': product.name,
        'product': product,
    }

    return render(request, 'product_detail.html', context)


def profile(request):

    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = User.objects.filter(username=request.POST['login'])  # Находим пользователя по введенному логину,
            # Ибо он уникальный. Я использовал фильтр, а не get,
            # Потому что если пользователя нет то будет ошибка,
            # А с фильтром пустой queryset

            if user:
                if check_password(request.POST['password'], user.first().password):
                    login(request, user.first())
                    return redirect('shop:profile')
                else:
                    login_form.add_error(None, 'Неверный пароль')
            else:
                login_form.add_error(None, 'Такой пользователь не найден')

    else:
        login_form = UserLoginForm()

    context = {
        'title': "Профиль",
        'login_form': login_form,
    }

    return render(request, 'profile.html', context)


def logout_profile(request):
    logout(request)
    return redirect('shop:profile')


def categories(request):

    category = Category.objects.all()
    category_result = False
    context = {
        'title': "Категории",
        'category': category,
    }

    if request.GET.get('subcategory'):
        category_result = SubCategory.objects.get(id=request.GET.get('subcategory'))
        products = Product.objects.filter(subcategory_id=category_result.id)
    elif request.GET.get('category'):
        category_result = Category.objects.get(id=request.GET.get('category'))
        products = Product.objects.filter(category_id=category_result.id)

    if category_result:
        context['title'] = category_result.name
        context['products'] = products
        context['request_GET'] = True

    return render(request, 'categories.html', context)


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def cart(request):

    if 'cart' not in request.session:
        request.session['cart'] = {}
    cart_info = request.session['cart']

    products = []
    for prod in cart_info:
        product = Product.objects.get(id=cart_info[prod]['id'])
        product_count = cart_info[prod]['count']
        product_obj = {'product': product, 'count': product_count}
        products.append(product_obj)

    context = {
        'title': 'Корзина',
        'products': products,
    }

    return render(request, 'cart.html', context)


def cart_fetch(request):

    obj = {
        'status': 'ok',
    }

    if 'cart' not in request.session:
        request.session['cart'] = {}
    cart_info = request.session['cart']

    product_id = json.loads(request.body.decode())['id']
    if json.loads(request.body.decode())['action'] == 'add':
        if f'product{product_id}' not in cart_info:
            cart_info[f'product{product_id}'] = {'count': 1, 'id': product_id}
        else:
            cart_info[f'product{product_id}']['count'] += 1
    elif json.loads(request.body.decode())['action'] == 'remove':
        del cart_info[f'product{product_id}']
        obj['remove_product_id'] = product_id

    request.session.modified = True

    return JsonResponse(obj)


@login_required
def order(request):

    if 'cart' not in request.session:
        request.session['cart'] = {}
    cart_info = request.session['cart']

    products = []
    for prod in cart_info:
        product = Product.objects.get(id=cart_info[prod]['id'])
        product_count = cart_info[prod]['count']
        product_obj = {'product': product, 'count': product_count}
        if product.discount_price:
            product_obj['price_per_piece'] = product.discount_price
        else:
            product_obj['price_per_piece'] = product.price
        products.append(product_obj)

    if request.method == 'POST':
        products_text = ''  # продукты, которые заказал пользователь в удобном текстовом формате
        price_cart = 0
        for prod in products:
            product_item = f"{prod['product'].name} — {prod['count']}\n"
            price_cart += prod['price_per_piece'] * prod['count']
            products_text += product_item
        Order.objects.create(
            user=request.user,
            cart=cart_info,
            products=products_text,
            price=price_cart,
        )

    context = {
        'title': 'Заказ',
        'products': products,
    }

    return render(request, 'order.html', context)

