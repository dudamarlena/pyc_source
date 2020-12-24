# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/adagios/adagios/profiling.py
# Compiled at: 2018-05-16 10:07:32
import hotshot, os, time, settings, tempfile, random
try:
    PROFILE_LOG_BASE = settings.PROFILE_LOG_BASE
except:
    PROFILE_LOG_BASE = tempfile.gettempdir()

def profile(log_file):
    """Profile some callable.

    This decorator uses the hotshot profiler to profile some callable (like
    a view function or method) and dumps the profile data somewhere sensible
    for later processing and examination.

    It takes one argument, the profile log name. If it's a relative path, it
    places it under the PROFILE_LOG_BASE. It also inserts a time stamp into the 
    file name, such that 'my_view.prof' become 'my_view-20100211T170321.prof', 
    where the time stamp is in UTC. This makes it easy to run and compare 
    multiple trials.     
    """
    if not os.path.isabs(log_file):
        log_file = os.path.join(PROFILE_LOG_BASE, log_file)

    def _outer(f):

        def _inner(*args, **kwargs):
            base, ext = os.path.splitext(log_file)
            base = base + '-' + time.strftime('%Y%m%dT%H%M%S', time.gmtime()) + str(random.randint(1, 9999))
            final_log_file = base + ext
            prof = hotshot.Profile(final_log_file)
            try:
                ret = prof.runcall(f, *args, **kwargs)
            finally:
                prof.close()

            return ret

        return _inner

    return _outer