# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/freqkey/__init__.py
# Compiled at: 2019-03-25 07:56:18
# Size of source mod 2**32: 3801 bytes
__version__ = '0.0.3'
from argparse import ArgumentParser
from collections import Counter
from datetime import datetime, timedelta
from inputs import devices

class FreqKey:

    def __init__(self):
        self._start = datetime.now()
        self._last = self._start
        self._run = True
        self._ignore = ['yubikey']
        self._states = {0:'release', 
         1:'press', 
         2:'hold'}
        self._mods = {'KEY_LEFTSHIFT':False, 
         'KEY_LEFTCTRL':False, 
         'KEY_LEFTMETA':False, 
         'KEY_LEFTALT':False, 
         'KEY_RIGHTSHIFT':False, 
         'KEY_RIGHTCTRL':False, 
         'KEY_RIGHTMETA':False, 
         'KEY_RIGHTALT':False}
        self._mod_ctr = Counter()
        self._combo_ctr = Counter()
        self._single_ctr = Counter()
        self._keebs = []
        for kb in devices.keyboards:
            if not any((ign in str(kb).lower() for ign in self._ignore)):
                print('Found keyboard: {}'.format(str(kb)))
                self._keebs.append(kb)

    def setmods(self, event):
        self._mods[event.code] = event.state in (1, 2)

    def getmods(self):
        return tuple(sorted((k for k, v in self._mods.items() if v)))

    def ismod(self, event):
        return event.code in self._mods.keys()

    def write_stats(self, filename, now):

        def ctr_str(counter):

            def fmt(k, v):
                keys = ' + '.join(k).replace('KEY_', '').lower()
                return '  {:<60}{:>4}'.format(keys, v)

            return '\n'.join((fmt(k, v) for k, v in counter.most_common()))

        output = [
         f"freqkey version {__version__}\n",
         f"Started: {self._start} (duration {now - self._start})",
         '\n\nModifiers:\n',
         ctr_str(self._mod_ctr),
         '\n\nCombos:\n',
         ctr_str(self._combo_ctr),
         '\n\nSingles:\n',
         ctr_str(self._single_ctr)]
        if filename:
            with open(filename, 'w') as (file):
                file.writelines(output)
        else:
            print(''.join(output))

    def main(self, args):
        print('Recording events')
        while self._run:
            now = datetime.now()
            if now - self._last > args.update:
                self.write_stats(args.out, now)
                self._last = now
            events = []
            for kb in self._keebs:
                events.extend(kb.read())

            if events:
                keyev = filter(lambda ev: ev.ev_type == 'Key', events)
                for ev in keyev:
                    if self.ismod(ev):
                        self.setmods(ev)


def main():

    def mkupdt(sec):
        return timedelta(seconds=(int(sec)))

    ap = ArgumentParser()
    ap.add_argument('--out', help='Output file, defaults to stdout')
    ap.add_argument('--update', help='Update frequency in seconds, defaults to 60', type=mkupdt, default=timedelta(seconds=60))
    ap.add_argument('--version', action='version', version=__version__)
    args = ap.parse_args()
    fq = FreqKey()
    try:
        fq.main(args)
    except KeyboardInterrupt:
        print('Exiting')
        fq._run = False


if __name__ == '__main__':
    main()