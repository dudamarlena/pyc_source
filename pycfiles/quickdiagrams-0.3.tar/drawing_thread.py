# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugoruscitti/Aptana Studio 3 Workspace/quickdiagrams/quickdiagrams/gtkclient/drawing_thread.py
# Compiled at: 2011-01-24 11:46:37
import time
from threading import Thread
import gtk

class DrawingThread(Thread):
    """Representa el componente del programa que dibuja los diagramas.

    Este componente actua de manera desacoplada por medio de un hilo, para
    no interferir en la interfaz de usuario gtk."""

    def __init__(self, main, queue):
        Thread.__init__(self)
        self.queue = queue
        self.main = main

    def run(self):
        while True:
            task = self.queue.get()
            if task:
                task()
                self.queue.task_done()
            else:
                return