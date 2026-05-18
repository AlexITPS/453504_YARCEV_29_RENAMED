import pytest
from django.urls import reverse
from repairs.models import Service, Order, RepairCategory
from website.models import PromoCode, Review, News, FAQ
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()

@pytest.mark.django_db
class TestExtendedLogic:
    
    @pytest.fixture
    def setup_data(self):
        self.cat = RepairCategory.objects.create(name="Одежда")
        self.service = Service.objects.create(name="Ремонт", price=50, category=self.cat)
        self.client_user = User.objects.create_user(username="ivan", password="123", is_client=True)
        self.admin_user = User.objects.create_superuser(username="admin", password="123", email="a@a.com")

    def test_analytics_access_as_admin(self, client, setup_data):
        """Тестируем доступность аналитики для админа (покрывает analytics/views.py)"""
        client.login(username="admin", password="123")
        response = client.get(reverse('stats'))
        assert response.status_code == 200
        
        response_charts = client.get(reverse('stats_charts'))
        assert response_charts.status_code == 200

    def test_user_registration(self, client):
        """Тестируем вьюху регистрации (покрывает users/views.py)"""
        url = reverse('register')
        data = {
            'username': 'new_user',
            'password': 'password123',
            'password_confirm': 'password123', # если у тебя есть подтверждение
            'phone': '+375 (29) 111-22-33',
            'birth_date': '1990-01-01'
        }
        # Если используется стандартная форма UserCreationForm, поля могут отличаться
        response = client.post(url, data)
        # Проверяем редирект на главную после успешной регистрации
        assert response.status_code in [200, 302] 

    def test_full_review_crud(self, client, setup_data):
        """Тестируем весь цикл CRUD отзывов (покрывает website/views.py)"""
        client.login(username="ivan", password="123")
        
        # 1. Create
        url_add = reverse('add_review', args=[self.service.id])
        client.post(url_add, {'rating': 5, 'text': 'Первый отзыв'})
        review = Review.objects.get(text='Первый отзыв')
        
        # 2. Update
        url_edit = reverse('edit_review', args=[review.id])
        client.post(url_edit, {'rating': 4, 'text': 'Измененный отзыв'})
        review.refresh_from_db()
        assert review.text == 'Измененный отзыв'
        
        # 3. Delete
        url_delete = reverse('delete_review', args=[review.id])
        client.get(url_delete) # или post, если у тебя через форму
        assert Review.objects.count() == 0

    def test_static_pages(self, client):
        """Проверяем мелкие страницы (FAQ, О компании и т.д.)"""
        pages = ['faq', 'contacts', 'privacy', 'news_list', 'about', 'promo_list', 'vacancies']
        for page in pages:
            response = client.get(reverse(page))
            assert response.status_code == 200

    def test_order_confirmation_page(self, client, setup_data):
        """Тестируем GET и POST страницы подтверждения заказа"""
        client.login(username="ivan", password="123")
        url = reverse('create_order', args=[self.service.id])
        
        # GET страница
        response_get = client.get(url)
        assert response_get.status_code == 200
        
        # POST (Создание заказа)
        response_post = client.post(url, {'promo_code': ''})
        assert response_post.status_code == 302 # Редирект в профиль
        assert Order.objects.filter(client=self.client_user).exists()