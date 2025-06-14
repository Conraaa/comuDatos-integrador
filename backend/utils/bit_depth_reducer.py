from PIL import Image

def apply_bit_depth_reduction(
    image: Image.Image,
    target_bits: int
) -> Image.Image:
    """
    Aplica reducción de la profundidad de bits a una imagen.

    Esta función simula la cuantificación de color, reduciendo el número
    de colores distintos que se usan en la imagen para representarla.

    Args:
        image (Image.Image): Imagen de entrada de PIL.
        target_bits (int): Profundidad de bits deseada.
                           Valores válidos:
                           - 1 a 8: Para imágenes con paleta indexada (ej: 1 bit para B/N, 8 bits para 256 colores).
                           - 24: Para color real (8 bits por canal RGB, sin reducción de paleta).

    Returns:
        Image.Image: Imagen con profundidad de bits ajustada.

    Raises:
        ValueError: Si `target_bits` no está en el rango válido (1-8 o 24).
    """
    if target_bits == 24:
        # Para 24 bits (color real), simplemente nos aseguramos de que la imagen
        # esté en modo RGB sin aplicar ninguna cuantificación de paleta.
        return image.convert("RGB")
    elif 1 <= target_bits <= 8:
        # Para profundidades de 1 a 8 bits, se usa .quantize() para reducir
        # la imagen a una paleta con 2^target_bits colores.
        num_colors = 2**target_bits
        return image.quantize(colors=num_colors)
    else:
        # Lanza un error si el valor de target_bits no es soportado.
        raise ValueError("target_bits debe estar en el rango de 1 a 8, o ser 24.")