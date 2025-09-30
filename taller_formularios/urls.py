from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('asistencia/', include('asistencia.urls')),
    path('solicitudes/', include('solicitudes.urls')),
    path('', RedirectView.as_view(url='/asistencia/', permanent=False), name='home'),
]
