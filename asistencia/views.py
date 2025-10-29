from django.views import generic
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Asistencia
from .forms import AsistenciaForm
from solicitudes.models import Solicitud


class AsistenciaCreateView(generic.CreateView):
	model = Asistencia
	form_class = AsistenciaForm
	template_name = 'asistencia/asistencia_form.html'
	success_url = reverse_lazy('asistencia:list')

	def form_valid(self, form):
		messages.success(self.request, 'Asistencia registrada exitosamente.')
		return super().form_valid(form)


class AsistenciaListView(generic.ListView):
    model = Asistencia
    template_name = 'asistencia/asistencia_list.html'
    paginate_by = 25
    ordering = ['-fecha_creacion']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el queryset
        qs = self.get_queryset()
        
        # Obtener la fecha actual
        hoy = timezone.now().date()
        
        # Calcular inicio y fin de la semana
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        
        # Calcular inicio y fin del mes
        inicio_mes = hoy.replace(day=1)
        if hoy.month == 12:
            fin_mes = hoy.replace(year=hoy.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            fin_mes = hoy.replace(month=hoy.month + 1, day=1) - timedelta(days=1)
        
        # Estadísticas
        context['total_registros'] = qs.count()
        context['presentes_hoy'] = qs.filter(fecha_asistencia=hoy, presente=True).count()
        context['presentes_semana'] = qs.filter(
            fecha_asistencia__range=[inicio_semana, fin_semana],
            presente=True
        ).count()
        context['presentes_mes'] = qs.filter(
            fecha_asistencia__range=[inicio_mes, fin_mes],
            presente=True
        ).count()
        # Añadir estadísticas y últimos registros de solicitudes
        try:
            context['total_solicitudes'] = Solicitud.objects.count()
            context['ultimas_solicitudes'] = Solicitud.objects.all().order_by('-fecha_solicitud')[:5]
        except Exception:
            # Si la app solicitudes no está disponible, garantizar que las claves existan
            context['total_solicitudes'] = 0
            context['ultimas_solicitudes'] = []
        
        return context


class AsistenciaDetailView(generic.DetailView):
	model = Asistencia
	template_name = 'asistencia/asistencia_detail.html'


class AsistenciaUpdateView(generic.UpdateView):
	model = Asistencia
	form_class = AsistenciaForm
	template_name = 'asistencia/asistencia_form.html'
	success_url = reverse_lazy('asistencia:list')

	def form_valid(self, form):
		messages.success(self.request, 'Asistencia actualizada exitosamente.')
		return super().form_valid(form)


class AsistenciaDeleteView(generic.DeleteView):
	model = Asistencia
	template_name = 'asistencia/asistencia_confirm_delete.html'
	success_url = reverse_lazy('asistencia:list')

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, 'Asistencia eliminada exitosamente.')
		return super().delete(request, *args, **kwargs)
