from django import template
register = template.Library()
# Djangoテンプレートタグライブラリ
# テンプレートで使用する関数

@register.filter
def value1000nTo1k(value):
    if value >= 100000:
        return str(format(int(value/1000),',d')) + ' k'
    else:
        return str(format(int(value),',d'))
