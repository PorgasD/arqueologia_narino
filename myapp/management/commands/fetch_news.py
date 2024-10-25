import requests
from django.core.management.base import BaseCommand
from myapp.models import Noticia

class Command(BaseCommand):
    help = 'Obtener noticias sobre arqueología prehispánica en Colombia desde NewsAPI'

    def handle(self, *args, **kwargs):
        api_key = '50b02d4986384ad6a5bbe6c14ba700b6'  # tu clave de API
         # Cambia la consulta para buscar noticias sobre arqueología en Colombia
        url = f'https://newsapi.org/v2/everything?q=colombia+arqueología&apiKey={api_key}'
        
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'ok':
            articles = data['articles'][:12]  # Limitar a los primeros 12 artículos
            for item in data['articles']:
                Noticia.objects.update_or_create(
                    titulo=item['title'],
                    defaults={
                        'contenido': item['description'],
                        'enlace': item['url'],
                        'fecha_publicacion': item['publishedAt'],
                        'imagen': item.get('urlToImage', '')  # Obtener la URL de la imagen
                    }
                )
            self.stdout.write(self.style.SUCCESS('Noticias obtenidas con éxito'))
        else:
            self.stdout.write(self.style.ERROR('Error al obtener noticias'))