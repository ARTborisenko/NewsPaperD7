from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value, active=True):
    if isinstance(value, str) and active:
        bad_words = ['черный', 'нигер', 'убью']
        good_text_list = value.split()
        good_text = ''
        for word in good_text_list:
            if word.lower() in bad_words:
                word = '*' * len(word)
            good_text += word
            good_text += " "
        return good_text
    elif isinstance(value, str) and not active:
        return value
    else:
        raise ValueError(f'Фильтр не позволяет зацензурить переменную типа: {type(value)}')