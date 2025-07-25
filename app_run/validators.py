from decimal import Decimal

from rest_framework import serializers


def validate_coordinate(value):
    if value < Decimal('-90.0') or value > Decimal('90.0'):
        raise serializers.ValidationError("Координата должна быть в диапазоне [-90.0, 90.0]")
    # Проверка на 4 знака после запятой
    if value.as_tuple().exponent < -4:  # exponent = -n, где n — знаки после запятой
        raise serializers.ValidationError("Координата должна иметь не более 4 знаков после запятой.")
    return value
