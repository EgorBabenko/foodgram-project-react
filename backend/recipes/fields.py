import base64

from django.core import validators
from django.core.files.base import ContentFile
from django.db import models
from rest_framework.serializers import ImageField


class HexField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        super().__init__(*args, **kwargs)
        self.validators.append(
            validators.RegexValidator(
                regex=r'#([a-fA-F0-9]{6})',
                message='Введите корректное значение HEX кода цвета',
            )
        )


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            data_format, imgstr = data.split(';base64,')
            ext = data_format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
