from django.contrib import admin
from .models import Mascota

# Register your models here.
@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'dueño')
    search_fields = ('nombre', 'dueño__username', 'dueño__rut')