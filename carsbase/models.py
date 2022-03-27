from django.db import models
from datetime import date

# Create your models here.


class Colors(models.Model):
    """Цвета"""
    name = models.CharField('Цвет', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['name']


class Brands(models.Model):
    """Марки"""
    name = models.CharField('Марка', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'
        ordering = ['name']


class Models(models.Model):
    """Модели"""
    name = models.CharField('Модель', max_length=100)
    brand = models.ForeignKey(Brands, verbose_name='Марка', related_name='brand', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.brand} {self.name}'

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
        ordering = ['name']


class Orders(models.Model):
    """Заказы"""
    color = models.ForeignKey(Colors, verbose_name='Цвет', related_name='color', on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(Models, verbose_name='Модель', related_name='model', on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField('Количество')
    order_date = models.DateField('Дата', default=date.today)

    def __str__(self):
        return f'{self.count} {self.color} {self.model} {self.order_date}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date']