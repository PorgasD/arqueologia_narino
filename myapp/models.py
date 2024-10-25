from django.db import models # type: ignore
import hashlib

from myapp.image_utils import embed_hash_in_image

DEPARTAMENTOS = [
    ('Amazonas', 'Amazonas'),
    ('Antioquia', 'Antioquia'),
    ('Arauca', 'Arauca'),
    ('Atlántico', 'Atlántico'),
    ('Bolívar', 'Bolívar'),
    ('Boyacá', 'Boyacá'),
    ('Caldas', 'Caldas'),
    ('Caquetá', 'Caquetá'),
    ('Casanare', 'Casanare'),
    ('Cauca', 'Cauca'),
    ('Cesar', 'Cesar'),
    ('Chocó', 'Chocó'),
    ('Córdoba', 'Córdoba'),
    ('Cundinamarca', 'Cundinamarca'),
    ('Guainía', 'Guainía'),
    ('Guaviare', 'Guaviare'),
    ('Huila', 'Huila'),
    ('La Guajira', 'La Guajira'),
    ('Magdalena', 'Magdalena'),
    ('Meta', 'Meta'),
    ('Nariño', 'Nariño'),
    ('Norte de Santander', 'Norte de Santander'),
    ('Putumayo', 'Putumayo'),
    ('Quindío', 'Quindío'),
    ('Risaralda', 'Risaralda'),
    ('San Andrés y Providencia', 'San Andrés y Providencia'),
    ('Santander', 'Santander'),
    ('Sucre', 'Sucre'),
    ('Tolima', 'Tolima'),
    ('Valle del Cauca', 'Valle del Cauca'),
    ('Vaupés', 'Vaupés'),
    ('Vichada', 'Vichada'),
]

COMPLEJO_CERAMICO = [
    ('Capulí', 'Capulí'),
    ('Tuza', 'Tuza'),
    ('Piartal', 'Piartal')
]

ACABADO_SUPERFICIE = [
    ('Alisado', 'Alisado'),
    ('Baño', 'Baño'),
    ('Bruñido', 'Bruñido'),
    ('Engobe', 'Engobe'),
    ('Erosionado', 'Erosionado'),
    ('Pulido', 'Pulido'),
    ('Alisado y Bruñido', 'Alisado y Bruñido'),
    ('Alisado y Baño', 'Alisado y Baño'),
    ('Alisado, Bruñido y Pulido', 'Alisado, Bruñido y Pulido'),
    ('Alisado, Bruñido, erosionado y Pulido', 'Alisado, Bruñido, erosionado y Pulido'),
    ('Alisado y Englobe', 'Alisado y Englobe'),
    ('Alisado, erosionado y Englobe', 'Alisado, erosionado y Englobe'),
    ('Alisado y erosionado', 'Alisado y erosionado'),
     ('Alisado y pulido', 'Alisado y pulido'),
]

TECNICA_MANUFACTURA = [
    ('Rollos y Modelado', 'Rollos y Modelado'),
    ('Pellizcado y Modelado', 'Pellizcado y Modelado'),
    ('Colombín y Modelado', 'Colombín y Modelado'),
    ('Torneado', 'Torneado'),
    ('Moldeado', 'Moldeado')
]

TEXTURA_PASTA = [
    ('Compacta', 'Compacta'),
    ('Friable', 'Friable'),
    ('Granular', 'Granular'),
    ('Laminar', 'Laminar'),
    ('Porosa', 'Porosa')
]

COCCION = [
    ('Oxidante', 'Oxidante'),
    ('Reducida', 'Reducida'),
    ('Mixta', 'Mixta')
]

TAMANO_DESGRASANTE = [
    ('Muy fino', 'Muy fino'),
    ('Fino', 'Fino'),
    ('Medio', 'Medio'),
    ('Grueso', 'Grueso')
]

def hash_image(image_path):
    """Calcula el hash SHA256 de una imagen."""
    hasher = hashlib.sha256()
    try:
        with open(image_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None  # Manejo de errores

class Imagen(models.Model):
    departamento = models.CharField(
        max_length=50,
        choices=DEPARTAMENTOS,
        default='Antioquia'  # Valor por defecto
    )
    corregimiento = models.CharField(max_length=100, default='')
    forma = models.CharField(max_length=100, default='')
    descripcion = models.TextField(default='')
    altura_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    autor = models.CharField(max_length=100, default='Desconocido')
    complejo_ceramico = models.CharField(
        max_length=50,
        choices=COMPLEJO_CERAMICO,
        default='Capulí'  # Valor por defecto
    )
    tecnica_decorativa = models.CharField(max_length=100, default='')
    acabado_superficie = models.CharField(
        max_length=50,
        choices=ACABADO_SUPERFICIE,
        default='Alisado'  # Valor por defecto
    )
    tecnica_manufactura = models.CharField(
        max_length=50,
        choices=TECNICA_MANUFACTURA,
        default='Moldeado'  # Valor por defecto
    )
    textura_pasta = models.CharField(
        max_length=50,
        choices=TEXTURA_PASTA,
        default='Compacta'  # Valor por defecto
    )
    coccion = models.CharField(
        max_length=50,
        choices=COCCION,
        default='Oxidante'  # Valor por defecto
    )
    color_pasta = models.CharField(max_length=50, default='')
    composicion_desgrasante = models.CharField(max_length=100, default='')
    tamano_desgrasante = models.CharField(
        max_length=50,
        choices=TAMANO_DESGRASANTE,
        default='Medio'  # Valor por defecto
    )
    imagen = models.ImageField(upload_to='images/', default='images/default.jpg')  # Imagen por defecto
    hash = models.CharField(max_length=64, unique=True, null=True, blank=True)  # Asegúrate de que este campo esté aquí

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Primero guarda la instancia para crear el archivo
        if self.imagen:
            output_path = self.imagen.path  # Usa la misma ruta para sobrescribir
            image_hash = embed_hash_in_image(self.imagen.path, output_path)  # Llama a la función con ambos argumentos
            
            # Guarda el hash en la base de datos
            self.hash = image_hash
            
            if self.hash:  # Si se generó un hash válido
                super().save(update_fields=['hash'])  # Guarda solo el campo del hash


#modelo de tecnicas ceramicas

class TecnicaCeramica(models.Model):
    TIPO_CHOICES = [
        ('tecnica_manufactura', 'Técnica manufactura'),
        ('tipologia_ceramica', 'Tipología cerámica'),
        ('decoracion_ceramica', 'Decoración cerámica'),
        ('coccion_ceramica', 'Cocción cerámica'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='imagenes/')
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
#modelo de noticia

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    enlace = models.URLField()
    fecha_publicacion = models.DateTimeField()
    imagen = models.URLField(blank=True, null=True)  # Campo para la imagen

    def __str__(self):
        return self.titulo
    

    #mapa

class Hallazgo(models.Model):
    nombre = models.CharField(max_length=200)
    departamento = models.CharField(max_length=100)
    corregimiento = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return f"{self.nombre} - {self.corregimiento}, {self.departamento}"
    
   