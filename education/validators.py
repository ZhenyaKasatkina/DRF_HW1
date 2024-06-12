from rest_framework import serializers


def validate_url(value):

    if "@youtube.com" not in value:
        raise serializers.ValidationError("Можно добавить ссылку только на youtube.com")
