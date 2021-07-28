# -*- coding: utf-8 -*-
import logging

from django.http import HttpResponseRedirect
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from job.models import Job
from job.serializers import JobDoneSerializer, JobNotDoneSerializer, JobSerializer

logger = logging.getLogger(__name__)


class JobViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        self.instance = serializer.save()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('job-detail', args=[self.instance.pk]))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == Job.DONE:
            self.serializer_class = JobDoneSerializer
        else:
            self.serializer_class = JobNotDoneSerializer
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
