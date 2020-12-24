# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/extend/summary.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.extend.my import my_i, my_c
from cloudmesh_client.common.DynamicClass import DynamicClass

def z_a(args):
    print('z_a', args)


def z_c(cls, args):
    print('z_c', args)


def z_b(cls, args):
    print('z_b', args)


class A(DynamicClass):
    pass


if __name__ == '__main__':
    a = A()
    a.add_instance_method(my_i)
    a.my_i('i am my_i')
    A.add_classmethod(my_c)
    a.my_c('i am my_c')
    A.load_classmethod('cloudmesh_client.extend.my.my_cc')
    a.my_cc('i am my_cc')
    b = A()
    b.my_cc('i am my_cc')
    A.z_b = z_b
    A().z_b('i am z_b')
    A.load_classmethod('cloudmesh_client.extend.my.my_ccc')
    A().my_ccc('YOURS')