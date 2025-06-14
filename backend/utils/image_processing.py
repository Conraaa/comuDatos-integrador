"""
sample_rate: tomar un píxel cada 'n' píxeles en ambas direcciones.
             valores más altos reducen la resolución espacial (muestreo).
              
quantization_bits: número de bits para la cuantización de color por canal.
                   valores más bajos reducen la profundidad de color (cuantización).
                   ej: 8 bits (256 colores), 4 bits (16 colores), 2 bits (4 colores).
"""

from PIL import Image

def process_image_for_digitalization(
    image: Image.Image,
    sample_rate: int = 1,
    quantization_bits: int = 8
) -> Image.Image:
    if sample_rate < 1:
        raise ValueError("sample_rate debe ser al menos 1.")
    if not (1 <= quantization_bits <= 8):
        raise ValueError("quantization_bits debe estar entre 1 y 8.")

    # para simular la perdida de muestreo (reducción de resolución espacial)
    # se redimensiona la imagen a una resolución mas baja y despues se vuelve a escalar al tamaño original
    if sample_rate > 1:
        width, height = image.size
        new_width = width // sample_rate
        new_height = height // sample_rate

        sampled_image = image.resize((new_width, new_height), Image.Resampling.NEAREST)
        sampled_image = sampled_image.resize((width, height), Image.Resampling.NEAREST)
    else:
        sampled_image = image.copy()
        
    # para simular la perdida de colores disponibles en la imagen.
    # se manipulan los pixeles (paleta) si la cuantización es baja
    if quantization_bits < 8:
        num_colors = 2**quantization_bits
        quantized_image = sampled_image.quantize(colors=num_colors)
    else:
        quantized_image = sampled_image

    return quantized_image