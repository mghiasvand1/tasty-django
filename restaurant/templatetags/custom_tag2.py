from django import template
from deep_translator import GoogleTranslator

register = template.Library()

@register.filter(name='translate')
def translate(text, languageCode):
    if languageCode != "en":
        translatedText = GoogleTranslator(source='en', target=languageCode).translate(text=text)
        return translatedText
    else:
        return text
