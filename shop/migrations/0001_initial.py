# Generated by Django 5.0.6 on 2024-05-30 13:17

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Название подкатегории')),
            ],
            options={
                'verbose_name': 'ПодКатегория',
                'verbose_name_plural': 'ПодКатегории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата проведения заказа')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления заказа')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Создан'), (1, 'Оплачено'), (2, 'В пути'), (3, 'Доставлен')], default=0, verbose_name='Статус заказа')),
                ('cart', models.JSONField(default=dict, verbose_name='Товары добавленные в заказ')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Цена заказа(цена корзины)')),
                ('products', models.TextField(default='', max_length=3000, verbose_name='Продукты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название товара')),
                ('slug', models.SlugField(max_length=70, unique=True, verbose_name='Слаг товара')),
                ('price', models.PositiveBigIntegerField(verbose_name='Цена товара')),
                ('discount_price', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Цена товара со скидкой')),
                ('remainder', models.PositiveBigIntegerField(verbose_name='Товарный остаток')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.category', verbose_name='Категория продукта')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.subcategory', verbose_name='ПодКатегория продукта')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CharacteristicValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('characteristic', models.CharField(max_length=80, verbose_name='Название характеристики:')),
                ('value', models.CharField(max_length=180, verbose_name='Значение характеристики:')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Характеристика и Значение',
                'verbose_name_plural': 'Характеристики и Значения',
                'ordering': ['characteristic', 'value'],
            },
        ),
        migrations.AddField(
            model_name='category',
            name='subcategories',
            field=models.ManyToManyField(blank=True, to='shop.subcategory', verbose_name='Подкатегории'),
        ),
    ]
