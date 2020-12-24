# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hgwebcommit/main.py
# Compiled at: 2011-10-28 23:12:30
if __name__ == '__main__':
    from hgwebcommit import app
    import os, sys, random
    if len(sys.argv) < 2:
        sys.stdout.write('python -m hgwebcommit directory\n')
        sys.exit()
    repository_path = os.path.abspath(sys.argv[1])
    app.config.update(DEBUG=True, SECRET_KEY=('').join([ random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#$&():;') for i in range(30) ]), HGWEBCOMMIT_REPOSITORY=repository_path, HGWEBCOMMIT_ENCODING='utf-8', HGWEBCOMMIT_ALLOW_COMMIT=True, HGWEBCOMMIT_ACTIONS=[])
    app.run(host='127.0.0.1')