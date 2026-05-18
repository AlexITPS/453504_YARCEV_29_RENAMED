import pytest
from django.urls import reverse
from repairs.models import Service, Order, RepairCategory
from website.models import PromoCode, Review
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()

@pytest.mark.django_db
class TestRepairsLogic:
    """Тестируем логику заказов и моделей"""
    
    def test_order_total_price_with_promo(self):
        cat = RepairCategory.objects.create(name="Обувь")
        service = Service.objects.create(name="Набойки", price=100, category=cat)
        client = User.objects.create_user(username="test_client", is_client=True)
        promo = PromoCode.objects.create(code="DISCOUNT10", discount_percent=10, valid_until=date.today() + timedelta(days=1))
        
        order = Order.objects.create(client=client, service=service, applied_promo=promo)
        
        assert order.total_price == 90

@pytest.mark.django_db
class TestWebsiteViews:
    """Тестируем доступность страниц и CRUD"""

    def test_home_page_accessible(self, client):
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200

    def test_service_list_filter(self, client):
        cat = RepairCategory.objects.create(name="Одежда")
        Service.objects.create(name="Молния", price=20, category=cat)
        
        url = reverse('service_list')
        response = client.get(url, {'q': 'Молния'})
        assert response.status_code == 200
        assert "Молния" in response.content.decode()

    def test_delete_review_permission(self, client):
        user1 = User.objects.create_user(username="owner", password="pass", is_client=True)
        user2 = User.objects.create_user(username="stranger", password="pass", is_client=True)
        cat = RepairCategory.objects.create(name="Тест")
        service = Service.objects.create(name="Услуга", price=10, category=cat)
        review = Review.objects.create(user=user1, service=service, rating=5, text="Супер")
        
        client.login(username="stranger", password="pass")
        url = reverse('delete_review', args=[review.id])
        response = client.get(url)
        
        assert response.status_code == 404
        assert Review.objects.count() == 1 

@pytest.mark.django_db
class TestUserValidation:
    """Тестируем валидацию пользователей"""
    
    def test_age_restriction(self):
        underage_date = date.today() - timedelta(days=365 * 10) 
        user = User(username="kid", birth_date=underage_date)
        
        from django.core.exceptions import ValidationError
        with pytest.raises(ValidationError):
            user.full_clean() 