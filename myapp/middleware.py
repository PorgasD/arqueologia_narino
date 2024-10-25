# myapp/middleware.py

import time
from django.core.cache import cache
from django.http import HttpResponse

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la dirección IP del usuario
        ip = self.get_client_ip(request)
        current_time = time.time()

        # Definir una clave única para la dirección IP
        cache_key = f'rate_limit_{ip}'
        
        # Obtener el número de solicitudes y el tiempo de la última solicitud
        requests_data = cache.get(cache_key, (0, current_time))

        request_count, last_request_time = requests_data

        # Si ha pasado más de 60 segundos desde la última solicitud
        if current_time - last_request_time > 60:
            request_count = 0  # Reiniciar el contador

        # Incrementar el contador de solicitudes
        request_count += 1

        # Almacenar los datos en caché
        cache.set(cache_key, (request_count, current_time), timeout=60)

        # Limitar a 100 solicitudes por minuto
        if request_count > 100:
            return HttpResponse("Demasiadas solicitudes. Intenta más tarde.", status=429)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Obtener la dirección IP del cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip