# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/th13f/dev/drf-batch-requests/drf_batch_requests/utils.py
# Compiled at: 2018-02-16 08:16:44
import random, string

def get_attribute(instance, attrs):
    for attr in attrs:
        if instance is None:
            return
        if attr == '*':
            continue
        if isinstance(instance, list):
            instance = list(map(lambda i: i[attr], instance))
        else:
            instance = instance[attr]

    return instance


def generate_random_id(size=10, chars=string.ascii_uppercase + string.digits):
    return ('').join(random.choice(chars) for _ in range(size))


def generate_node_callback(node, status):

    def callback():
        if status == 'start':
            node.start()
        elif status == 'success':
            node.complete()
        elif status == 'fail':
            node.fail()
        else:
            raise NotImplementedError

    return callback