from PIL import Image

def apply_bit_depth_reduction(
    image: Image.Image,
    target_bits: int
) -> Image.Image:
    if target_bits == 24:
        return image.convert("RGB")
    elif 1 <= target_bits <= 8:
        num_colors = 2**target_bits
        return image.quantize(colors=num_colors)
    else:
        raise ValueError("target_bits debe estar en el rango de 1 a 8, o ser 24.")