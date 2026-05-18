# analytics/views.py
import statistics
import io
import base64
from datetime import date

import matplotlib
matplotlib.use('Agg') 
from matplotlib.figure import Figure

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from repairs.models import RepairCategory, Order, Service
from users.models import User

def get_graph(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    return graph

def stats_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "У вас нет прав для просмотра этого раздела.")
        return redirect('home')

    orders_done = Order.objects.filter(status='done').select_related('service', 'applied_promo')
    total_sales = sum(order.total_price for order in orders_done)

    prices = [float(order.total_price) for order in orders_done]
    stats_sales = {
        'avg': round(statistics.mean(prices), 2) if prices else 0,
        'median': round(statistics.median(prices), 2) if prices else 0,
        'mode': statistics.mode(prices) if prices else 0
    }

    today = date.today()
    ages = []
    clients = User.objects.filter(is_client=True, birth_date__isnull=False)
    for client in clients:
        age = today.year - client.birth_date.year - ((today.month, today.day) < (client.birth_date.month, client.birth_date.day))
        ages.append(age)
    
    stats_ages = {
        'avg': round(statistics.mean(ages), 1) if ages else 0,
        'median': statistics.median(ages) if ages else 0
    }

    popular_service = Service.objects.annotate(num_orders=Count('order')).order_by('-num_orders').first()

    categories = RepairCategory.objects.all()
    categories_stats = []
    max_profit = 0
    best_category_name = "Нет данных"

    for cat in categories:
        cat_orders = orders_done.filter(service__category=cat)
        cat_earned = sum(order.total_price for order in cat_orders)
        
        if cat_earned > max_profit:
            max_profit = cat_earned
            best_category_name = cat.name

        categories_stats.append({
            'name': cat.name,
            'total_services': cat.service_set.count(),
            'total_orders': cat_orders.count(),
            'earned_money': cat_earned
        })

    categories_stats = sorted(categories_stats, key=lambda x: x['earned_money'], reverse=True)

    context = {
        'total_sales': total_sales,
        'stats_sales': stats_sales,
        'stats_ages': stats_ages,
        'popular_service': popular_service,
        'category_profit': {'service__category__name': best_category_name, 'total': max_profit},
        'categories_stats': categories_stats,
    }
    return render(request, 'analytics/stats.html', context)

# Графики
def stats_charts_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "У вас нет прав для просмотра этого раздела.")
        return redirect('home')

    orders_done = Order.objects.filter(status='done').select_related('service', 'applied_promo')
    categories = RepairCategory.objects.all()
    
    labels = []
    values_orders = []
    values_money = []

    for cat in categories:
        cat_orders = orders_done.filter(service__category=cat)
        count = cat_orders.count()
        if count > 0:
            labels.append(cat.name)
            values_orders.append(count)
            values_money.append(float(sum(order.total_price for order in cat_orders)))

    chart_pie = None
    chart_bar = None
    
    if labels:
        fig_pie = Figure(figsize=(5, 3.5))
        ax_pie = fig_pie.subplots()
        ax_pie.pie(values_orders, labels=labels, autopct='%1.1f%%', startangle=140, 
                   colors=['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e'])
        ax_pie.set_title('Распределение заказов по категориям', fontsize=11, fontweight='bold')
        chart_pie = get_graph(fig_pie)

        # Столбчатая
        fig_bar = Figure(figsize=(5, 3.5))
        ax_bar = fig_bar.subplots()
        ax_bar.bar(labels, values_money, color='#4e73df')
        ax_bar.set_title('Реальная выручка по категориям (руб.)', fontsize=11, fontweight='bold')
        ax_bar.set_ylabel('Сумма со скидками')
        ax_bar.set_xticklabels(labels, rotation=15, ha='right')
        chart_bar = get_graph(fig_bar)

    context = {
        'chart_pie': chart_pie,
        'chart_bar': chart_bar,
    }
    return render(request, 'analytics/stats_charts.html', context)