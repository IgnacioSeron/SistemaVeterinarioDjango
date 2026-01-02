from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from gestion.models import Mascota

# Register your models here.
class MascotaInline(admin.TabularInline):
    model = Mascota
    extra = 1

class CustomUserAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información Extra', {'fields': ('rol', 'rut', 'celular', 'direccion')}),
    )
    inlines = [MascotaInline]

admin.site.register(Usuario, CustomUserAdmin)