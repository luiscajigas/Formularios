from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Q
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse
import csv
from datetime import datetime

from .models import Asistencia


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
	"""
	Configuración personalizada para el modelo Asistencia en el admin
	"""
    
	list_display = [
		'nombre_completo',
		'documento_identidad', 
		'fecha_asistencia',
		'hora_ingreso',
		'hora_salida',
		'estado_presente',
		'duracion_display',
		'fecha_creacion'
	]
    
	list_filter = [
		'presente',
		'fecha_asistencia',
		'fecha_creacion',
		('fecha_asistencia', admin.DateFieldListFilter),
	]
    
	search_fields = [
		'nombre_completo',
		'documento_identidad',
		'correo_electronico'
	]
    
	ordering = ['-fecha_asistencia', '-hora_ingreso']
    
	readonly_fields = [
		'id',
		'fecha_creacion',
		'fecha_actualizacion',
		'duracion_display',
		'es_asistencia_completa'
	]

	fieldsets = (
		('Información Personal', {
			'fields': (
				'nombre_completo',
				'documento_identidad',
				'correo_electronico'
			),
			'classes': ('wide',)
		}),
		('Información de Asistencia', {
			'fields': (
				'fecha_asistencia',
				'hora_ingreso',
				'hora_salida',
				'presente'
			),
			'classes': ('wide',)
		}),
		('Observaciones', {
			'fields': ('observaciones',),
			'classes': ('collapse',)
		}),
		('Información del Sistema', {
			'fields': (
				'id',
				'fecha_creacion',
				'fecha_actualizacion',
				'duracion_display',
				'es_asistencia_completa'
			),
			'classes': ('collapse',)
		})
	)
    
	list_per_page = 25
	list_max_show_all = 100
    
	date_hierarchy = 'fecha_asistencia'
    
	actions = [
		'marcar_presente',
		'marcar_ausente',
		'exportar_seleccionados_csv',
		'duplicar_registros'
	]
    
	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path(
				'estadisticas/',
				self.admin_site.admin_view(self.estadisticas_view),
				name='asistencia_estadisticas'
			),
			path(
				'reporte-mensual/',
				self.admin_site.admin_view(self.reporte_mensual_view),
				name='asistencia_reporte_mensual'
			),
		]
		return custom_urls + urls
    
	def estado_presente(self, obj):
		if obj.presente:
			return format_html(
				'<span style="color: green; font-weight: bold;">✅ Presente</span>'
			)
		return format_html(
			'<span style="color: red; font-weight: bold;">❌ Ausente</span>'
		)
	estado_presente.short_description = 'Estado'
	estado_presente.admin_order_field = 'presente'
    
	def duracion_display(self, obj):
		duracion = obj.get_duracion_display()
		if obj.duracion_asistencia and obj.duracion_asistencia >= 4:
			return format_html(
				'<span style="color: green; font-weight: bold;">{}</span>',
				duracion
			)
		elif obj.duracion_asistencia and obj.duracion_asistencia < 4:
			return format_html(
				'<span style="color: orange;">{}</span>',
				duracion
			)
		return duracion
	duracion_display.short_description = 'Duración'
    
	def marcar_presente(self, request, queryset):
		updated = queryset.update(presente=True)
		self.message_user(
			request,
			f'{updated} registro(s) marcado(s) como presente.'
		)
	marcar_presente.short_description = "Marcar seleccionados como presente"
    
	def marcar_ausente(self, request, queryset):
		updated = queryset.update(presente=False)
		self.message_user(
			request,
			f'{updated} registro(s) marcado(s) como ausente.'
		)
	marcar_ausente.short_description = "Marcar seleccionados como ausente"
    
	def exportar_seleccionados_csv(self, request, queryset):
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="asistencias_seleccionadas.csv"'
        
		writer = csv.writer(response)
		writer.writerow([
			'ID', 'Nombre Completo', 'Documento', 'Correo', 'Fecha',
			'Hora Ingreso', 'Hora Salida', 'Presente', 'Duración', 'Observaciones'
		])
        
		for obj in queryset:
			writer.writerow([
				str(obj.id),
				obj.nombre_completo,
				obj.documento_identidad,
				obj.correo_electronico,
				obj.fecha_asistencia.strftime('%d/%m/%Y'),
				obj.hora_ingreso.strftime('%H:%M'),
				obj.hora_salida.strftime('%H:%M'),
				'Sí' if obj.presente else 'No',
				obj.get_duracion_display(),
				obj.observaciones or ''
			])
        
		self.message_user(
			request,
			f'{queryset.count()} registro(s) exportado(s) a CSV.'
		)
		return response
	exportar_seleccionados_csv.short_description = "Exportar seleccionados a CSV"
    
	def duplicar_registros(self, request, queryset):
		duplicados = 0
		for obj in queryset:
			obj.pk = None  # Crear nuevo objeto
			obj.id = None
			obj.fecha_asistencia = datetime.now().date()
			obj.save()
			duplicados += 1
        
		self.message_user(
			request,
			f'{duplicados} registro(s) duplicado(s) para hoy.'
		)
	duplicar_registros.short_description = "Duplicar seleccionados para hoy"
    
	def estadisticas_view(self, request):
		total_registros = Asistencia.objects.count()
		total_presentes = Asistencia.objects.filter(presente=True).count()
		total_ausentes = Asistencia.objects.filter(presente=False).count()
        
		stats_mes = Asistencia.objects.estadisticas_mes_actual()
        
		personas_activas = Asistencia.objects.values('nombre_completo', 'documento_identidad')\
			.annotate(total=Count('id'), presentes=Count('id', filter=Q(presente=True)))\
			.order_by('-total')[:10]
        
		context = {
			'title': 'Estadísticas de Asistencia',
			'total_registros': total_registros,
			'total_presentes': total_presentes,
			'total_ausentes': total_ausentes,
			'porcentaje_asistencia': round((total_presentes / total_registros * 100), 2) if total_registros > 0 else 0,
			'stats_mes': stats_mes,
			'personas_activas': personas_activas,
			'opts': self.model._meta,
		}
        
		return render(request, 'admin/asistencia_estadisticas.html', context)
    
	def reporte_mensual_view(self, request):
		from django.db.models import Count
		from datetime import datetime, timedelta
        
		today = datetime.now().date()
		primer_dia = today.replace(day=1)
        
		registros_mes = Asistencia.objects.filter(
			fecha_asistencia__gte=primer_dia,
			fecha_asistencia__lte=today
		)
        
		stats_diarios = registros_mes.values('fecha_asistencia')\
			.annotate(
				total=Count('id'),
				presentes=Count('id', filter=Q(presente=True)),
				ausentes=Count('id', filter=Q(presente=False))
			).order_by('fecha_asistencia')
        
		context = {
			'title': f'Reporte Mensual - {today.strftime("%B %Y")}',
			'mes': today.strftime("%B %Y"),
			'total_registros': registros_mes.count(),
			'total_presentes': registros_mes.filter(presente=True).count(),
			'total_ausentes': registros_mes.filter(presente=False).count(),
			'stats_diarios': stats_diarios,
			'opts': self.model._meta,
		}
        
		return render(request, 'admin/asistencia_reporte_mensual.html', context)
    
	def get_queryset(self, request):
		queryset = super().get_queryset(request)
		return queryset.select_related()
    
	def changelist_view(self, request, extra_context=None):
		extra_context = extra_context or {}
        
		extra_context['stats_rapidas'] = {
			'total_hoy': Asistencia.objects.filter(
				fecha_asistencia=datetime.now().date()
			).count(),
			'presentes_hoy': Asistencia.objects.filter(
				fecha_asistencia=datetime.now().date(),
				presente=True
			).count(),
			'total_mes': Asistencia.objects.filter(
				fecha_asistencia__month=datetime.now().month,
				fecha_asistencia__year=datetime.now().year
			).count()
		}
        
		return super().changelist_view(request, extra_context=extra_context)
