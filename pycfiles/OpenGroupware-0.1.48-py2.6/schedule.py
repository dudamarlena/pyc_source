# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/schedule.py
# Compiled at: 2012-10-12 07:02:39
import yaml

class Schedule(object):

    def _amq_callback(self, uuid, source, target, data):
        self.log.debug('Schedule presentation received callback.')
        self.parse_schedule(data)
        return True

    def get_schedule(self):
        self.context.run_command('process::get-schedule', callback=self._amq_callback)
        self.log.debug('Schedule presentation requested workflow schedule')
        self.context.wait()

    def parse_schedule(self, data):
        if data is not None:
            if data.get('status', 500) == 200:
                self.log.debug(('parsing workflow schedule in "{0}" mode.').format(self.mode))
                result = []
                result.append({'comment': ''})
                for entry in data.get('schedule'):
                    if self.mode == 'cron' and entry[4] == 'crontab':
                        result.append({'UUID': entry[0], 'routeId': entry[1], 
                           'contextId': entry[2], 
                           'year': entry[5][0], 
                           'month': entry[5][1], 
                           'day': entry[5][2], 
                           'dayofweek': entry[5][3], 
                           'hour': entry[5][4], 
                           'minute': entry[5][5]})
                    elif self.mode == 'interval' and entry[4] == 'interval':
                        result.append({'UUID': entry[0], 'routeId': entry[1], 
                           'contextId': entry[2], 
                           'days': entry[5][0], 
                           'hours': entry[5][1], 
                           'minutes': entry[5][2], 
                           'seconds': entry[5][3], 
                           'start': entry[5][4], 
                           'repeat': entry[5][5]})
                    elif self.mode == 'calendar' and entry[4] == 'date':
                        result.append({'UUID': entry[0], 'routeId': entry[1], 
                           'contextId': entry[2], 
                           'date': entry[3]})

            self.log.debug(('found {0} items in workflow schedule for this mode').format(len(result) - 1))
            self.schedule = result
        return

    def diff_schedule(self, new):
        if self.schedule is None:
            self.get_schedule()
            if self.schedule is None:
                raise CoilsException('Unable to marshal workflow schedule for comparison')
        update = []
        delete = []
        for nentry in new:
            if 'routeId' not in nentry:
                continue
            if 'UUID' in nentry:
                for oentry in self.schedule:
                    if 'UUID' in oentry:
                        if oentry['UUID'] == nentry['UUID']:
                            break

            else:
                update.append(nentry)

        for oentry in self.schedule:
            if 'UUID' in oentry:
                for nentry in new:
                    if nentry.get('UUID', '---') == oentry['UUID']:
                        break

            else:
                delete.append(oentry)

        return {'update': update, 'delete': delete}

    def parse_payload(self, payload):
        data = yaml.load(payload)
        self.log.debug(data)
        for entry in data:
            if 'routeId' in entry:
                d = {'routeId': entry['routeId']}
                d['contextId'] = entry.get('contextId', self.context.account_id)
                if d['contextId'] not in self.context.context_ids:
                    raise CoilsException('Cannot create process for an unrelated context')
                if 'UUID' in entry:
                    d['UUID'] = entry['UUID']
                if self.mode == 'crontab':
                    d['year'] = str(entry.get('year', '*'))
                    d['month'] = str(params.get('month', '*'))
                    d['day'] = str(params.get('day', '*'))
                    d['weekday'] = str(params.get('dayofweek', '*'))
                    d['hour'] = str(params.get('hour', '*'))
                    d['minute'] = str(params.get('minute', '*'))
                elif self.mode == 'interval':
                    pass
                elif self.mode == 'date':
                    if date in entry:
                        d['date'] = entry['date']
                result.append(d)

        return result

    def render_schedule(self):
        self.log.debug(('rendering workflow schedule for "{0}" mode.').format(self.mode))
        return yaml.dump(self.schedule)

    def update_schedule(self, mode, data):
        new = self.parse_payload(data)