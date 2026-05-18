from django.contrib import admin # type: ignore
from .models import RepairCategory, Service, SparePart, Order

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'service', 'get_total_price', 'created_at')
    filter_horizontal = ('spare_parts',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('spare_parts', 'service')

    def get_total_price(self, obj):
        return f"{obj.total_price} руб."
    get_total_price.short_description = 'Итоговая цена'

admin.site.register(RepairCategory)
admin.site.register(SparePart)