# -*- coding: utf-8 -*-
import logging
import os
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

logger = logging.getLogger(__name__)


def image_directory_path(instance: models.Model, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower().strip('.')
    return '{name}.{ext}'.format(name=uuid.uuid4().hex, ext=ext or 'png')


class Job(models.Model):
    PENDING, PROCESSING, DONE = 'pending', 'processing', 'done'
    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (PROCESSING, 'processing'),
        (DONE, 'done'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING, editable=False)

    GAUSSIAN_NOISE, ROTATE, ADD_TO_HUE_AND_SATURATION = 'GaussianNoise', 'Rotate', 'AddToHueAndSaturation'
    FILTER_CHOICES = (
        (GAUSSIAN_NOISE, 'GaussianNoise'),
        (ROTATE, 'Rotate'),
        (ADD_TO_HUE_AND_SATURATION, 'AddToHueAndSaturation'),
    )

    image_filter = models.CharField(max_length=30, choices=FILTER_CHOICES)
    severity = models.PositiveSmallIntegerField(blank=True, null=True, default=1,
                                                validators=[
                                                    MinValueValidator(1),
                                                    MaxValueValidator(5),

                                                ])
    rotate = models.SmallIntegerField(blank=True, null=True, default=0,
                                      validators=[
                                          MinValueValidator(-360),
                                          MaxValueValidator(360),

                                      ])
    value_hue = models.SmallIntegerField(blank=True, null=True, default=None,
                                         validators=[
                                             MinValueValidator(-255),
                                             MaxValueValidator(+255),

                                         ])

    value_saturation = models.SmallIntegerField(blank=True, null=True, default=None,
                                                validators=[
                                                    MinValueValidator(-255),
                                                    MaxValueValidator(+255),
                                                ])
    per_channel = models.CharField(blank=True, null=True, max_length=10, default='False',
                                   )

    file = models.ImageField(upload_to=image_directory_path)

    def __str__(self):
        return '{id}-{status}-{filter}-{filename}'.format(
            id=self.pk,
            status=self.status,
            filter=self.image_filter,
            filename=self.file.name)
