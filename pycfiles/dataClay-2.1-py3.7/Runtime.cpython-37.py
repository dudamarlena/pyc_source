# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/commonruntime/Runtime.py
# Compiled at: 2020-02-11 05:03:46
# Size of source mod 2**32: 2270 bytes
""" Class description goes here. """
import threading, logging
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'
logger = logging.getLogger(__name__)
__all__ = [
 'DataClayObject', 'StorageObject', 'dclayMethod']
threadLocal = threading.local()
runtimes_per_thread = dict()
client_static_runtime = None

def clean_runtime():
    global client_static_runtime
    global runtimes_per_thread
    global threadLocal
    threadLocal = threading.local()
    runtimes_per_thread.clear()
    client_static_runtime = None


def setRuntime(runtime):
    """
    @summary: set runtime in current thread. This function is used in Execution Environment 
    @param runtime: runtime to set 
    """
    thread_id = threading.current_thread().ident
    runtimes_per_thread[thread_id] = runtime


def getRuntime():
    """
    @summary: get runtime associated to current thread. If there is no runtime, return client runtime. 
    In EE if current thread has no runtime, it means thread was not prepared properly and it is wrong!
    @return runtime of the current thread
    """
    global client_static_runtime
    thread_id = threading.current_thread().ident
    if thread_id in runtimes_per_thread:
        return runtimes_per_thread.get(thread_id)
    if client_static_runtime is None:
        import dataclay.commonruntime.ClientRuntime as ClientRuntime
        client_static_runtime = ClientRuntime()
    return client_static_runtime


import dataclay.DataClayObject as DataClayObject
StorageObject = DataClayObject