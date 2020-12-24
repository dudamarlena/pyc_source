# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/dev/pyCast/shakecast/sc/app/newthread.py
# Compiled at: 2017-04-21 05:20:51
import threading, time, pdb

class New_Thread(threading.Thread):
    """
    A New_Thread is built from a threading.thread with the added
    functionality of looping and intuitive argument passing
    
    Usage:
    ::
        >>>new_thread = New_Thread(func=func, args_in=kwargs)
        >>>new_thread.start()
    
    """

    def __init__(self, func, args_in=None, loop=False, loop_time=5, use_pdb=False):
        super(New_Thread, self).__init__()
        self._stop = threading.Event()
        self.func = func
        self.args_in = args_in
        self.loop = loop
        self.loop_time = loop_time
        self.use_pdb = use_pdb

    def stop(self):
        """
        Stop a looping thread
        """
        self._stop.set()

    def stopped(self):
        self._stop.isSet()

    def run(self):
        """
        The function that is run when new_thread.start() is called
        """
        if self.func is not None:
            if self.loop is False:
                if self.args_in is not None:
                    self.func(**self.args_in)
                else:
                    self.func()
            else:
                while not self._stop.isSet():
                    if self.args is not None:
                        self.func(**self.args_in)
                    else:
                        self.func()
                    time.sleep(self.loop_time)

        return