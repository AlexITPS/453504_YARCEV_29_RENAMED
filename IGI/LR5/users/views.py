from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from repairs.models import Order

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.is_client = True  
            user = form.save()
            login(request, user) 
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    context = {'role_title': ""}
    
    if user.is_superuser:
        context['role_title'] = "Главный Администратор"
        context['orders'] = Order.objects.all().select_related('client', 'service')
    elif user.is_master:
        context['role_title'] = "Мастер"
        # Мастер видит только те заказы, где он назначен
        context['orders'] = user.master_orders.all().select_related('client', 'service')
    else:
        context['role_title'] = "Клиент"
        # Клиент видит только свои покупки
        context['orders'] = user.client_orders.all().select_related('service')
        
    return render(request, 'registration/profile.html', context)