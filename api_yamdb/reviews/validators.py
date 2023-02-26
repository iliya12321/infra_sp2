import datetime
import re

from django.core.exceptions import ValidationError


def validate_year(value):
    year = datetime.date.today().year
    if value > year:
        raise ValidationError('Год издания не может быть больше текущего года')


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('"me" - Недопустимое имя пользователя.')

    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Cимволы: "{value}" использовать нельзя'),
            params={'value': value},
        )
