# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mougeon/core/model.py
# Compiled at: 2012-03-13 12:39:51
"""
Created on 01 March 2012 04:19:29

@author: maemo
"""
import subprocess, logging
from datetime import datetime
from persistence import dao
from utils import *
from ..common import version
version.getInstance().submitRevision('$Revision: 47 $')

class Settings:
    """
    Represents the settings for Gnatirac
    """

    def __init__(self):
        pass


class Operator:
    """
    Define a cellular operator
    """

    def __init__(self, name, code, country):
        """
        Parameters:
            - code is a list of integer
            - country is a list of integer
        """
        self.name = name
        self.code = code
        self.country = country

    def is_operator_code(self, code):
        return code in self.code

    def is_operator_country(self, country):
        return country in self.country


class FreeMobile(Operator):
    """
    Free mobile operator
    """

    def __init__(self):
        Operator.__init__(self, 'Free', FREE_MOBILE_OP_CODE, FREE_MOBILE_COUNTRY)


class Orange(Operator):
    """
    Orange operateur used on roaming by Free Mobile
    """

    def __init__(self):
        Operator.__init__(self, 'Orange', ORANGE_OP_CODE, ORANGE_COUNTRY)


FREE_OPERATOR = FreeMobile()
ORANGE_OPERATOR = Orange()

class RegisteredOp:
    """
    Simple structure to read registered operator
    """
    code = None
    country = None

    def __str__(self):
        return '%s %s' % (self.code, self.country)


def get_current_op(raw=False):
    """
    Return the current operator
    """
    resu = None
    p = subprocess.Popen(["dbus-send --system --print-reply --dest=com.nokia.phone.net /com/nokia/phone/net Phone.Net.get_registration_status | awk 'NR==5 || NR==6 {print $2}'"], shell=True, stdout=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    registered_op = RegisteredOp()
    lines = stdout.splitlines(False)
    if len(lines) > 0:
        registered_op.code = lines[0]
        registered_op.country = lines[1]
    if raw:
        return registered_op
    elif FREE_OPERATOR.is_operator_code(registered_op.code) and FREE_OPERATOR.is_operator_country(registered.country):
        resu = FREE_OPERATOR
    else:
        resu = ORANGE_OPERATOR
    logging.info('current registered op %s' % str(stdout))
    return resu


class ITrackerListener:

    def record_operator(self, tracker, tct):
        raise NotImplementedError()


class Tracker:
    """
    This class can track cell tower used 
    """
    stop_request = False
    async_task = None
    record_listener = []

    def reset_data(self):
        dao.TrackedCellTower.clear(cnx=None)
        return

    def add_listener(self, aListener):
        """
        Subscribe a listener on this trcaker
        """
        self.record_listener.append(aListener)

    def remove_listener(self, aListener):
        """
        Subscribe a listener on this trcaker
        """
        self.record_listener.remove(aListener)

    def _record(self):
        registered_op = get_current_op(True)
        tct = dao.TrackedCellTower()
        tct.opId = registered_op.code
        tct.country = registered_op.country
        tct.timestamp = datetime.now().strftime('%Y-%m(%d %H:%M:%S')
        tct.create(cnx=None)
        logging.debug('Cell tower %s recorded' % (str(registered_op),))
        map(lambda l: l.record_operator(self, tct), self.record_listener)
        return

    def _stop_hook(self):
        self.stop_request = True

    def _record_for_ever(self):
        import time
        SLEEP_DELAY = 300
        now = None
        next = None
        while not self.stop_request:
            if not next:
                next = time.time()
            now = time.time()
            if now >= next:
                next = now + SLEEP_DELAY
                self._record()
            time.sleep(5)

        raise StopSignalException()
        return

    def record(self, background=False):
        """
        Record current operator
        """
        if background:
            self.async_task = AsyncTask(self._stop_hook, self._record_for_ever)
            self.async_task.start()
        else:
            self._record()

    def stop_record(self):
        self.async_task.send_stop_signal()

    def free_mobile_record(self):
        """
        Return the number of record for Free Mobile Cell Tower
        """
        return dao.TrackedCellTower.free_mobile_record(cnx=None)

    def orange_record(self):
        """
        Return the number of record for Orange Cell Tower
        """
        return dao.TrackedCellTower.orange_record(cnx=None)

    def number_of_record(self):
        """
        Return the number of record
        """
        return dao.TrackedCellTower.total_record(cnx=None)


TRACKER_INSTANCE = Tracker()