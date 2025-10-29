from django.apps import AppConfig
import os
from django.conf import settings

class SolicitudesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'solicitudes'
    verbose_name = 'Gestión Solicitudes'

    def ready(self):
        """Ensure MEDIA_ROOT exists and has permissive permissions in development."""
        try:
            media_root = settings.MEDIA_ROOT
            if media_root:
                os.makedirs(media_root, exist_ok=True)
                # try to set permissive permissions where supported
                try:
                    os.chmod(media_root, 0o777)
                except Exception:
                    # ignore permission setting errors on platforms like Windows
                    pass
        except Exception:
            # keep startup robust even if settings not fully available
            pass