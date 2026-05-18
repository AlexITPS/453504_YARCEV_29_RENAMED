from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MasterProfile

class MasterProfileInline(admin.StackedInline):
    model = MasterProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (MasterProfileInline,)
    list_display = ('username', 'email', 'is_master', 'is_client', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('phone', 'birth_date', 'is_master', 'is_client')}),
    )

admin.site.register(User, CustomUserAdmin)