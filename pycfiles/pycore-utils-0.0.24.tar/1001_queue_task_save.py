# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/1001_queue_task_save.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2015 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import os, django
imageA = None
imageB = None
test_user = None
test_taskA = None
test_taskB = None
test_taskC = None

def setup_module(module):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'corecluster.settings'
    django.setup()


def teardown_module(module):
    global imageA
    global imageB
    global test_taskA
    global test_taskB
    global test_user
    if test_taskA is not None:
        test_taskA.delete()
    test_taskA = None
    test_taskB = None
    if test_user is not None:
        test_user.delete()
    if imageA is not None:
        imageA.delete()
    if imageB is not None:
        imageB.delete()
    imageA = None
    imageB = None
    return


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_empty_queue():
    global imageA
    global imageB
    from corecluster.cache.task import Task
    imageA = None
    imageB = None
    while True:
        tasks = Task.get_task('queue_a', ['test_action'])
        if len(tasks) > 0:
            tasks[0].delete()
        else:
            break

    while True:
        tasks = Task.get_task('queue_b', ['test_action'])
        if len(tasks) > 0:
            tasks[0].delete()
        else:
            break

    return


def test_create_user():
    global test_user
    from corecluster.models.core import User
    test_user = User.create()
    test_user.name = 'unit'
    test_user.surname = 'test'
    test_user.login = 'unittest'
    test_user.set_state('ok')


def test_create_image_objects():
    global imageA
    global imageB
    from corecluster.models.core import Image
    imageA = Image.create(test_user, 'imageA', 'imageA desc', 1024, 'transient', 'virtio', 'private', 'qcow2')
    imageA.save()
    imageB = Image.create(test_user, 'imageB', 'imageB desc', 1024, 'transient', 'virtio', 'private', 'qcow2')
    imageB.save()


def test_add_task():
    global test_taskA
    from corecluster.cache.task import Task
    assert imageA.last_task == None
    test_taskA = Task()
    test_taskA.type = 'queue_a'
    test_taskA.state = 'not active'
    test_taskA.action = 'test_action'
    test_taskA.append_to([imageA])
    assert test_taskA.blockers == []
    return


def test_saved_task():
    from corecluster.cache.task import Task
    task_a = Task(cache_key=test_taskA.cache_key())
    assert hasattr(task_a, 'Image_module')
    assert hasattr(task_a, 'Image_id')
    assert task_a.blockers == []
    assert task_a.Image_module != None
    assert task_a.Image_id != None
    image = test_taskA.get_obj('Image')
    assert image != None
    assert image.id != None
    img_a = Image.objects.get(pk=imageA.id)
    assert img_a.last_task == test_taskB.cache_key()
    return