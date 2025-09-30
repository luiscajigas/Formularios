from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Asistencia
from .forms import AsistenciaForm


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
