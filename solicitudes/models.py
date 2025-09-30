from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import os

def validar_tamaño_archivo(value):
    """Valida que el archivo no exceda 5MB"""
    limit = 5 * 1024 * 1024  # 5MB
    if value.size > limit:
        raise ValidationError('El archivo no puede exceder 5MB.')

def upload_to_solicitudes(instance, filename):
    return f'solicitudes/{instance.documento_identidad}/{filename}'

class Solicitud(models.Model):
    TIPO_SOLICITUD_CHOICES = [
        ('academica', 'Académica'),
        ('administrativa', 'Administrativa'), 
        ('tecnica', 'Técnica'),
        ('otra', 'Otra'),
    ]
    
    nombre_solicitante = models.CharField(
        max_length=150,
        verbose_name="Nombre completo del solicitante",
        help_text="Ingrese el nombre completo"
    )
    
    documento_identidad = models.CharField(
        max_length=20,
        verbose_name="Documento de identidad",
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='El documento de identidad debe contener solo números.'
            )
        ],
        help_text="Ingrese solo números"
    )
    
    correo_electronico = models.EmailField(
        verbose_name="Correo electrónico",
        help_text="Ingrese un correo electrónico válido"
    )
    
    telefono_contacto = models.CharField(
        max_length=15,
        verbose_name="Teléfono de contacto",
        validators=[
            RegexValidator(
                regex=r'^\d{7,15}$',
                message='El teléfono debe contener entre 7 y 15 números.'
            )
        ],
        help_text="Ingrese solo números (7-15 dígitos)"
    )
    
    tipo_solicitud = models.CharField(
        max_length=20,
        choices=TIPO_SOLICITUD_CHOICES,
        verbose_name="Tipo de solicitud",
        help_text="Seleccione el tipo de solicitud"
    )
    
    asunto = models.CharField(
        max_length=200,
        verbose_name="Asunto",
        help_text="Resuma brevemente el asunto de su solicitud"
    )
    
    descripcion_detallada = models.TextField(
        verbose_name="Descripción detallada",
        help_text="Proporcione una descripción completa de su solicitud"
    )
    
    fecha_solicitud = models.DateField(
        verbose_name="Fecha de solicitud",
        auto_now_add=True,
        help_text="Fecha en que se realiza la solicitud"
    )
    
    archivo_adjunto = models.FileField(
        upload_to=upload_to_solicitudes,
        blank=True,
        null=True,
        verbose_name="Archivo adjunto",
        validators=[validar_tamaño_archivo],
        help_text="Archivo opcional (máximo 5MB)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        ordering = ['-fecha_solicitud']
        
    def __str__(self):
        return f"{self.nombre_solicitante} - {self.asunto} ({self.get_tipo_solicitud_display()})"
    
    def clean(self):
        """Validaciones adicionales del modelo"""
        super().clean()
        
        # Validar que el asunto no esté vacío después de limpiar espacios
        if self.asunto and not self.asunto.strip():
            raise ValidationError({'asunto': 'El asunto no puede estar vacío.'})
            
        # Validar que la descripción tenga al menos 10 caracteres
        if self.descripcion_detallada and len(self.descripcion_detallada.strip()) < 10:
            raise ValidationError({
                'descripcion_detallada': 'La descripción debe tener al menos 10 caracteres.'
            })