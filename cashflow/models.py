from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Status(models.Model):
    """Статус записи ДДС (Бизнес, Личное, Налог)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название статуса")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Type(models.Model):
    """Тип операции (Пополнение, Списание)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название типа")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория расходов/доходов"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name="Тип"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['type__name', 'name']
        unique_together = ['name', 'type']

    def __str__(self):
        return f"{self.type.name} - {self.name}"


class Subcategory(models.Model):
    """Подкатегория расходов/доходов"""
    name = models.CharField(max_length=100, verbose_name="Название подкатегории")
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name="Категория"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['category__name', 'name']
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class CashFlowRecord(models.Model):
    """Запись о движении денежных средств"""
    date = models.DateField(
        default=timezone.now,
        verbose_name="Дата операции"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name="Статус"
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        verbose_name="Тип"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Сумма"
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления записи")

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} - {self.type.name} - {self.amount} р."

    def clean(self):
        """Валидация бизнес-правил"""
        super().clean()

        # Проверка соответствия категории типу
        if self.category.type != self.type:
            raise models.ValidationError(
                "Категория должна соответствовать выбранному типу операции"
            )

        # Проверка соответствия подкатегории категории
        if self.subcategory.category != self.category:
            raise models.ValidationError(
                "Подкатегория должна соответствовать выбранной категории"
            )
