"""
Course modes API serializers.
"""
from rest_framework import serializers

from course_modes.models import CourseMode


class CourseModeSerializer(serializers.Serializer):
    """
    Serializer for the CourseMode model.
    """
    MODIFIABLE_FIELDS = {
        'mode_display_name', 'min_price', 'currency', 'expiration_datetime',
        'expiration_datetime_is_explicit', 'description', 'sku', 'bulk_sku',
    }

    course_id = serializers.CharField()
    mode_slug = serializers.CharField()
    mode_display_name = serializers.CharField()
    min_price = serializers.IntegerField()
    currency = serializers.CharField()
    expiration_datetime = serializers.DateTimeField(required=False)
    expiration_datetime_is_explicit = serializers.BooleanField(required=False)
    description = serializers.CharField(required=False)
    sku = serializers.CharField(required=False)
    bulk_sku = serializers.CharField(required=False)

    def create(self, validated_data):
        return CourseMode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        errors = {}

        for field in validated_data:
            if field not in self.MODIFIABLE_FIELDS:
                errors[field] = ['This field cannot be modified.']

        if errors:
            raise serializers.ValidationError(errors)

        for modifiable_field in validated_data:
            setattr(
                instance,
                modifiable_field,
                validated_data.get(modifiable_field, getattr(instance, modifiable_field))
            )
        instance.save()
        return instance
