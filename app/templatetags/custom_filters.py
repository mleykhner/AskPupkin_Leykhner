from django import template
from AskPupkin_Leykhner.color_utils import string_to_hex_color, get_contrast_color

register = template.Library()

@register.filter
def string_to_hex_color_filter(input_string):
    return string_to_hex_color(input_string.lower())

@register.filter
def get_contrast_color_filter(input_string):
    bg = string_to_hex_color(input_string.lower())
    return get_contrast_color(bg)