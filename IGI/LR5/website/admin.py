# website/admin.py
from django.contrib import admin
from .models import News, FAQ, Vacancy, Review, CompanyInfo, Employee, PromoCode

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at') 
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'text')

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_until', 'is_archived')
    list_filter = ('is_archived', 'valid_until')
    list_editable = ('is_archived',) 
    search_fields = ('code',)

admin.site.register(FAQ)
admin.site.register(Vacancy)
admin.site.register(CompanyInfo)
admin.site.register(Employee)