from django import forms
from django.core.exceptions import ValidationError
from .models import Solicitud
import re

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'nombre_solicitante',
            'documento_identidad', 
            'correo_electronico',
            'telefono_contacto',
            'tipo_solicitud',
            'asunto',
            'descripcion_detallada',
            'archivo_adjunto'
        ]
        
        widgets = {
            'nombre_solicitante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Juan Pérez García'
            }),
            'documento_identidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1234567890'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'telefono_contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 3001234567'
            }),
            'tipo_solicitud': forms.Select(attrs={
                'class': 'form-select'
            }),
            'asunto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Resuma brevemente su solicitud'
            }),
            'descripcion_detallada': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describa detalladamente su solicitud...'
            }),
            'archivo_adjunto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            })
        }
    
    def clean_nombre_solicitante(self):
        nombre = self.cleaned_data.get('nombre_solicitante')
        if nombre:
            # Validar que contenga al menos dos palabras
            palabras = nombre.strip().split()
            if len(palabras) < 2:
                raise ValidationError('Debe ingresar al menos nombres y apellidos.')
            
            # Validar que solo contenga letras y espacios
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
                raise ValidationError('El nombre solo debe contener letras y espacios.')
        
        return nombre
    
    def clean_documento_identidad(self):
        documento = self.cleaned_data.get('documento_identidad')
        if documento:
            # Validar que sea solo números
            if not documento.isdigit():
                raise ValidationError('El documento debe contener solo números.')
            
            if len(documento) < 6 or len(documento) > 20:
                raise ValidationError('El documento debe tener entre 6 y 20 dígitos.')
        
        return documento
    
    def clean_telefono_contacto(self):
        telefono = self.cleaned_data.get('telefono_contacto')
        if telefono:
            # Remover espacios y caracteres especiales
            telefono_limpio = re.sub(r'[^\d]', '', telefono)
            
            # Validar longitud
            if len(telefono_limpio) < 7 or len(telefono_limpio) > 15:
                raise ValidationError('El teléfono debe tener entre 7 y 15 dígitos.')
            
            return telefono_limpio
        
        return telefono
    
    def clean_asunto(self):
        asunto = self.cleaned_data.get('asunto')
        if asunto:
            asunto = asunto.strip()
            if len(asunto) < 5:
                raise ValidationError('El asunto debe tener al menos 5 caracteres.')
            if len(asunto) > 200:
                raise ValidationError('El asunto no puede exceder 200 caracteres.')
        
        return asunto
    
    def clean_descripcion_detallada(self):
        descripcion = self.cleaned_data.get('descripcion_detallada')
        if descripcion:
            descripcion = descripcion.strip()
            if len(descripcion) < 20:
                raise ValidationError('La descripción debe tener al menos 20 caracteres.')
        
        return descripcion
    
    def clean_archivo_adjunto(self):
        archivo = self.cleaned_data.get('archivo_adjunto')
        if archivo:
            # Validar tamaño (5MB máximo)
            if archivo.size > 5 * 1024 * 1024:
                raise ValidationError('El archivo no puede exceder 5MB.')
            
            # Validar extensión
            nombre_archivo = archivo.name.lower()
            extensiones_permitidas = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png']
            
            if not any(nombre_archivo.endswith(ext) for ext in extensiones_permitidas):
                raise ValidationError(
                    'Tipo de archivo no permitido. Use: PDF, DOC, DOCX, JPG, JPEG, PNG'
                )
        
        return archivo
