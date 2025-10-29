from django.views.generic import (
    CreateView, TemplateView, ListView, DetailView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import Solicitud
from .forms import SolicitudForm


class SolicitudListView(ListView):
    model = Solicitud
    template_name = 'solicitudes/solicitud_list.html'
    context_object_name = 'solicitudes'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('search')
        tipo = self.request.GET.get('tipo')
        if q:
            qs = qs.filter(Q(nombre_solicitante__icontains=q) | Q(asunto__icontains=q))
        if tipo:
            qs = qs.filter(tipo_solicitud=tipo)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Solicitudes'
        return context


class SolicitudCreateView(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitudes/clean_form.html'
    success_url = reverse_lazy('asistencia:list')  # Redirigir a la página principal de asistencias

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Formulario de Solicitud'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Solicitud enviada exitosamente. Número de referencia: SOL-{self.object.id:06d}'
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)


class SolicitudDetailView(DetailView):
    model = Solicitud
    template_name = 'solicitudes/solicitud_detail.html'
    context_object_name = 'solicitud'


class SolicitudUpdateView(UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitudes/clean_form.html'
    success_url = reverse_lazy('solicitudes:solicitud_list')

    def form_valid(self, form):
        messages.success(self.request, 'Solicitud actualizada correctamente.')
        return super().form_valid(form)


class SolicitudDeleteView(DeleteView):
    model = Solicitud
    template_name = 'solicitudes/solicitud_confirm_delete.html'
    success_url = reverse_lazy('solicitudes:solicitud_list')


class SolicitudConfirmacionView(TemplateView):
    template_name = 'solicitudes/clean_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Solicitud Enviada'
        context['mensaje'] = 'Su solicitud ha sido enviada exitosamente.'
        return context