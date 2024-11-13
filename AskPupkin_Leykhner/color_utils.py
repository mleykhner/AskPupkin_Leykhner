import zlib

def string_to_hex_color(input_string: str) -> str:
    hash_object = zlib.crc32(input_string.encode('utf-8'))
    hex_dig = hex(hash_object)
    color = f"#{hex_dig[2:8]}"
    return color

def get_contrast_color(hex_color: str) -> str:
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    brightness = (r * 299 + g * 587 + b * 114) / 255
    return '#000000' if brightness > 550 else '#FFFFFF'