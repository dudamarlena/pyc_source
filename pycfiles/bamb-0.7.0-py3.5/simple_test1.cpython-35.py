# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/simple_test1.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 459 bytes
import celery, time
app = celery.Celery()

@app.task(bind=True)
def hello(self, a, b):
    time.sleep(1)
    self.update_state(state='PROGRESS', meta={'progress': 50})
    time.sleep(1)
    self.update_state(state='PROGRESS', meta={'progress': 90})
    time.sleep(1)
    return 'hello world: %i' % (a + b)


def on_raw_message(body):
    print(body)


r = hello.apply_async(4, 5)
print(type(r))
print(r.get(on_message=on_raw_message, propagate=False))