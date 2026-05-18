# website/urls.py
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.service_list, name='service_list'),
    path('create-order/<int:service_id>/', views.create_order, name='create_order'), 
    path('service/<int:service_id>/add_review/', views.add_review, name='add_review'),
    re_path(r'^service/(?P<pk>\d+)/$', views.service_detail, name='service_detail'),
    path('faq/', views.faq_view, name='faq'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('news/', views.news_list, name='news_list'),
    path('about/', views.about_view, name='about'),
    path('vacancies/', views.vacancies_view, name='vacancies'),
    path('promos/', views.promo_view, name='promo_list'),
    path('review/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
]