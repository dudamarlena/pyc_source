# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/devenv/hadoop_build.py
# Compiled at: 2016-03-01 07:13:25
from common.resources import image_path
from common.cluster import docker_image_build, docker_image_built
from common.cluster_config import CONTAINER_HADOOP

def run(args):
    if not docker_image_built(CONTAINER_HADOOP.image):
        docker_image_build(image_path('centos6-java8-oracle'))
        docker_image_build(image_path('cdh5-base'))
        docker_image_build(image_path('cdh5-hive'))