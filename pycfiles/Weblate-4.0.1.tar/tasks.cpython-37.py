# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nijel/weblate/weblate/weblate/fonts/tasks.py
# Compiled at: 2020-03-12 04:44:12
# Size of source mod 2**32: 1372 bytes
from weblate.fonts.models import FONT_STORAGE, Font
from weblate.utils.celery import app

@app.task(trail=False)
def cleanup_font_files():
    """Remove stale fonts."""
    try:
        files = FONT_STORAGE.listdir('.')[1]
    except OSError:
        return
    else:
        for name in files:
            if name == 'fonts.conf':
                continue
            if not Font.objects.filter(font=name).exists():
                FONT_STORAGE.delete(name)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(86400,
      (cleanup_font_files.s()), name='font-files-cleanup')