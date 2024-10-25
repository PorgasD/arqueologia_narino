from django.urls import path, include  # type: ignore
from . import views
from .views import index, login_view, map_view, hallazgos_json, verify_code_view
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='index/', permanent=True)),  # Redirige a /index/
    path('index/', views.index, name='index'),  # Ruta para la vista de índice
    path('tecnica/<str:tipo>/', views.tecnica_por_tipo, name='tecnica_por_tipo'),  # Ruta para filtrar por tipo
    path('map/', views.map_view, name='map_view'), 
    path('api/hallazgos/', views.hallazgos_json, name='hallazgos_json'),
    path('login/', views.login_view, name='login'),
    path('verify-code/', views.verify_code_view, name='verify_code'),
]