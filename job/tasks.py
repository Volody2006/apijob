# -*- coding: utf-8 -*-
from time import sleep

import cv2
from celery import shared_task
from django.conf import settings
from imgaug import augmenters as iaa

from job.models import Job
from job.utils import per_channel_to_python


def update_job(job: Job) -> None:
    img = cv2.imread(job.file.path)
    imglist = [img, ]
    aug = False
    if job.image_filter == Job.GAUSSIAN_NOISE:
        aug = iaa.imgcorruptlike.GaussianNoise(severity=job.severity)
    elif job.image_filter == Job.ROTATE:
        aug = iaa.Rotate(rotate=job.rotate)
    elif job.image_filter == Job.ADD_TO_HUE_AND_SATURATION:
        aug = iaa.AddToHueAndSaturation(value_hue=job.value_hue,
                                        value_saturation=job.value_saturation,
                                        per_channel=per_channel_to_python(job.per_channel),
                                        )
    if aug:
        images_aug = aug.augment_images(imglist)
        cv2.imwrite(job.file.path, images_aug[0])


@shared_task
def task_job(job_id: int) -> None:
    if Job.objects.filter(pk=job_id, status=Job.PENDING).exists():
        jobs = Job.objects.select_for_update().filter(pk=job_id, status=Job.PENDING)
        job = jobs.get()
        jobs.update(status=Job.PROCESSING)
        if not settings.TEST:
            sleep(30)
        update_job(job)
        if not settings.TEST:
            sleep(30)
        jobs = Job.objects.select_for_update().filter(pk=job_id)
        jobs.update(status=Job.DONE)
