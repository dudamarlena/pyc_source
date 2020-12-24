# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/system/who.py
# Compiled at: 2017-04-23 10:30:41
import json, subprocess

class Who(object):

    @classmethod
    def _run_command(cls, command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.stdout.readlines()

    def __init__(self, hostname):
        self.get(hostname)
        self.parse()
        self.data = None
        self.result = None
        self.cache = {}
        return

    def get(self, hostname):
        self.result = self._run_command(['ssh', hostname, 'who'])
        return self.result

    def parse(self):
        if self.result is None:
            self.data = None
        else:
            self.data = []
            for line in self.result:
                host = line.split('(')[1][:-1].replace(')', '')
                name = line.split()[0]
                self.data.append({'name': name, 
                   'host': host})

        return self.data

    def __str__(self):
        return json.dumps(self.data, indent=4)

    def sanitize_whois(self, lines):
        content = ('').join(lines)
        if 'NOTICE:' in content:
            return
        else:
            result = {}
            data = [ l for l in lines if ':' in l ]
            for element in data:
                if 'Access to Public Interest Registry' not in element:
                    attribute, value = element.split(':', 1)
                result[attribute] = value.strip('\n')

            return result
            return

    def whois(self):
        for entry in self.data:
            print (
             'EEE', entry)
            host = entry['host']
            if '.edu' in host or '.org' in host:
                host = host.split('.')
                host = ('.').join(host[-2:])
                print host
            entry['domain'] = host
            if host in self.cache:
                data = self.cache[host]
            else:
                data = self._run_command(['whois', host])
                self.cache[host] = data
            entry['whois'] = self.sanitize_whois(data)


def main():
    host = 'juliet'
    who = Who(host)
    who.whois()
    from pprint import pprint
    pprint(who.data)


if __name__ == '__main__':
    main()