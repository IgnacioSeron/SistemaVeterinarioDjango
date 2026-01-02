from django.db import models
from django.conf import settings

# Create your models here.
class Mascota(models.Model):
    PERRO = 'perro'
    GATO = 'gato'
    AVE = 'ave'
    EXOTICO = 'exotico'
    OTRO = 'otro'

    ESPECIES_CHOICES = [
        (PERRO, 'Perro'),
        (GATO, 'Gato'),
        (AVE, 'Ave'),
        (EXOTICO, 'Exótico'),
        (OTRO, 'Otro')
    ]

    nombre = models.CharField(max_length=50)
    especie = models.CharField(max_length=10, choices=ESPECIES_CHOICES)
    raza = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text='Peso en Kg')

    dueño = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name= 'mascotas'
    )

    def __str__(self):
        return f"{self.nombre} ({self.especie}) - Dueño: {self.dueño.username}"