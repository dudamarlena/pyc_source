# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zaggregator/daemon.py
# Compiled at: 2018-08-01 11:48:52
# Size of source mod 2**32: 1155 bytes
import asyncio, sys, os, zaggregator, time, setproctitle
from zaggregator import sqlite
if len(sys.argv) > 1:
    pidfile = sys.argv[1]
    with open(pidfile, 'w') as (fd):
        fd.write(str(os.getpid()))
delay = 29
loop = asyncio.get_event_loop()

def collect_data(bundle) -> (
 str, int, int, float):
    """  Collect data """
    return (
     bundle.bundle_name, bundle.ctx_vol,
     bundle.rss,
     bundle.pcpu)


def zag_sampler_loop(lc):
    """ Main sampler loop """
    loop, callback = lc
    loop.call_later(delay, callback, lc)
    pt = zaggregator.ProcTable()
    for b in pt.get_top_5s():
        sqlite.add_record((
         b.bundle_name,
         b.rss,
         b.vms,
         b.ctx_vol,
         b.ctx_invol,
         b.pcpu))


def start() -> None:
    """
        initialize and start main daemon loop
    """
    setproctitle.setproctitle('zaggregator')
    lc = (loop, callback)
    loop.call_later(delay, callback, lc)
    loop.run_forever()
    loop.close()


callback = zag_sampler_loop