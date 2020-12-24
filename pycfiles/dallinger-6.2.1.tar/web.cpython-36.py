# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger_scripts/web.py
# Compiled at: 2020-04-26 19:37:24
# Size of source mod 2**32: 270 bytes
"""Launch the experiment server."""

def main():
    import gevent.monkey
    gevent.monkey.patch_all()
    from dallinger.experiment_server.gunicorn import launch
    launch()


if __name__ == '__main__':
    main()