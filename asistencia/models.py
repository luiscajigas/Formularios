from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
import uuid

from .managers import AsistenciaManager
from . import validators


class Asistencia(models.Model):
	"""
	Modelo para registrar la asistencia de personas
	Implementa validaciones robustas y métodos de utilidad
	"""

	# Campos principales
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False,
		help_text="Identificador único del registro"
	)

	nombre_completo = models.CharField(
		max_length=150,
		verbose_name="Nombre Completo",
		help_text="Nombre completo de la persona",
		db_index=True  # Índice para búsquedas
	)

	documento_identidad = models.CharField(
		max_length=20,
		verbose_name="Documento de Identidad",
		help_text="Número de documento de identidad",
		db_index=True
	)

	correo_electronico = models.EmailField(
		verbose_name="Correo Electrónico",
		help_text="Dirección de correo electrónico válida"
	)

	# Campos de fecha y hora
	fecha_asistencia = models.DateField(
		default=timezone.now,
		verbose_name="Fecha de Asistencia",
		help_text="Fecha del registro de asistencia",
		db_index=True
	)

	hora_ingreso = models.TimeField(
		verbose_name="Hora de Ingreso",
		help_text="Hora de entrada"
	)

	hora_salida = models.TimeField(
		verbose_name="Hora de Salida",
		help_text="Hora de salida"
	)

	# Campo booleano
	presente = models.BooleanField(
		default=True,
		verbose_name="Presente",
		help_text="Indica si la persona estuvo presente"
	)

	# Campo opcional
	observaciones = models.TextField(
		blank=True,
		null=True,
		verbose_name="Observaciones",
		help_text="Observaciones adicionales (opcional)",
		max_length=500
	)

	# Campos de auditoría
	fecha_creacion = models.DateTimeField(
		auto_now_add=True,
		verbose_name="Fecha de Creación"
	)

	fecha_actualizacion = models.DateTimeField(
		auto_now=True,
		verbose_name="Última Actualización"
	)

	# Manager personalizado
	objects = AsistenciaManager()

	class Meta:
		verbose_name = "Asistencia"
		verbose_name_plural = "Asistencias"
		ordering = ['-fecha_asistencia', '-hora_ingreso']
		indexes = [
			models.Index(fields=['fecha_asistencia', 'presente']),
			models.Index(fields=['documento_identidad']),
			models.Index(fields=['fecha_creacion']),
		]
		unique_together = [
			('documento_identidad', 'fecha_asistencia')
		]

	def clean(self):
		"""
		Validaciones a nivel de modelo
		"""
		errors = {}

		# Validar que la fecha no sea futura
		if self.fecha_asistencia and self.fecha_asistencia > timezone.now().date():
			errors['fecha_asistencia'] = "La fecha de asistencia no puede ser futura."

		# Validar que hora_salida sea posterior a hora_ingreso
		if self.hora_ingreso and self.hora_salida:
			if self.hora_salida <= self.hora_ingreso:
				errors['hora_salida'] = "La hora de salida debe ser posterior a la hora de ingreso."

		# Validar documento de identidad (solo números)
		if self.documento_identidad:
			if not self.documento_identidad.isdigit():
				errors['documento_identidad'] = "El documento debe contener solo números."
			elif len(self.documento_identidad) < 6:
				errors['documento_identidad'] = "El documento debe tener al menos 6 dígitos."

		# Validar nombre completo
		if self.nombre_completo:
			if len(self.nombre_completo.strip()) < 2:
				errors['nombre_completo'] = "El nombre debe tener al menos 2 caracteres."

			# Verificar que contenga al menos dos palabras
			palabras = self.nombre_completo.strip().split()
			if len(palabras) < 2:
				errors['nombre_completo'] = "Debe ingresar nombre y apellido."

		if errors:
			raise ValidationError(errors)

	def save(self, *args, **kwargs):
		"""
		Override del método save para ejecutar validaciones
		"""
		# Normalizar datos
		if self.nombre_completo:
			self.nombre_completo = self.nombre_completo.strip().title()

		if self.documento_identidad:
			self.documento_identidad = self.documento_identidad.strip()

		if self.correo_electronico:
			self.correo_electronico = self.correo_electronico.lower().strip()

		# Ejecutar validaciones
		self.full_clean()

		super().save(*args, **kwargs)

	def __str__(self):
		"""
		Representación string del objeto
		"""
		estado = "Presente" if self.presente else "Ausente"
		return f"{self.nombre_completo} - {self.fecha_asistencia} ({estado})"

	def get_absolute_url(self):
		"""
		URL canónica del objeto
		"""
		return reverse('asistencia:detail', kwargs={'pk': self.pk})

	@property
	def duracion_asistencia(self):
		"""
		Calcula la duración de la asistencia en horas
		"""
		if self.hora_ingreso and self.hora_salida:
			# Convertir a datetime para calcular diferencia
			ingreso = datetime.combine(self.fecha_asistencia, self.hora_ingreso)
			salida = datetime.combine(self.fecha_asistencia, self.hora_salida)

			# Si la salida es al día siguiente
			if self.hora_salida < self.hora_ingreso:
				salida = datetime.combine(
					self.fecha_asistencia + timezone.timedelta(days=1),
					self.hora_salida
				)

			duracion = salida - ingreso
			return duracion.total_seconds() / 3600  # Retorna en horas
		return None

	@property
	def es_asistencia_completa(self):
		"""
		Determina si es una asistencia completa (más de 4 horas)
		"""
		duracion = self.duracion_asistencia
		return duracion and duracion >= 4

	def get_estado_display(self):
		"""
		Retorna el estado de asistencia con formato
		"""
		if self.presente:
			return "✅ Presente"
		return "❌ Ausente"

	def get_duracion_display(self):
		"""
		Retorna la duración formateada
		"""
		duracion = self.duracion_asistencia
		if duracion:
			horas = int(duracion)
			minutos = int((duracion - horas) * 60)
			return f"{horas}h {minutos}m"
		return "No disponible"
