# Alfarería Prehispánica de Nariño

Este proyecto está dedicado a la investigación y documentación de la alfarería prehispánica de Nariño, Colombia. Incluye detalles sobre los complejos cerámicos de Piartal, Quiyacingas y pastos.

## Características
- Documentación de técnicas cerámicas.
- Visualización de hallazgos arqueológicos.
- Funcionalidad de búsqueda por forma o técnica.

## Tecnologías Utilizadas
- Django
- Bootstrap
- SQLite

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/PorgasD/arqueologia_narino.git
    ```

2. Navega al directorio del proyecto:
    ```bash
    cd arqueologia_narino
    ```

3. Crea un entorno virtual e instálalo:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

4. Realiza las migraciones:
    ```bash
    python manage.py migrate
    ```

5. Ejecuta el servidor:
    ```bash
    python manage.py runserver
    ```

## Uso

Accede a la aplicación en tu navegador web en `http://127.0.0.1:8000/`.

## Contribuciones

Si deseas contribuir, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva característica'`).
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request.

