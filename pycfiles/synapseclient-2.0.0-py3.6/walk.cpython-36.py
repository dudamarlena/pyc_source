# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseutils/walk.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 1468 bytes
from synapseclient.entity import is_container
import os

def walk(syn, synId):
    """
    Traverse through the hierarchy of files and folders stored under the synId. Has the same behavior as os.walk()

    :param syn:     A synapse object: syn = synapseclient.login()- Must be logged into synapse

    :param synId:   A synapse ID of a folder or project

    Example::

        walkedPath = walk(syn, "syn1234")

        for dirpath, dirname, filename in walkedPath:
            print(dirpath)
            print(dirname) #All the folders in the directory path
            print(filename) #All the files in the directory path

    """
    return _helpWalk(syn, synId)


def _helpWalk(syn, synId, newpath=None):
    starting = syn.get(synId, downloadFile=False)
    if newpath is None:
        if not is_container(starting):
            return
    else:
        if newpath is None:
            dirpath = (
             starting.name, synId)
        else:
            dirpath = (
             newpath, synId)
    dirs = []
    nondirs = []
    results = syn.getChildren(synId)
    for i in results:
        if is_container(i):
            dirs.append((i['name'], i['id']))
        else:
            nondirs.append((i['name'], i['id']))

    yield (
     dirpath, dirs, nondirs)
    for name in dirs:
        newpath = os.path.join(dirpath[0], name[0])
        for x in _helpWalk(syn, (name[1]), newpath=newpath):
            yield x