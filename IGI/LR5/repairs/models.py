from django.db import models # type: ignore
from django.conf import settings # type: ignore

class RepairCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория ремонта"
        verbose_name_plural = "Категории ремонта"
    
    def __str__(self): return self.name

class Service(models.Model):
    category = models.ForeignKey(RepairCategory, on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=150, verbose_name="Название услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
    def __str__(self): return self.name

class SparePart(models.Model):
    name = models.CharField(max_length=100, verbose_name="Запчасть")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"
    
    def __str__(self): return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('process', 'В работе'),
        ('done', 'Выполнен'),
        ('canceled', 'Отменен'),
    ]
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        limit_choices_to={'is_client': True},
        related_name='client_orders', 
        verbose_name="Клиент"
    )
    master = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='master_orders', 
        limit_choices_to={'is_master': True},
        verbose_name="Мастер"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='new', 
        verbose_name="Статус"
    )
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name="Услуга")
    applied_promo = models.ForeignKey('website.PromoCode', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Примененный промокод")
    spare_parts = models.ManyToManyField(SparePart, blank=True, verbose_name="Запчасти")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    @property
    def total_price(self):
        parts_sum = sum(part.price for part in self.spare_parts.all())
        base_price = self.service.price + parts_sum
        
        if self.applied_promo:
            discount = (base_price * self.applied_promo.discount_percent) / 100
            return base_price - discount
            
        return base_price

    def __str__(self):
        return f"Заказ #{self.id} - {self.client.username}"