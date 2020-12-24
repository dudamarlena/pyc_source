# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/Seeti/core/storage.py
# Compiled at: 2012-04-16 00:14:12
import datetime, getpass, os, sqlite3, sys

class Manager(object):

    def __init__(self, path='.seeti'):
        self.path = path

    def init(self):
        """
        Creates a the database file if it does not exist, creates the entries 
        table and inserts a init entry on it.
        
        Returns True if succeeded.
        """
        try:
            if not os.path.exists(self.path):
                connection = sqlite3.connect(self.path)
                cursor = connection.cursor()
                cursor.execute('CREATE TABLE entries (id INTEGER PRIMARY KEY, type TEXT, datetime TEXT)')
                cursor.execute('INSERT INTO entries (type, datetime) VALUES (?, ?)', ('init', datetime.datetime.now()))
                connection.commit()
                connection.close()
                return True
            raise RuntimeError('Seeti was already initialized!')
        except sqlite3.Error:
            raise IOError("An error occurred while trying to create the .seeti file.\nCheck if you've got write permissions on this directory.\n")

    def start(self):
        """
        Inserts a 'start' entry in the database file if already there isn't one, 
        or if the last entry is a 'stop' one.
        
        Returns True if succeeded.
        """
        if self.is_initialized():
            if self.is_open():
                if self.is_stopped() or not self.is_started():
                    self._create_entry('start')
                    return True
                raise RuntimeError('Seeti is already started!')
            else:
                raise RuntimeError('Seeti is closed. Open or restart the project, then execute the start command again.')
        else:
            raise RuntimeError('Seeti was not initiated. You need to run the init command to do so.')

    def stop(self):
        """
        Inserts a 'stop' entry in the database file if the last entry is a 'start' one.
        
        Returns True if succeeded.
        """
        if self.is_initialized():
            if self.is_open():
                if self.is_started():
                    self._create_entry('stop')
                    return True
                raise RuntimeError('Seeti is not started!')
            else:
                raise RuntimeError('Seeti is closed. Open or restart the project, then execute the start command again.')
        else:
            raise RuntimeError('Seeti was not initiated. You need to run the init command to do so.')

    def report(self):
        """
        Computes the difference of all the 'start's and 'stops's, sums them and then returns the total 
        as a timedelta object.
        
        If the last command issued was a 'start', the last 'stop' is the current datetime.
        """
        if self.is_initialized():
            format = '%Y-%m-%d %H:%M:%S.%f'
            starts = [ datetime.datetime.strptime(entry[1], format) for entry in self.get_entries('start') ]
            stops = [ datetime.datetime.strptime(entry[1], format) for entry in self.get_entries('stop') ]
            if self.is_started():
                stops.append(datetime.datetime.now())
            timedelta = datetime.timedelta()
            for i in xrange(len(starts)):
                timedelta += stops[i] - starts[i]

            return timedelta
        raise RuntimeError('Seeti was not initiated. You need to run the init command to do so.')

    def get_status(self):
        """
        Returns the latest entry type formatted - started, stopped, closed or, initialized.
        """
        if self.is_initialized():
            statuses = {'start': 'started', 'stop': 'stopped', 'init': 'initialized', 
               'close': 'closed', 
               'open': 'open'}
        try:
            entry = self.get_entry(latest=True)[0]
        except:
            return False

        return statuses.get(entry)

    def close(self):
        """
        Inserts a 'close' entry in the database if it's not already closed, and is stopped.
        
        Returns True if succeeded. 
        """
        if self.is_initialized():
            if self.get_status() == 'open' or self.is_stopped():
                self._create_entry('close')
                return True
            raise RuntimeError('Seeti is not stopped or open.')
        else:
            raise RuntimeError('Seeti was not initiated. You need to run the init command to do so.')

    def open(self):
        """
        Inserts an 'open' entry if is initialized and not open.
        Returns True if succeed.
        """
        if self.is_initialized():
            if not self.is_open():
                self._create_entry('open')
                return True
            raise RuntimeError("Seeti isn't closed.")
        else:
            raise RuntimeError('Seeti was not initiated. You need to run the init command to do so.')

    def restart(self):
        """
        Deletes all entries, except the 'init' one and updates it to the current datetime
        if self.is_open() returns False.
        
        Returns True if succeed.
        """
        if self.is_initialized():
            if not self.is_open():
                connection = sqlite3.connect(self.path)
                cursor = connection.cursor()
                cursor.execute('DELETE FROM entries WHERE type != ?', ('init', ))
                cursor.execute('UPDATE entries SET datetime = ? WHERE type = ?', (
                 datetime.datetime.now(), 'init'))
                connection.commit()
                connection.close()
                return True
            raise RuntimeError("Seeti isn't closed.")
        else:
            raise RuntimeError('Seeti was not initiated. You need to run the init command to do so.')

    def remove(self):
        """
        Removes the database file if it exists.
        """
        try:
            if self.is_initialized():
                os.remove(self.path)
            else:
                raise RuntimeError('Seeti was not initiated. Nothing to be done.')
            return True
        except OSError as e:
            raise OSError("An error occurred while trying to remove the %s file. Check if you've got write permissions on this directory." % e.filename)

    def get_rowcount(self):
        """
        Returns an integer representing the amount of rows in the database.
        """
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM entries')
        rowcount = len(cursor.fetchall())
        connection.commit()
        connection.close()
        return rowcount

    def is_initialized(self):
        """
        Returns True if there is a database file and there's an 'init' entry on it. 
        Returns False otherwise.
        """
        if os.path.exists(self.path):
            entry = self.get_entry('init')[0]
            return entry == 'init'
        return False

    def is_open(self):
        """
        Returns True if it's initialized and the last entry isn't a 'close' one. 
        Returns False otherwise.
        """
        init = self.is_initialized()
        closed = self.get_status() == 'closed'
        return init and not closed

    def is_started(self):
        """
        Returns True if the last entry is a 'start' one. Returns False otherwise.
        """
        return self.get_status() == 'started'

    def is_stopped(self):
        """
        Returns True if the last entry is a 'stop' one. Returns True otherwise.
        """
        return self.get_status() == 'stopped'

    def _create_entry(self, type):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO entries (type, datetime) VALUES (?, ?)', (type, datetime.datetime.now()))
        connection.commit()
        connection.close()

    def _print_all_entries(self):
        """
        Prints all the entries. 
        
        Debug-purpose method only. 
        """
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute('SELECT type, datetime FROM entries')
        print 'all entries', cursor.fetchall()
        connection.close()

    def get_entry(self, type='', latest=True):
        """
        Searches for an entry in the database.
        
        If type if provided, returns this specific record if exists. 
        Otherwise returns the latest or first entry recorded, based on the 
        latest argument.
        
        None is returned if no entry is found.
        """
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        if type:
            cursor.execute('SELECT type, datetime FROM entries WHERE type = ?', (type,))
        else:
            cursor.execute('SELECT type, datetime FROM entries')
        entries = cursor.fetchall()
        connection.close()
        try:
            if latest:
                return entries[(-1)]
            else:
                return entries[0]

        except IndexError:
            return

        return

    def get_entries(self, type=''):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        if type:
            cursor.execute('SELECT type, datetime FROM entries WHERE type = ?', (type,))
        else:
            cursor.execute('SELECT type, datetime FROM entries')
        entries = cursor.fetchall()
        connection.close()
        return entries