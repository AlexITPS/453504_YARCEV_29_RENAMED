from django.contrib.auth.models import AbstractUser # type: ignore
from django.db import models # type: ignore
from django.core.validators import RegexValidator # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from datetime import date

def validate_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("Регистрация доступна только лицам старше 18 лет.")

class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+375 \((25|29|33|44)\) \d{3}-\d{2}-\d{2}$',
        message="Формат телефона: +375 (29) XXX-XX-XX"
    )
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    birth_date = models.DateField(validators=[validate_age], null=True, blank=True)

    is_master = models.BooleanField(default=False, verbose_name="Мастер")
    is_client = models.BooleanField(default=True, verbose_name="Клиент") # ВЕРНУЛИ ЭТО ПОЛЕ

class MasterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='master_profile')
    bio = models.TextField(verbose_name="О мастере")
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Профиль мастера: {self.user.username}"