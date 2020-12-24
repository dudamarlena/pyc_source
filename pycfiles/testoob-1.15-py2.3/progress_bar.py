# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/progress_bar.py
# Compiled at: 2009-10-07 18:08:46
"""Simple GUI progress bar"""
from Tkinter import *
import threading, sys

class NumberWidget:
    __module__ = __name__

    def __init__(self, master, label, count=0):
        font = ('Helvetica', 10, 'bold')
        self.text = Label(master, text=label + ' :', font=font)
        self.text.pack(side=LEFT)
        self.number = Label(master, text=str(count), width=5)
        self.number.pack(side=LEFT)

    def set_count(self, count):
        self.number.configure(text=str(count))


class ProgressBarGuiThread(threading.Thread):
    __module__ = __name__

    def __init__(self, num_tests):
        threading.Thread.__init__(self)
        self.num_tests = num_tests
        self.ready_event = threading.Event()
        self.error = None
        self.bar_state = 'ok'
        self.num_failures = 0
        self.num_skipped = 0
        self.num_tests_run = 0
        return

    def wait_until_ready(self):
        self.ready_event.wait()

    def create_bar_widget(self):
        self.bar_width = 300
        self.bar_height = 30
        self.canvas = Canvas(self.root, height=self.bar_height - 2, relief='sunken', borderwidth=1, width=self.bar_width - 2)
        self.canvas.pack()
        self.progress_bar = self.canvas.create_rectangle(0, 0, 0, self.bar_height, width=0)
        self.percent_label = self.canvas.create_text(self.bar_width / 2, self.bar_height / 2, font=('Helvetica', 10, 'bold'))

    def create_frame(self):
        frame = Frame(self.root)
        frame.pack()
        return frame

    def set_state(self, state):
        if state == 'failed':
            self.num_failures += 1
            self.num_tests_run += 1
            self.bar_state = state
        elif state == 'skip':
            self.num_skipped += 1
        elif state == 'ok':
            self.num_tests_run += 1

    def run(self):
        try:
            try:
                self.root = Tk()
                self.count = 0
                self.create_bar_widget()
                frame = self.create_frame()
                self.test_cases = NumberWidget(frame, 'Test Cases', self.num_tests)
                self.tests_run = NumberWidget(frame, 'Tests Run')
                self.failures = NumberWidget(frame, 'Failures')
                self.skipped = NumberWidget(frame, 'Skipped')
                self.update()
                self.ready_event.set()
                self.root.mainloop()
            except TclError:
                self.error = sys.exc_info()

        finally:
            self.ready_event.set()

    ratio = property(lambda self: float(self.count) / float(self.num_tests))

    def advance(self):
        self.count += 1
        self.update()

    def die(self):
        import time
        time.sleep(1)
        self.root.quit()
        del self.test_cases
        del self.tests_run
        del self.failures
        del self.skipped
        del self.canvas
        del self.root

    def update(self):
        self.canvas.coords(self.progress_bar, 1, 1, self.ratio * self.bar_width, self.bar_height)
        if self.bar_state in ['ok', 'skip']:
            color = 'green'
        else:
            color = 'red'
        self.canvas.itemconfigure(self.progress_bar, fill=color)
        self.canvas.itemconfigure(self.percent_label, text='%d%%' % (self.ratio * 100))
        self.tests_run.set_count(self.count)
        self.failures.set_count(self.num_failures)
        self.skipped.set_count(self.num_skipped)
        self.tests_run.set_count(self.num_tests_run)


from base import BaseReporter

class ProgressBarReporter(BaseReporter):
    """Displays a progress bar"""
    __module__ = __name__

    def start(self):
        BaseReporter.start(self)
        self._pbg = ProgressBarGuiThread(num_tests=self.parameters['num_tests'])
        self._pbg.start()
        self._pbg.wait_until_ready()
        if self._pbg.error:
            raise self._pbg.error[1]

    def done(self):
        BaseReporter.done(self)
        self._pbg.die()
        self._pbg.join()

    def addError(self, test_info, err_info):
        BaseReporter.addError(self, test_info, err_info)
        self._pbg.set_state('failed')
        self._pbg.advance()

    def addFailure(self, test_info, err_info):
        BaseReporter.addFailure(self, test_info, err_info)
        self._pbg.set_state('failed')
        self._pbg.advance()

    def addSuccess(self, test_info):
        BaseReporter.addSuccess(self, test_info)
        self._pbg.set_state('ok')
        self._pbg.advance()

    def addSkip(self, test_info, err_info, isRegistered=True):
        BaseReporter.addSkip(self, test_info, err_info, isRegistered)
        self._pbg.set_state('skip')
        self._pbg.advance()