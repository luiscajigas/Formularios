from django.contrib import admin
from .models import Solicitud
@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = [
        'nombre_solicitante',
        'documento_identidad', 
        'tipo_solicitud',
        'asunto',
        'fecha_solicitud',
        'correo_electronico'
    ]
    
    list_filter = [
        'tipo_solicitud',
        'fecha_solicitud',
        'fecha_creacion'
    ]
    
    search_fields = [
        'nombre_solicitante',
        'documento_identidad',
        'correo_electronico',
        'asunto'
    ]
    
    readonly_fields = [
        'fecha_solicitud',
        'fecha_creacion', 
        'fecha_actualizacion'
    ]
    
    fieldsets = (
        ('Información Personal', {
            'fields': (
                'nombre_solicitante',
                'documento_identidad',
                'correo_electronico',
                'telefono_contacto'
            )
        }),
        ('Detalles de la Solicitud', {
            'fields': (
                'tipo_solicitud',
                'asunto',
                'descripcion_detallada',
                'archivo_adjunto'
            )
        }),
        ('Fechas', {
            'fields': (
                'fecha_solicitud',
                'fecha_creacion',
                'fecha_actualizacion'
            )
        }),
    )
    
    ordering = ['-fecha_solicitud']
    date_hierarchy = 'fecha_solicitud'