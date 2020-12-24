# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.1/dist-packages/cbstats/__init__.py
# Compiled at: 2011-03-13 18:23:38
import re, time, datetime, collections, os

class CraftBukkitStats:

    def __init__(self, bukkit_folder=False):
        """ 
        Init function, keeps and sets environment specific settings. Ski at your own risk. """
        if not bukkit_folder:
            raise Exception('No bukkit folder location arbument passed to CraftBukkitStats. use cbstats.CraftBukkitStats("/home/user/bukkit_folder/)')
        if not os.access(str(bukkit_folder), os.R_OK):
            raise Exception('User does not have access to "{folder}", it might not exist or you might not have sufficient read permissions'.format(folder=bukkit_folder))
        self.bukkit_folder = bukkit_folder
        self.file_server_log = self.bukkit_folder + 'server.log'
        self.file_server_operators_file = self.bukkit_folder + 'ops.txt'
        self.file_server_properties = self.bukkit_folder + 'server.properties'
        self.file_server_whitelist = self.bukkit_folder + 'white-list.txt'

    def get_operators(self):
        """ Returns operators entered in the ops.txt file """
        f = open(self.file_server_operators_file, encoding='utf-8')
        lines = f.read().splitlines()
        operators = list()
        for line in lines:
            operators.append(line)

        return operators

    def get_whitelist(self):
        """ Returns a list containing nicknames present in whitelist """
        f = open(self.file_server_whitelist, encoding='utf-8')
        lines = f.read().splitlines()
        whitelist = list()
        for line in lines:
            whitelist.append(line)

        return whitelist

    def get_properties(self):
        """ Returns server properties found in the server.properties file """
        self.update_properties()
        return self.configuration

    def update_properties(self):
        f = open(self.file_server_properties, encoding='utf-8')
        lines = f.read().splitlines()
        self.configuration = dict()
        for line in lines:
            matchConfiguration = re.search('^(?P<key>.*)=(?P<value>.*)$', line)
            if matchConfiguration:
                self.configuration[matchConfiguration.group('key')] = matchConfiguration.group('value')
                continue

    def get_property(self, property):
        """ Returns named property if it is found in the server.properties file """
        self.update_properties()
        try:
            return self.configuration[property]
        except KeyError:
            return False

    def get_connected(self):
        """ Returns a dictionary of the currently connected users.
        Example:
        
        """
        try:
            return self.connected
        except AttributeError:
            self.get_usage_stats()
            return self.connected

    def get_usage_stats(self):
        """ Returns statistics about the users of the server """
        f = open(self.file_server_log, encoding='utf-8')
        lines = f.read().splitlines()
        self.connected = dict()
        times = list()
        self.connected_log = list()
        connected_time_average = float()
        connected_time_per_user = dict()
        for line in lines:
            match_connect = re.search('^(?P<date>[0-9-]+) (?P<time>[0-9:]+) (.*) (?P<user>\\w+) \\[/(?P<address>[0-9.:]+)\\] logged', line)
            if match_connect:
                groups = match_connect.groups()
                self.connected_log.append('{date} {time} {name} connected'.format(debug=groups, date=match_connect.group('date'), time=match_connect.group('time'), name=match_connect.group('user')))
                time_connect = time.strptime(match_connect.group('date') + ' ' + match_connect.group('time'), '%Y-%m-%d %H:%M:%S')
                self.connected[match_connect.group('user')] = time_connect
            match_disconnect = re.search('^(?P<date>[0-9-]+) (?P<time>[0-9:]+) (.*) (?P<user>\\w+) lost connection: disconnect\\.(\\w+)$', line)
            if match_disconnect:
                time_disconnect = time.strptime(match_disconnect.group('date') + ' ' + match_disconnect.group('time'), '%Y-%m-%d %H:%M:%S')
                delta = time.mktime(time_disconnect) - time.mktime(self.connected[match_disconnect.group('user')])
                delta_format = datetime.timedelta(seconds=int(delta))
                self.connected_log.append('{date} {time} {name} disconnected ({delta})'.format(date=match_disconnect.group('date'), time=match_disconnect.group('time'), name=match_disconnect.group('user'), delta=delta_format))
                times.append({'user': match_disconnect.group('user'),  'time': delta})
                del self.connected[match_disconnect.group('user')]
                continue

        connected_time_total = float()
        connected_time_total_discarded = 0
        connected_time_per_user = dict()
        for connected_time in times:
            if connected_time['time'] > 120:
                connected_time_total += connected_time['time']
            else:
                connected_time_total_discarded += 1
            if connected_time['user'] not in connected_time_per_user:
                connected_time_per_user[connected_time['user']] = connected_time['time']
            else:
                connected_time_per_user[connected_time['user']] += connected_time['time']

        connected_time_average = connected_time_total / (len(times) - connected_time_total_discarded)
        connected_time_per_user = collections.OrderedDict(sorted(connected_time_per_user.items(), key=lambda t: t[1], reverse=True))
        return {'connectedAverage': connected_time_average, 
         'timePerUser': connected_time_per_user}


if __name__ == '__main__':
    stats = CraftBukkitStats('/home/jwandborg/bukkit-1.3/')
    usageStats = stats.get_usage_stats()
    print('# Server stats for mc.wandborg.se\n\nOperators: {ops}\n\nOnline right now: {users_connected}\n\nAverage user session length: {average_session_length}\n'.format(average_session_length=datetime.timedelta(seconds=int(usageStats['connectedAverage'])), timezone='UTC', ops=', '.join(stats.get_operators()), users_connected=', '.join(stats.connected)))
    print('# Toplist - Time online\n')
    for user, time in usageStats['timePerUser'].items():
        print('{time} {user}'.format(time=datetime.timedelta(seconds=int(time)), user=user))

    if not len(usageStats['timePerUser']):
        print('No users have connected yet')
    print('\n# Configuration\n')
    for key, value in stats.get_properties().items():
        print('{key}: {value}'.format(key=key, value=value))