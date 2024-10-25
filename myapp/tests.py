import json
from django.test import Client, TestCase

# Create your tests here.
from .models import Imagen, TecnicaCeramica, Noticia, Hallazgo # type: ignore
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


#tests para modelos ORM o models
class ImagenModelTest(TestCase):
    
    def setUp(self):
        self.imagen = Imagen.objects.create(
            departamento='Antioquia',
            corregimiento='Envigado',
            forma='Vasija',
            descripcion='Vasija prehispánica.',
            altura_total=15.50,
            autor='Desconocido',
            complejo_ceramico='Capulí',
            tecnica_decorativa='Pintura roja',
            acabado_superficie='Alisado',
            tecnica_manufactura='Moldeado',
            textura_pasta='Compacta',
            coccion='Oxidante',
            color_pasta='Marrón',
            composicion_desgrasante='Arena',
            tamano_desgrasante='Fino',
            imagen='images/test_image.jpg'
        )

    def test_str_method(self):
        self.assertEqual(str(self.imagen), 'Vasija prehispánica.')

    def test_default_values(self):
        imagen = Imagen.objects.create()
        self.assertEqual(imagen.departamento, 'Antioquia')
        self.assertEqual(imagen.complejo_ceramico, 'Capulí')
        self.assertEqual(imagen.acabado_superficie, 'Alisado')
        self.assertEqual(imagen.tecnica_manufactura, 'Moldeado')
        self.assertEqual(imagen.textura_pasta, 'Compacta')
        self.assertEqual(imagen.coccion, 'Oxidante')
        self.assertEqual(imagen.tamano_desgrasante, 'Medio')

class TecnicaCeramicaModelTest(TestCase):
    
    def setUp(self):
        self.tecnica_ceramica = TecnicaCeramica.objects.create(
            nombre='Técnica de Rollo',
            descripcion='Se utiliza para crear formas cilíndricas.',
            imagen='imagenes/tecnica_rollo.jpg',
            tipo='tecnica_manufactura'
        )

    def test_str_method(self):
        self.assertEqual(str(self.tecnica_ceramica), 'Técnica de Rollo')

class NoticiaModelTest(TestCase):
    
    def setUp(self):
        self.noticia = Noticia.objects.create(
            titulo='Descubrimiento arqueológico en Nariño',
            contenido='Se ha descubierto una vasija en perfecto estado.',
            enlace='https://ejemplo.com/descubrimiento',
            fecha_publicacion=timezone.now(),
            imagen='https://ejemplo.com/imagen_vasija.jpg'
        )

    def test_str_method(self):
        self.assertEqual(str(self.noticia), 'Descubrimiento arqueológico en Nariño')

    def test_noticia_creation(self):
        noticia = Noticia.objects.create(
            titulo='Nueva noticia',
            contenido='Contenido de la nueva noticia.',
            enlace='https://ejemplo.com/nueva-noticia',
            fecha_publicacion=timezone.now()
        )
        self.assertEqual(noticia.titulo, 'Nueva noticia')

class HallazgoModelTest(TestCase):
    
    def setUp(self):
        self.hallazgo = Hallazgo.objects.create(
            nombre='Sitio arqueológico de Nariño',
            departamento='Nariño',
            corregimiento='Tuquerres',
            latitud=1.2345,
            longitud=-77.1234
        )

    def test_str_method(self):
        self.assertEqual(str(self.hallazgo), 'Sitio arqueológico de Nariño - Tuquerres, Nariño')

    def test_hallazgo_creation(self):
        hallazgo = Hallazgo.objects.create(
            nombre='Nuevo hallazgo',
            departamento='Antioquia',
            corregimiento='Medellín',
            latitud=6.2442,
            longitud=-75.5812
        )
        self.assertEqual(hallazgo.nombre, 'Nuevo hallazgo')

#Tests para las vistas o views
class ViewsTestCase(TestCase):
    def setUp(self):
        # Crear cliente de prueba
        self.client = Client()

        # Crear usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Crear objetos de prueba para Noticia, Imagen y TecnicaCeramica
        self.noticia = Noticia.objects.create(
            titulo="Noticia de Prueba",
            contenido="Contenido de prueba",
            enlace="https://example.com",
            fecha_publicacion="2024-10-22T12:00:00Z",
        )

        self.imagen = Imagen.objects.create(
            departamento="Antioquia",
            corregimiento="Medellín",
            forma="Vase",
            descripcion="Una imagen de prueba",
            altura_total=25.5,
            autor="Autor de prueba",
            complejo_ceramico="Capulí",
            tecnica_decorativa="Decoración de prueba",
            acabado_superficie="Alisado",
            tecnica_manufactura="Moldeado",
            textura_pasta="Compacta",
            coccion="Oxidante",
            color_pasta="Rojo",
            composicion_desgrasante="Desgrasante de prueba",
            tamano_desgrasante="Medio",
            imagen="images/default.jpg",
        )

        self.tecnica = TecnicaCeramica.objects.create(
            nombre="Técnica de prueba",
            descripcion="Descripción de la técnica de prueba",
            imagen="imagenes/default.jpg",
            tipo="tecnica_manufactura"
        )

        self.hallazgo = Hallazgo.objects.create(
            nombre="Hallazgo de prueba",
            departamento="Antioquia",
            corregimiento="Medellín",
            latitud=6.25184,
            longitud=-75.56359
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('noticias', response.context)
        self.assertEqual(len(response.context['noticias']), 1)

    def test_index_view_with_search(self):
        response = self.client.get(reverse('index'), {'q': 'Medellín'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)
        self.assertEqual(len(response.context['page_obj'].object_list), 1)

    def test_tecnica_por_tipo_view(self):
        response = self.client.get(reverse('tecnica_por_tipo', kwargs={'tipo': 'tecnica_manufactura'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tecnica_por_tipo.html')
        self.assertEqual(len(response.context['tecnicas']), 1)

    def test_map_view(self):
        response = self.client.get(reverse('map_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map.html')

    def test_hallazgos_json(self):
        response = self.client.get(reverse('hallazgos_json'))
        self.assertEqual(response.status_code, 200)
        hallazgos_data = json.loads(response.content)
        self.assertEqual(len(hallazgos_data), 1)
        self.assertEqual(hallazgos_data[0]['nombre'], 'Hallazgo de prueba')
