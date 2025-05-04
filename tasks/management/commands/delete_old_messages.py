from django.core.management.base import BaseCommand
from tasks.models import MensajeCocina
from datetime import timedelta
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Elimina mensajes especiales con más de 48 horas de antigüedad.'

    def handle(self, *args, **kwargs):
        limite_tiempo = now() - timedelta(hours=48)
        mensajes_eliminados, _ = MensajeCocina.objects.filter(creado_en__lt=limite_tiempo).delete()
        self.stdout.write(self.style.SUCCESS(f'Se eliminaron {mensajes_eliminados} mensajes especiales antiguos.'))