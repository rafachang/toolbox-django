from django import template

register = template.Library()

@register.filter
def dictKeyLookupQuantidade(the_dict, key):
   # Try to fetch from the dict, and if it's not found return an empty string.
   return the_dict.get(key).get('quantidade')

@register.filter
def dictKeyLookupDescricao(the_dict, key):
   # Try to fetch from the dict, and if it's not found return an empty string.
   return the_dict.get(key).get('descricao')

@register.filter
def roundvalue(value):
   return round(value, 2)