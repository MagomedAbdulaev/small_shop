# coding=windows-1251
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class SubCategory(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название подкатегории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ПодКатегория"
        verbose_name_plural = "ПодКатегории"
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название категории')
    subcategories = models.ManyToManyField(to='SubCategory', blank=True, verbose_name='Подкатегории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class CharacteristicValue(models.Model):
    product = models.ForeignKey("Product", on_delete=models.PROTECT, verbose_name="Продукт")
    characteristic = models.CharField(max_length=80, verbose_name="Название характеристики:")
    value = models.CharField(max_length=180, verbose_name="Значение характеристики:")

    def __str__(self):
        return f'{self.characteristic}: {self.value}'

    class Meta:
        verbose_name = "Характеристика и Значение"
        verbose_name_plural = "Характеристики и Значения"
        ordering = ["characteristic", "value"]


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название товара')
    slug = models.SlugField(max_length=70, unique=True, verbose_name='Слаг товара')
    category = models.ForeignKey(to='Category', on_delete=models.PROTECT, verbose_name='Категория продукта')
    subcategory = models.ForeignKey(to='SubCategory', on_delete=models.PROTECT, verbose_name='ПодКатегория продукта')
    price = models.PositiveBigIntegerField(verbose_name='Цена товара')
    discount_price = models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Цена товара со скидкой')
    remainder = models.PositiveBigIntegerField(verbose_name='Товарный остаток')

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={"product_detail_slug": self.slug})

    def clean(self):
        super().clean()
        if self.pk:  # Проверяем, что объект уже сохранен в базе данных (имеет первичный ключ)
            original = self.__class__.objects.get(pk=self.pk)  # Получаем исходный объект из базы данных
            if self.name != original.name:
                while Product.objects.filter(slug=self.slug).exists():
                    last_letter_slug = self.slug[-1]
                    try:
                        last_letter_slug_int = int(last_letter_slug)
                        last_letter_slug_int += 1
                        self.slug = self.slug[:-1] + str(last_letter_slug_int)
                    except ValueError:
                        self.slug += '2'
        else:
            while Product.objects.filter(slug=self.slug).exists():
                last_letter_slug = self.slug[-1]
                try:
                    last_letter_slug_int = int(last_letter_slug)
                    last_letter_slug_int += 1
                    self.slug = self.slug[:-1] + str(last_letter_slug_int)
                except ValueError:
                    self.slug += '2'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачено'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="Дата проведения заказа")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления заказа")
    status = models.PositiveSmallIntegerField(default=CREATED, choices=STATUSES, verbose_name="Статус заказа")
    cart = models.JSONField(default=dict, verbose_name="Товары добавленные в заказ")
    price = models.PositiveIntegerField(default=0, verbose_name="Цена заказа(цена корзины)")
    products = models.TextField(default='', max_length=3000, verbose_name="Продукты")

    def __str__(self):
        return f'Заказ номер {self.id}, {self.status}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-date_created"]
