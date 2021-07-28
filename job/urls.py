# -*- coding: utf-8 -*-

from django.urls import include, path
from rest_framework import routers

from job.views import JobViewSet

router = routers.DefaultRouter()
router.register('jobs', JobViewSet)

urlpatterns = [
    path('', include(router.urls))
]
