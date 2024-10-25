import json
from django.core.paginator import Paginator  
from django.http import JsonResponse 
from django.shortcuts import redirect, render  
from django.db.models import Q 

from myapp.utils import send_verification_code, verify_code  # type: ignore
from .models import Hallazgo, Imagen, Noticia, TecnicaCeramica
from django.contrib.auth import authenticate, login # type: ignore

def home(request):
    return render(request, 'index.html')

def paginate_images(request, items):
    paginator = Paginator(items, 4)  # Mostrar 4 elementos por página
    page_number = request.GET.get('page')  # Obtener el número de página de la solicitud
    page_obj = paginator.get_page(page_number)  # Obtener la página actual
    return page_obj

def index(request):
    periodo = request.GET.get('periodo')
    query = request.GET.get('q')

    # Inicializar las consultas de imágenes y técnicas
    imagenes = []
    tecnicas = []

     # Obtener noticias desde la base de datos
    noticias = Noticia.objects.all()[:12]  # Limitar a los primeros 12 artículos

    # Solo realizar consultas si hay un periodo o un término de búsqueda
    if periodo or query:
        imagenes = Imagen.objects.all()
        tecnicas = TecnicaCeramica.objects.all()

        # Filtrar imágenes por periodo si se especifica
        if periodo:
            imagenes = imagenes.filter(complejo_ceramico=periodo)

        # Filtrar imágenes por la búsqueda si se especifica
        if query:
            imagenes = imagenes.filter(
                Q(departamento__icontains=query) |
                Q(corregimiento__icontains=query) |
                Q(forma__icontains=query) |
                Q(complejo_ceramico__icontains=query) |
                Q(tecnica_decorativa__icontains=query) |
                Q(acabado_superficie__icontains=query) |
                Q(tecnica_manufactura__icontains=query) |
                Q(textura_pasta__icontains=query) |
                Q(coccion__icontains=query) |
                Q(color_pasta__icontains=query) |
                Q(composicion_desgrasante__icontains=query) |
                Q(tamano_desgrasante__icontains=query)
            )

            # Filtrar técnicas cerámicas según el término de búsqueda
            tecnicas = tecnicas.filter(nombre__icontains=query)

    # Paginación para imágenes
    page_obj_imagenes = paginate_images(request, imagenes)

    return render(request, 'index.html', {
        'page_obj': page_obj_imagenes,
        'tecnicas': tecnicas,
        'query': query,
        'periodo': periodo,
        'noticias': noticias,  # Pasar las noticias al contexto
    })
def tecnica_por_tipo(request, tipo):
    # Filtra las técnicas cerámicas según el tipo seleccionado
    tecnicas = TecnicaCeramica.objects.filter(tipo=tipo)
    
    return render(request, 'tecnica_por_tipo.html', {
        'tecnicas': tecnicas,
        'tipo': tipo,
    })

#mapa
def map_view(request):
    # Lógica para mostrar el mapa
    return render(request, 'map.html')

def hallazgos_json(request):
    # Obtener todos los hallazgos y convertir a una lista de diccionarios
    hallazgos = list(Hallazgo.objects.values('nombre', 'latitud', 'longitud'))
    return JsonResponse(hallazgos, safe=False)  # Retornar los datos como JSON

#MFA

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generar y enviar código de verificación
            phone_number = user.profile.phone_number  # Asegúrate de que el usuario tenga un número registrado
            send_verification_code(phone_number)

            request.session['phone_number'] = phone_number  # Guardar el número en la sesión
            return redirect('verify_code')  # Redirige a la vista donde se ingresa el código

        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas.'})

    return render(request, 'login.html')

#Vista para verificar el codigo SMS:

def verify_code_view(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        phone_number = request.session.get('phone_number')

        if verify_code(phone_number, entered_code):
            user = authenticate(username=request.session.get('username'))  # Asegúrate de guardar el nombre de usuario en la sesión
            login(request, user)  # Iniciar sesión del usuario si el código es correcto
            return redirect('admin:index')  # Redirige al panel de administración
        else:
            return render(request, 'verify_code.html', {'error': 'Código incorrecto.'})

    return render(request, 'verify_code.html')