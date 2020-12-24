# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/asyncluster/master/database.py
# Compiled at: 2007-07-24 13:41:19
"""
Persistent data concerning control and records of user access.
"""
import time
from datetime import date, timedelta
from twisted.internet import defer
from sasync.database import transact, AccessBroker, SA

class UserDataTransactor(AccessBroker):
    """
    I manage control and records data for user access accounts.
    """
    __module__ = __name__

    def startup(self):
        """
        Ensures that all necessary tables are in place and accessible via
        instance variables before the first transaction runs.
        """
        self._activeSessionStartTimes = {}
        d1 = self.table('users', SA.Column('id', SA.String(20), primary_key=True), SA.Column('password', SA.String(40), nullable=False), SA.Column('enabled', SA.Boolean, default=True, nullable=False), SA.Column('restricted', SA.Boolean, default=True, nullable=False), SA.Column('daily_hours', SA.Float), SA.Column('weekly_hours', SA.Float))
        d2 = self.table('openings', SA.Column('weekday', SA.Integer, primary_key=True), SA.Column('start_hour', SA.Float(2), primary_key=True), SA.Column('end_hour', SA.Float(2), primary_key=True))
        d3 = self.table('timesheet', SA.Column('user_id', SA.String(20), primary_key=True), SA.Column('date', SA.Date, primary_key=True), SA.Column('start_hour', SA.Float, primary_key=True), SA.Column('end_hour', SA.Float, primary_key=True))
        return defer.DeferredList([d1, d2, d3])

    def recordSessionStartTime(self, userID):
        thisHour = self._timeToFloat(self._localtime())
        self._activeSessionStartTimes[userID] = thisHour

    def retrieveSessionStartTime(self, userID):
        return self._activeSessionStartTimes.pop(userID, None)

    @transact
    def sessionAuthorized(self, userID, userPassword):
        """
        Returns a deferred that fires with C{True} if the user is authorized
        and enabled, or C{False} if not.
        """
        if not self.s('authorization'):
            col = self.users.c
            self.s([col.enabled], SA.and_(col.id == SA.bindparam('ID'), col.password == SA.bindparam('password')))
        row = self.s().execute(ID=userID, password=userPassword).fetchone()
        if row is None or not row['enabled']:
            return False
        return True

    @transact
    def sessionStart(self, userID):
        """
        Begins an account's access session if any time remains for it. Returns
        the number of hours remaining for access today, if so, or 0.0
        otherwise.
        """
        timesLeft = [
         self.openingTimeLeft()]
        if timesLeft[0] <= 0:
            return 0.0
        timesLeft.append(self.accountTimeLeft(userID))
        timeLeft = min(timesLeft)
        return timeLeft

    @transact
    def sessionEnd(self, userID):
        """
        Ends an account's access session, inserting a new database record to
        account for the account's usage during the session.
        """
        started = self.retrieveSessionStartTime(userID)
        if started is not None:
            ended = self._timeToFloat(self._localtime())
            self.timesheet.insert().execute(user_id=userID, date=self._today(), start_hour=started, end_hour=ended)
        return

    @transact
    def openingTimeLeft(self):
        """
        Returns as a float the hours left in the current usage opening, if any.
        """
        if not self.s('pertinentOpenings'):
            col = self.openings.c
            self.s([col.end_hour], SA.and_(col.weekday == SA.bindparam('weekday'), col.start_hour < SA.bindparam('startsBy')))
        thisWeekday = self._weekday()
        thisHour = self._timeToFloat(self._localtime())
        rows = self.s().execute(weekday=thisWeekday, startsBy=thisHour).fetchall()
        currentOpenings = [
         0.0]
        for row in rows:
            if thisHour < row['end_hour']:
                currentOpenings.append(row['end_hour'] - thisHour)

        return max(currentOpenings)

    @transact
    def accountTimeLeft(self, userID):
        """
        Returns as a float the hours the identified user has left given the
        user's daily and weekly quotas, the usage records, and the current
        date and time.
        """
        if self._activeSessionStartTimes.has_key(userID):
            return 0.0
        if not self.s('userTime'):
            col = self.users.c
            self.s([col.daily_hours, col.weekly_hours], col.id == SA.bindparam('ID'))
        row = self.s().execute(ID=userID).fetchone()
        if row is None:
            return 0.0
        timesLeft = []
        timeLeftToday = row['daily_hours'] - self._timeLoggedToday(userID)
        if timeLeftToday <= 0.0:
            return 0.0
        timesLeft.append(timeLeftToday)
        timeLeftThisWeek = row['weekly_hours'] - self._timeLoggedThisWeek(userID)
        timesLeft.append(timeLeftThisWeek)
        return min(timesLeft)

    def _timeLoggedToday(self, userID):
        """
        Returns as a float the number of hours the user has already logged in
        previous sessions today.
        """
        if not self.s('usageToday'):
            col = self.timesheet.c
            self.s([col.start_hour, col.end_hour], SA.and_(col.user_id == SA.bindparam('userID'), col.date == SA.bindparam('date')))
        rows = self.s().execute(userID=userID, date=self._today()).fetchall()
        return sum([ x['end_hour'] - x['start_hour'] for x in rows ])

    def _timeLoggedThisWeek(self, userID):
        """
        Returns as a float the number of hours the user has already logged in
        previous sessions this week.
        """
        if not self.s('usageThisWeek'):
            col = self.timesheet.c
            self.s([col.start_hour, col.end_hour], SA.and_(col.user_id == SA.bindparam('userID'), col.date >= SA.bindparam('dateFirst'), col.date <= SA.bindparam('dateLast')))
        thisWeekday = self._weekday()
        thisWeekFirstDay = self._today() - timedelta(thisWeekday)
        thisWeekLastDay = thisWeekFirstDay + timedelta(6)
        rows = self.s().execute(userID=userID, dateFirst=thisWeekFirstDay, dateLast=thisWeekLastDay).fetchall()
        return sum([ x['end_hour'] - x['start_hour'] for x in rows ])

    def _timeToFloat(self, timeObject):
        (hours, minutes) = timeObject[3:5]
        return float(hours) + float(minutes) / 60

    def _today(self):
        return date.today()

    def _weekday(self):
        return self._today().weekday()

    def _localtime(self):
        return time.localtime()

    @transact
    def enabled(self, userID, isOrNot):
        """
        Sets the user's session access to enabled if I{isOrNot} is C{True} or
        disabled otherwise.
        """
        self.users.update(self.users.c.id == userID).execute(enabled=isOrNot)

    @transact
    def restricted(self, userID, isOrNot=None):
        """
        If I{isOrNot} is specified, sets the user's session access to
        restricted if it is C{True} or unrestricted if C{False}.

        Otherwise, returns a boolean indicating if the user is currently
        restricted.
        
        """
        if isOrNot is None:
            if not self.s('userRestricted'):
                col = self.users.c
                self.s([col.restricted], col.id == SA.bindparam('ID'))
            row = self.s().execute(ID=userID).fetchone()
            return row is None or row['restricted']
        self.users.update(self.users.c.id == userID).execute(restricted=isOrNot)
        return

    @transact
    def password(self, userID, password):
        """
        Sets the password for a user session account.  If the account doesn't
        already exist, it will be created.  A new account is disabled and
        restricted by default.
        """
        if self.userExists(userID):
            self.users.update(self.users.c.id == userID).execute(password=password)
        else:
            self.users.insert().execute(id=userID, password=password, enabled=False, restricted=True)

    @transact
    def deleteUser(self, userID, all=False):
        """
        Deletes the user's entry in the I{users} table. If the I{all} keyword
        is set to C{True} then the user's entries in the I{timesheet} table are
        also deleted.
        
        This method is mostly useful for testing user account creation. It
        is probably better practice not to delete users, but rather just to
        disable them.
        """
        self.users.delete(self.users.c.id == userID).execute()
        if all:
            self.timesheet.delete(self.timesheet.c.user_id == userID).execute()

    @transact
    def userExists(self, userID):
        """
        Returns a deferred that fires with C{True} if the named user exists,
        or with C{False} otherwise.
        """
        if not self.s('userExists'):
            col = self.users.c
            self.s([col.enabled], col.id == SA.bindparam('ID'))
        row = self.s().execute(ID=userID).fetchone()
        if row is None:
            return False
        return True