# -*- coding: utf-8 -*-
import logging

from rest_framework import serializers

from job.models import Job
from job.tasks import task_job
from job.utils import per_channel_to_python

logger = logging.getLogger(__name__)


# Фильтр Параметры
# GaussianNoise severity severity=(1, 5)
# Rotate rotate  range is around [-360, 360]

# AddToHueAndSaturation
# value_hue от -255 до +255, Если и это, и значение value_saturation равны None,
# значение может быть установлено в значение, non-None.

# value_saturation Если и это, и значение value_hue равны None,
# значение может быть установлено в значение, non-None. от -255 до +255

# per_channel (bool or float, optional) –
# Whether to sample per image only one value from value and use it for both hue and
# saturation (False) or to sample independently one value for hue and one for saturation
# (True). If this value is a float p, then for p percent of all images per_channel will
# be treated as True, otherwise as False.
# This parameter has no effect is value_hue and/or value_saturation are used instead
# of value.

class JobSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        instance = super().create(validated_data)
        task_job.apply_async(args=[instance.pk])
        return instance

    def validate(self, attrs):
        if attrs.get('image_filter') == Job.GAUSSIAN_NOISE:
            if not attrs.get('severity'):
                raise serializers.ValidationError({'severity': 'Укажите значение от 1 до 5'})

        if attrs.get('image_filter') == Job.ROTATE:
            if not attrs.get('rotate'):
                raise serializers.ValidationError({'severity': 'Укажите значение от -360 до 360'})

        if attrs.get('image_filter') == Job.ADD_TO_HUE_AND_SATURATION:
            from imgaug.augmenters import AddToHueAndSaturation
            try:
                AddToHueAndSaturation(
                    value_hue=attrs.get('value_hue'),
                    value_saturation=attrs.get('value_saturation'),
                    per_channel=per_channel_to_python(attrs.get('per_channel')),
                )
            except Exception as e:
                raise serializers.ValidationError(e)

        return attrs

    class Meta:
        model = Job
        fields = ['id',
                  'url',
                  'image_filter',
                  'severity',
                  'rotate',
                  'value_hue',
                  'value_saturation',
                  'per_channel',
                  'file',
                  'status']


class JobDoneSerializer(JobSerializer):
    class Meta:
        model = Job
        fields = ['id', 'url', 'status', 'image_filter', 'file']


class JobNotDoneSerializer(JobSerializer):
    class Meta:
        model = Job
        fields = ['id', 'url', 'status', 'image_filter']
