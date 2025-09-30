from django.db import models
from django.utils import timezone


class AsistenciaManager(models.Manager):
    """
    Manager personalizado para consultas optimizadas de Asistencia
    """

    def presentes_hoy(self):
        """Retorna asistencias marcadas como presente para hoy"""
        return self.filter(
            fecha_asistencia=timezone.now().date(),
            presente=True
        )

    def por_fecha(self, fecha):
        """Retorna asistencias para una fecha específica"""
        return self.filter(fecha_asistencia=fecha)

    def estadisticas_mes_actual(self):
        """Retorna estadísticas del mes actual"""
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)

        return {
            'total': self.filter(fecha_asistencia__gte=inicio_mes).count(),
            'presentes': self.filter(
                fecha_asistencia__gte=inicio_mes,
                presente=True
            ).count(),
            'ausentes': self.filter(
                fecha_asistencia__gte=inicio_mes,
                presente=False
            ).count()
        }
