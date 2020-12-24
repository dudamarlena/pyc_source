# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/willdo/app.py
# Compiled at: 2008-04-22 18:15:31
import grok
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from willdo.interfaces import IDoItTomorrow, IWillDoList
import datetime

class ManageList(grok.Permission):
    __module__ = __name__
    grok.name('willdo.ManageList')
    grok.title('Manage willdo list')


class DoItTomorrow(grok.Application, grok.Container):
    __module__ = __name__
    implements(IDoItTomorrow)


class WillDo(grok.Model):
    __module__ = __name__
    implements(IWillDoList)

    def __init__(self, day=None):
        super(WillDo, self).__init__()
        if day is None:
            self.day = datetime.date.today()
        else:
            self.day = day
        self.tasks = PersistentList()
        self.closed = False
        return


class DoItTomorrowIndex(grok.View):
    __module__ = __name__
    grok.context(DoItTomorrow)
    grok.name('index')
    grok.require('willdo.ManageList')

    def update(self, day='', month='', year='', today=None, tomorrow=None):
        if today is None and tomorrow is None and day == '':
            return
        thisday = datetime.date.today()
        if today is not None:
            target = thisday
        if tomorrow is not None:
            target = datetime.date.fromordinal(thisday.toordinal() + 1)
        else:
            if day == '':
                day = thisday.day
            else:
                day = int(day)
            if month == '':
                month = thisday.month
            else:
                month = int(month)
            if year == '':
                year = thisday.year
            else:
                year = int(year)
            target = datetime.date(year, month, day)
        id = unicode(target.toordinal())
        if self.context.has_key(id):
            return
        self.context[id] = WillDo(day=target)
        return

    def entries(self):
        context = self.context
        contents = []
        for key in context.keys():
            info = dict(link=self.url(key), day=context[key].day)
            contents.append(info)

        return contents

    def todayslist(self):
        context = self.context
        thisday = datetime.date.today()
        key = unicode(thisday.toordinal())
        if key not in context.keys():
            return
        tl = context[key]
        info = dict(link=self.url(key), day=tl.day, tasks=tl.tasks, closed=tl.closed)
        return info


class WillDoIndex(grok.View):
    __module__ = __name__
    grok.context(WillDo)
    grok.name('index')
    grok.require('willdo.ManageList')

    def update(self, open=None, close=None, newtask=None):
        if open:
            self.context.closed = False
        if close:
            self.context.closed = True
        if newtask:
            if self.context.closed:
                pass
            else:
                new = dict(name=newtask, time=0, start=None)
                newdict = PersistentDict(new)
                self.context.tasks.append(newdict)
        now = datetime.datetime.utcnow()
        for key in self.request.form.keys():
            if key.startswith('start-'):
                started = [ task for task in self.context.tasks if task['start'] is not None ]
                for task in started:
                    diff = now - task['start']
                    task['time'] += int(round((now - task['start']).seconds / 60.0))
                    task['start'] = None

                try:
                    id = int(key[6:])
                except:
                    return
                else:
                    task = self.context.tasks[id]
                    task['start'] = now

        return


class Edit(grok.EditForm):
    __module__ = __name__
    grok.context(WillDo)
    grok.require('willdo.ManageList')