from django.urls import path
from .views import (
    SolicitudListView,
    SolicitudCreateView,
    SolicitudDetailView,
    SolicitudUpdateView,
    SolicitudDeleteView,
    SolicitudConfirmacionView,
)

app_name = 'solicitudes'

urlpatterns = [
    path('', SolicitudListView.as_view(), name='solicitud_list'),
    path('nuevo/', SolicitudCreateView.as_view(), name='solicitud_create'),
    path('<int:pk>/', SolicitudDetailView.as_view(), name='solicitud_detail'),
    path('<int:pk>/editar/', SolicitudUpdateView.as_view(), name='solicitud_update'),
    path('<int:pk>/eliminar/', SolicitudDeleteView.as_view(), name='solicitud_delete'),
    path('confirmacion/', SolicitudConfirmacionView.as_view(), name='solicitud_confirmacion'),
]