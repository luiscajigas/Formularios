import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validar_documento_identidad(value):
    """
    Valida que el documento de identidad tenga el formato correcto
    """
    if not value:
        raise ValidationError(_('Este campo es obligatorio.'))

    documento = str(value).strip()

    if not documento.isdigit():
        raise ValidationError(_('El documento de identidad debe contener solo números.'))

    if len(documento) < 6:
        raise ValidationError(_('El documento debe tener al menos 6 dígitos.'))

    if len(documento) > 20:
        raise ValidationError(_('El documento no puede tener más de 20 dígitos.'))

    if documento == '0' * len(documento):
        raise ValidationError(_('El documento no puede ser solo ceros.'))


def validar_nombre_completo(value):
    if not value:
        raise ValidationError(_('Este campo es obligatorio.'))

    nombre = str(value).strip()

    if len(nombre) < 2:
        raise ValidationError(_('El nombre debe tener al menos 2 caracteres.'))

    if len(nombre) > 150:
        raise ValidationError(_('El nombre no puede exceder los 150 caracteres.'))

    patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\.\']+$'
    if not re.match(patron, nombre):
        raise ValidationError(_('El nombre solo puede contener letras, espacios, puntos y apostrofes.'))

    palabras = nombre.split()
    if len(palabras) < 2:
        raise ValidationError(_('Debe ingresar al menos nombre y apellido.'))

    for palabra in palabras:
        if len(palabra.strip()) < 2:
            raise ValidationError(_('Cada palabra del nombre debe tener al menos 2 caracteres.'))

    if len(palabras) > 5:
        raise ValidationError(_('El nombre no puede tener más de 5 palabras.'))


def validar_correo_colombiano(value):
    if not value:
        return

    dominios_permitidos = [
        'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com',
        'udenar.edu.co', 'unicauca.edu.co', 'unal.edu.co',
        'upb.edu.co', 'javeriana.edu.co', 'unisabana.edu.co'
    ]

    correo = str(value).lower().strip()
    dominio = correo.split('@')[-1] if '@' in correo else ''

    # Validación opcional (desactivada por defecto)
    # if dominio and dominio not in dominios_permitidos:
    #     raise ValidationError(_('Por favor use un correo con dominio válido.'))


def validar_telefono_colombiano(value):
    if not value:
        return

    telefono = re.sub(r'[^\d]', '', str(value))

    if len(telefono) < 7:
        raise ValidationError(_('El número de teléfono debe tener al menos 7 dígitos.'))

    if len(telefono) > 10:
        raise ValidationError(_('El número de teléfono no puede tener más de 10 dígitos.'))

    if len(telefono) == 10 and not telefono.startswith('3'):
        raise ValidationError(_('Los números de celular deben iniciar con 3.'))


def validar_rango_horas(hora_inicio, hora_fin):
    if not hora_inicio or not hora_fin:
        return

    if hora_fin <= hora_inicio:
        raise ValidationError(_('La hora de salida debe ser posterior a la hora de ingreso.'))

    from datetime import datetime, date
    inicio_dt = datetime.combine(date.today(), hora_inicio)
    fin_dt = datetime.combine(date.today(), hora_fin)
    diferencia = fin_dt - inicio_dt

    if diferencia.total_seconds() > 12 * 3600:
        raise ValidationError(_('La diferencia entre ingreso y salida no puede exceder 12 horas.'))

    if diferencia.total_seconds() < 30 * 60:
        raise ValidationError(_('La diferencia mínima entre ingreso y salida debe ser 30 minutos.'))


class ValidadorPersonalizado:
    def __init__(self, mensaje=None):
        self.mensaje = mensaje

    def __call__(self, value):
        self.validar(value)

    def validar(self, value):
        raise NotImplementedError("Debe implementar el método validar")


class ValidadorDocumentoUnico(ValidadorPersonalizado):
    def __init__(self, modelo, campo_fecha='fecha_asistencia', mensaje=None):
        self.modelo = modelo
        self.campo_fecha = campo_fecha
        super().__init__(mensaje or _('Ya existe un registro con este documento para esta fecha.'))

    def validar(self, value):
        # Esta validación se maneja mejor en el formulario
        pass


class ValidadorLongitudTexto(ValidadorPersonalizado):
    def __init__(self, min_length=0, max_length=None, mensaje=None):
        self.min_length = min_length
        self.max_length = max_length
        super().__init__(mensaje)

    def validar(self, value):
        if not value:
            return

        texto = str(value).strip()
        longitud = len(texto)

        if longitud < self.min_length:
            raise ValidationError(self.mensaje or _(f'El texto debe tener al menos {self.min_length} caracteres.'))

        if self.max_length and longitud > self.max_length:
            raise ValidationError(self.mensaje or _(f'El texto no puede exceder {self.max_length} caracteres.'))
