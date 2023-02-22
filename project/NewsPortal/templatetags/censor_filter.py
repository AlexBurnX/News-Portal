from django import template

register = template.Library()


# Заполните список необходимыми словами для цензурирования новостей
BAD_WORDS = [
    'редиска',
    'слово1',
    'слово2',
    'слово3',
]


@register.filter(name='censor')
def censor(text):

    if type(text) != str:
        raise ValueError('Входные данные не являются строкой!')

    for bw1 in BAD_WORDS:
        bw2 = bw1.capitalize()
        text = text.replace(bw1, bw1[0] + ('*' * (len(bw1) - 1)))
        text = text.replace(bw2, bw2[0] + ('*' * (len(bw2) - 1)))

    return f'{text}'
