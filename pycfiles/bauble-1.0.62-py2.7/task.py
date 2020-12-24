# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/task.py
# Compiled at: 2016-10-03 09:39:22
"""
The bauble.task module allows you to queue up long running tasks. The
running tasks still block but allows the GUI to update.
"""
import fibra, gtk, bauble, logging
logger = logging.getLogger(__name__)
schedule = fibra.schedule()
__running = False
__kill = False
__message_ids = None

def running():
    """
    Return True/False if a task is running.
    """
    global __running
    return __running


def kill():
    """
    Kill the current task.

    This will kill the task when it goes idle and not while it's
    running.  A task is idle after it yields.
    """
    global __kill
    __kill = True


def _idle():
    """
    Called when a task is idle.
    """
    global __kill
    while gtk.events_pending():
        gtk.main_iteration(block=False)

    if __kill:
        __kill = False
        raise StopIteration()


schedule.register_idle_func(_idle)

def queue(task):
    """Run a task.

    task should be a generator with side effects. it does not matter what it
    yields, it is important that it does stop from time to time yielding
    whatever it wants to, and causing the side effect it has to cause.

    """
    global __running
    schedule.install(task)
    if bauble.gui is not None:
        bauble.gui.set_busy(True)
        bauble.gui.progressbar.show()
        bauble.gui.progressbar.set_pulse_step(1.0)
        bauble.gui.progressbar.set_fraction(0)
    __running = True
    try:
        try:
            schedule.run()
            __running = False
        except:
            raise

    finally:
        __running = False
        if bauble.gui is not None:
            bauble.gui.progressbar.set_pulse_step(0)
            bauble.gui.progressbar.set_fraction(0)
            bauble.gui.progressbar.hide()
            bauble.gui.set_busy(False)
        clear_messages()

    return


__message_ids = []

def set_message(msg):
    """
    A convenience function for setting a message on the
    statusbar. Returns the message id
    """
    global __message_ids
    global _context_id
    if bauble.gui is None or bauble.gui.widgets is None:
        return
    try:
        _context_id
    except NameError as e:
        logger.info(e)
        _context_id = bauble.gui.widgets.statusbar.get_context_id('__task')
        logger.info('new context id: %s' % _context_id)

    msg_id = bauble.gui.widgets.statusbar.push(_context_id, msg)
    __message_ids.append(msg_id)
    return msg_id


def clear_messages():
    """
    Clear all the messages from the statusbar that were set with
    :func:`bauble.task.set_message`
    """
    if bauble.gui is None or bauble.gui.widgets is None or bauble.gui.widgets.statusbar is None:
        return
    for mid in __message_ids:
        bauble.gui.widgets.statusbar.remove(_context_id, mid)

    return