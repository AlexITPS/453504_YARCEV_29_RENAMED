import calendar  
from django.utils import timezone  
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import logging 
from .models import Review 

from datetime import date

from repairs.models import Service, RepairCategory, Order
from .forms import ReviewForm
from .models import FAQ, Employee, News, CompanyInfo, Vacancy, PromoCode

logger = logging.getLogger('django')

def home(request):
    last_news = News.objects.order_by('-created_at').first()
    featured_services = Service.objects.all()[:4] 

    local_now = timezone.now()
    cal = calendar.TextCalendar(calendar.MONDAY)
    calendar_text = cal.formatmonth(local_now.year, local_now.month)

    context = {
        'last_news': last_news,
        'featured_services': featured_services,
        'main_calendar': calendar_text,
    }
    return render(request, 'index.html', context)

def service_list(request):
    services = Service.objects.all()
    categories = RepairCategory.objects.all()

    query = request.GET.get('q')
    if query:
        services = services.filter(name__icontains=query)

    cat_id = request.GET.get('category')
    if cat_id:
        services = services.filter(category_id=cat_id)

    sort = request.GET.get('sort')
    if sort in ['price_asc', 'cheap']:
        services = services.order_by('price')
    elif sort in ['price_desc', 'expensive']:
        services = services.order_by('-price')
    elif sort == 'name_asc':
        services = services.order_by('name')   
    elif sort == 'name_desc':
        services = services.order_by('-name') 

    return render(request, 'services.html', {
        'services': services,
        'categories': categories,
    })

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    reviews = service.reviews.all() 
    
    can_leave_review = False
    if request.user.is_authenticated and request.user.is_client:
        can_leave_review = Order.objects.filter(
            client=request.user, 
            service=service, 
            status='done'
        ).exists()

    form = ReviewForm()
    
    context = {
        'service': service,
        'reviews': reviews,
        'can_leave_review': can_leave_review,
        'form': form,
    }
    return render(request, 'service_detail.html', context)

def add_review(request, service_id):
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.service = service
            review.save()
            logger.info(f"Пользователь {request.user.username} создал отзыв к услуге {service.name}")
            messages.success(request, "Спасибо за ваш отзыв!")
    return redirect('service_detail', pk=service_id)

def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    service_id = review.service.id
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            logger.info(f"Пользователь {request.user.username} отредактировал отзыв #{pk}")
            messages.success(request, "Отзыв успешно обновлен!")
            return redirect('service_detail', pk=service_id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'website/edit_review.html', {'form': form, 'review': review})

def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    service_id = review.service.id
    review.delete()
    logger.warning(f"Пользователь {request.user.username} удалил отзыв #{pk}")
    messages.success(request, "Отзыв удален.")
    return redirect('service_detail', pk=service_id)

def create_order(request, service_id):
    if not request.user.is_authenticated or not request.user.is_client or request.user.is_superuser or request.user.is_master:
        messages.error(request, "Только клиенты могут оформлять заказы.")
        return redirect('service_list')

    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        promo_code_str = request.POST.get('promo_code', '').strip()
        applied_promo = None

        if promo_code_str:
            promo = PromoCode.objects.filter(
                code=promo_code_str, 
                is_archived=False, 
                valid_until__gte=date.today()
            ).first()

            if promo:
                applied_promo = promo
                messages.success(request, f"Промокод '{promo.code}' применен! Скидка {promo.discount_percent}%")
            else:
                messages.error(request, "Промокод не существует, истек или уже не активен.")
                return render(request, 'website/order_confirm.html', {'service': service})

        new_order = Order.objects.create(
            client=request.user,
            service=service,
            applied_promo=applied_promo,
            status='new'
        )

        logger.info(f"ЗАКАЗ: Пользователь {request.user.username} создал заказ #{new_order.id} на услугу '{service.name}'")
        
        messages.success(request, f"Заказ #{new_order.id} на '{service.name}' успешно оформлен!")
        return redirect('profile')

    return render(request, 'website/order_confirm.html', {'service': service})

def faq_view(request):
    faqs = FAQ.objects.all().order_by('-created_at')
    return render(request, 'website/faq.html', {'faqs': faqs})

def contacts_view(request):
    employees = Employee.objects.all()
    return render(request, 'website/contacts.html', {'employees': employees})

def privacy_view(request):
    return render(request, 'website/privacy.html')

def news_list(request):
    all_news = News.objects.all().order_by('-created_at')
    return render(request, 'website/news_list.html', {'news': all_news})

def about_view(request):
    info = CompanyInfo.objects.first() 
    return render(request, 'website/about.html', {'info': info})

def vacancies_view(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    return render(request, 'website/vacancies.html', {'vacancies': vacancies})

def promo_view(request):
    promos = PromoCode.objects.filter(is_archived=False)
    return render(request, 'website/promos.html', {'promos': promos})

def all_reviews_view(request):
    reviews = Review.objects.all().select_related('user', 'service').order_by('-created_at')
    return render(request, 'website/reviews_all.html', {'reviews': reviews})