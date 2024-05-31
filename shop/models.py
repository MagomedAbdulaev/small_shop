# coding=windows-1251
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class SubCategory(models.Model):
    name = models.CharField(max_length=40, verbose_name='�������� ������������')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "������������"
        verbose_name_plural = "������������"
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='�������� ���������')
    subcategories = models.ManyToManyField(to='SubCategory', blank=True, verbose_name='������������')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "���������"
        verbose_name_plural = "���������"
        ordering = ["name"]


class CharacteristicValue(models.Model):
    product = models.ForeignKey("Product", on_delete=models.PROTECT, verbose_name="�������")
    characteristic = models.CharField(max_length=80, verbose_name="�������� ��������������:")
    value = models.CharField(max_length=180, verbose_name="�������� ��������������:")

    def __str__(self):
        return f'{self.characteristic}: {self.value}'

    class Meta:
        verbose_name = "�������������� � ��������"
        verbose_name_plural = "�������������� � ��������"
        ordering = ["characteristic", "value"]


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='�������� ������')
    slug = models.SlugField(max_length=70, unique=True, verbose_name='���� ������')
    category = models.ForeignKey(to='Category', on_delete=models.PROTECT, verbose_name='��������� ��������')
    subcategory = models.ForeignKey(to='SubCategory', on_delete=models.PROTECT, verbose_name='������������ ��������')
    price = models.PositiveBigIntegerField(verbose_name='���� ������')
    discount_price = models.PositiveBigIntegerField(blank=True, null=True, verbose_name='���� ������ �� �������')
    remainder = models.PositiveBigIntegerField(verbose_name='�������� �������')

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={"product_detail_slug": self.slug})

    def clean(self):
        super().clean()
        if self.pk:  # ���������, ��� ������ ��� �������� � ���� ������ (����� ��������� ����)
            original = self.__class__.objects.get(pk=self.pk)  # �������� �������� ������ �� ���� ������
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
        verbose_name = "�������"
        verbose_name_plural = "��������"
        ordering = ["name"]


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, '������'),
        (PAID, '��������'),
        (ON_WAY, '� ����'),
        (DELIVERED, '���������'),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="������������")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="���� ���������� ������")
    updated = models.DateTimeField(auto_now=True, verbose_name="���� ���������� ������")
    status = models.PositiveSmallIntegerField(default=CREATED, choices=STATUSES, verbose_name="������ ������")
    cart = models.JSONField(default=dict, verbose_name="������ ����������� � �����")
    price = models.PositiveIntegerField(default=0, verbose_name="���� ������(���� �������)")
    products = models.TextField(default='', max_length=3000, verbose_name="��������")

    def __str__(self):
        return f'����� ����� {self.id}, {self.status}'

    class Meta:
        verbose_name = "�����"
        verbose_name_plural = "������"
        ordering = ["-date_created"]
