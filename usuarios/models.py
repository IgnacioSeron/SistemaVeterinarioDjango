from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

#Solo deja pasar 9 números de teléfono con un prefijo ya definido +56
telefono_validador = RegexValidator(
    regex=r'^\d{9}$',
    message="El Número Debe Tener 9 Dígitos."
)

#Validador y limpiador de RUT antes de ingresarlo a la DB
def validar_rut(value):
    #Limpieza total
    rut = str(value).replace(".", "").replace("-", "").upper().strip()
    
    #Formato (8 a 9 caracteres)
    if not re.match(r"^\d{7,8}[\dK]$", rut):
        raise ValidationError("Formato de RUT Inválido.")

    #Cálculo del Módulo 11
    cuerpo = rut[:-1]
    dv_ingresado = rut[-1]
    
    suma = 0
    multiplicador = 2
    
    #Recorrer de derecha a izquierda
    for c in reversed(cuerpo):
        suma += int(c) * multiplicador
        if multiplicador == 7:
            multiplicador = 2
        else:
            multiplicador += 1
    
    #Obtener el DV esperado
    resto = suma % 11
    valor_esperado = 11 - resto
    
    if valor_esperado == 11:
        dv_real = '0'
    elif valor_esperado == 10:
        dv_real = 'K'
    else:
        dv_real = str(valor_esperado)

    if dv_ingresado != dv_real:
        raise ValidationError(f"El RUT es Inválido. (Para El Cuerpo {cuerpo}, El DV Debería Ser {dv_real})")

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