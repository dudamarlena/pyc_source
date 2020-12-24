# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/devenv/presto_build.py
# Compiled at: 2016-03-01 07:13:25
import argparse, xml.etree.ElementTree as elementTree, os, contextlib, subprocess, shutil, tempfile
from datetime import datetime
from common.resources import image_path
from common.cluster_config import PRESTO_IMAGE
from common.cluster import docker_image_build, docker_tag
PRESTO_SOURCE_ROOT = None
PRESTO_WORKER_CONFIG_DIR = None
PRESTO_MASTER_CONFIG_DIR = None
PRESTO_VERSION = None
BUILD_PRESTO = None
ADD_IMAGE_TAG = None

def parse_args(args):
    global ADD_IMAGE_TAG
    global BUILD_PRESTO
    global PRESTO_MASTER_CONFIG_DIR
    global PRESTO_SOURCE_ROOT
    global PRESTO_WORKER_CONFIG_DIR
    parser = argparse.ArgumentParser(prog='devenv presto build-image')
    parser.add_argument('--no-build', help='skip building of presto', dest='build', action='store_false')
    parser.add_argument('--presto-source', help='Presto source directory', dest='presto_source_root', required=True)
    parser.add_argument('--master-config', help='Configuration directory to be used within image for master node', dest='presto_master_config_dir', required=True)
    parser.add_argument('--worker-config', help='Configuration directory to be used within image worker node', dest='presto_worker_config_dir', required=True)
    parser.add_argument('--add-image-tag', help='Tag built image with label based on git revision id and time', dest='add_image_tag', default=False, action='store_true', required=False)
    args = parser.parse_args(args)
    PRESTO_SOURCE_ROOT = os.path.abspath(args.presto_source_root)
    PRESTO_MASTER_CONFIG_DIR = os.path.abspath(args.presto_master_config_dir)
    PRESTO_WORKER_CONFIG_DIR = os.path.abspath(args.presto_worker_config_dir)
    BUILD_PRESTO = args.build
    ADD_IMAGE_TAG = args.add_image_tag


def read_presto_version():
    global PRESTO_VERSION
    pom_xml = '%s/pom.xml' % PRESTO_SOURCE_ROOT
    pom_parsed = elementTree.parse(pom_xml)
    version_tag = pom_parsed.getroot().find('{http://maven.apache.org/POM/4.0.0}version')
    if version_tag is None:
        raise Exception('could not determine version of presto for pom %s' % pom_xml)
    PRESTO_VERSION = version_tag.text
    return


@contextlib.contextmanager
def chdir(path):
    starting_directory = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(starting_directory)


def build_docker_file_dir(target_dir):
    presto_src_package = '%s/presto-server/target/presto-server-%s.tar.gz' % (PRESTO_SOURCE_ROOT, PRESTO_VERSION)
    if not os.path.exists(presto_src_package):
        raise Exception('Presto package %s not found' % presto_src_package)
    shutil.copytree(os.path.join(image_path('presto-local'), 'files'), os.path.join(target_dir, 'files'))
    with chdir(target_dir):
        os.mkdir('presto-server-unpacked')
        subprocess.check_call('tar -xzf %s -C %s' % (presto_src_package, 'presto-server-unpacked'), shell=True)
        shutil.copytree(PRESTO_MASTER_CONFIG_DIR, 'presto-config-master')
        shutil.copytree(PRESTO_WORKER_CONFIG_DIR, 'presto-config-worker')
        dockerfile_contents = '            FROM teradatalabs/centos6-java8-oracle\n            MAINTAINER Lukasz Osipiuk <lukasz.osipiuk@teradata.com>\n\n            RUN mkdir /presto\n            ADD presto-server-unpacked/presto-server-%(presto_version)s /presto\n            RUN mkdir /presto/etc-master\n            RUN mkdir /presto/etc-worker\n            ADD presto-config-master /presto/etc-master\n            ADD presto-config-worker /presto/etc-worker\n            ADD files/launcher-wrapper.sh /presto/bin/\n        ' % {'presto_version': PRESTO_VERSION}
        docker_file = open('Dockerfile', 'w')
        docker_file.write(dockerfile_contents)
        docker_file.close()


def build_presto_if_needed():
    if BUILD_PRESTO:
        build_presto()
    else:
        print 'Skipping building Presto'


def build_presto():
    print 'Building Presto\n'
    with chdir(PRESTO_SOURCE_ROOT):
        subprocess.check_call('mvn install -DskipTests -Dair.check.skip-all=true', shell=True)
        subprocess.check_call('mvn package --projects presto-server', shell=True)


def build_image():
    docker_image_build(image_path('centos6-java8-oracle'))
    docker_file_dir = tempfile.mkdtemp()
    try:
        build_docker_file_dir(docker_file_dir)
        docker_image_build(docker_file_dir, tag=PRESTO_IMAGE)
    finally:
        shutil.rmtree(docker_file_dir)


def tag_latest_image():
    with chdir(PRESTO_SOURCE_ROOT):
        tag = subprocess.check_output('git rev-parse HEAD', shell=True).strip()
        repo_dirty = subprocess.check_output('git diff-index --name-only HEAD --', shell=True) != ''
        if repo_dirty:
            time_marker = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
            tag = tag + '-' + time_marker
        docker_tag(PRESTO_IMAGE, tag)


def run(args):
    parse_args(args)
    read_presto_version()
    build_presto_if_needed()
    build_image()
    if ADD_IMAGE_TAG:
        tag_latest_image()