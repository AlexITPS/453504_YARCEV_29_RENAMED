from django.db import models # type: ignore
from django.conf import settings # type: ignore

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание статьи")
    image = models.ImageField(upload_to='news/', verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Вопрос/Ответ"
        verbose_name_plural = "Вопросы и ответы"

    def __str__(self):
        return self.question

class Vacancy(models.Model):
    title = models.CharField(max_length=100, verbose_name="Вакансия")
    description = models.TextField(verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Клиент")
    service = models.ForeignKey('repairs.Service', on_delete=models.CASCADE, related_name='reviews', verbose_name="Услуга")
    
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")
    text = models.TextField(verbose_name="Отзыв")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at'] 

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.service.name}"

class CompanyInfo(models.Model):
    description = models.TextField(verbose_name="О компании")
    history = models.TextField(verbose_name="История")
    requisites = models.TextField(verbose_name="Реквизиты")
    image = models.ImageField(upload_to='company/', verbose_name="Фото офиса/мастерской", null=True, blank=True)
    
    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"

    def __str__(self):
        return "Конфигурация: О компании"

class Employee(models.Model):
    full_name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='employees/')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
    
    def __str__(self):
        return f"{self.full_name} — {self.position}"

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField()
    valid_until = models.DateField()
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        
    def __str__(self):
        return f"Промокод: {self.code} (-{self.discount_percent}%)"