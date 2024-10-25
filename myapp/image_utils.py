from PIL import Image
import hashlib

def embed_hash_in_image(image_path, output_path):
    """Incrusta el hash SHA256 en los primeros píxeles de una imagen."""
    img = Image.open(image_path)
    width, height = img.size

    # Calcular el hash
    hasher = hashlib.sha256()
    with open(image_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    image_hash = hasher.hexdigest()

    # Incrustar el hash en los primeros píxeles
    for i in range(min(len(image_hash), width * height)):
        x = i % width
        y = i // width
        r, g, b = img.getpixel((x, y))
        # Modificar ligeramente el color del componente rojo con base en el hash
        new_r = (r + int(image_hash[i], 16)) % 256
        img.putpixel((x, y), (new_r, g, b))

    # Guardar la nueva imagen con el hash incrustado
    img.save(output_path)  # Sobrescribe o guarda como un nuevo archivo

    return image_hash  # Devuelve el hash para guardarlo en la base de datos