from django.urls import path
from .views import SolicitudCreateView, SolicitudConfirmacionView

app_name = 'solicitudes'
urlpatterns = [
    path('', SolicitudCreateView.as_view(), name='crear'),
    path('confirmacion/', SolicitudConfirmacionView.as_view(), name='confirmacion'),
]