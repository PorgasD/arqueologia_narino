# myapp/admin.py
from django.contrib import admin # type: ignore
from .models import Hallazgo, Imagen, TecnicaCeramica

class ImagenAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'corregimiento', 'forma', 'descripcion', 'altura_total', 'complejo_ceramico', 'tecnica_decorativa', 'acabado_superficie', 'tecnica_manufactura', 'textura_pasta', 'coccion', 'color_pasta', 'composicion_desgrasante', 'tamano_desgrasante', 'imagen', 'hash')
    search_fields = ('descripcion', 'corregimiento', 'forma')
    list_filter = ('departamento', 'complejo_ceramico', 'acabado_superficie', 'tecnica_manufactura', 'textura_pasta', 'coccion', 'tamano_desgrasante')

admin.site.register(Imagen, ImagenAdmin)


class TecnicaCeramicaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')  # Muestra los campos en la lista
    search_fields = ('nombre',)  # Permite buscar por nombre

admin.site.register(TecnicaCeramica, TecnicaCeramicaAdmin)

admin.site.register(Hallazgo)