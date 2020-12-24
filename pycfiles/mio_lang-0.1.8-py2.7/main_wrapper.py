# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/main_wrapper.py
# Compiled at: 2013-12-04 07:18:22
try:
    from coverage import coverage
    HAS_COVERAGE = True
except ImportError:
    HAS_COVERAGE = False

if __name__ == '__main__':
    try:
        if HAS_COVERAGE:
            _coverage = coverage(data_suffix=True)
            _coverage.start()
        from mio.main import entrypoint
        entrypoint()
    finally:
        if HAS_COVERAGE:
            _coverage.stop()
            _coverage.save()