from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

#Solo deja pasar 9 números de teléfono con un prefijo ya definido +56
telefono_validador = RegexValidator(
    regex=r'^\d{9}$',
    message="El Número Debe Tener Exactamente 9 Dígitos."
)

#Validador y limpiador de RUT antes de ingresarlo a la DB
def validar_rut(value):
    #Limpiar el RUT de puntos y guiones
    rut = value.replace(".", "").replace("-", "").upper()
    
    #Validar formato básico (7 a 8 dígitos + dígito verificador)
    if not re.match(r"^\d{7,8}[\dK]$", rut):
        raise ValidationError("Formato de RUT Inválido.")

    #Algoritmo Módulo 11 
    cuerpo = rut[:-1]
    dv = rut[-1]
    
    suma = 0
    multiplicador = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador > 7 else 2
    
    dv_esperado = 11 - (suma % 11)
    if dv_esperado == 11: dv_esperado = '0'
    elif dv_esperado == 10: dv_esperado = 'K'
    else: dv_esperado = str(dv_esperado)

    if dv != dv_esperado:
        raise ValidationError("El RUT Es Inválido ")

# Create your models here.
class Usuario(AbstractUser):
    ADMIN = 'admin'
    VETERINARIO = 'vet'
    SECRETARIA = 'sec'
    CLIENTE = 'cli'

    ROLES_CHOICES = [
        (ADMIN, 'Administrador'),
        (VETERINARIO, 'Veterinario'),
        (SECRETARIA, 'Secretaria'),
        (CLIENTE, 'Cliente')
    ]

    rol = models.CharField(max_length=10,choices=ROLES_CHOICES,default=CLIENTE,)

    celular = models.CharField(
        validators=[telefono_validador], max_length=9, blank=True, null=True)
    
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True, validators=[validar_rut], verbose_name="RUT")

    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")

    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"