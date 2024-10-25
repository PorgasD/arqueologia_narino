from django import forms # type: ignore
from .models import Imagen

class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = [
            'departamento',
            'corregimiento',
            'forma',
            'descripcion',
            'altura_total',
            'complejo_ceramico',
            'tecnica_decorativa',
            'acabado_superficie',
            'tecnica_manufactura',
            'textura_pasta',
            'coccion',
            'color_pasta',
            'composicion_desgrasante',
            'tamaño_desgrasante',
            'imagen'
            'hash'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'imagen': forms.FileInput(attrs={'accept': 'image/*'}),
        }
