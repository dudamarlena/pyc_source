# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /storage/Marcelo/codes/FluVigilanciaBR/fludashboard/fludashboard/app.py
# Compiled at: 2018-02-01 19:31:43
# Size of source mod 2**32: 292 bytes
from fludashboard.libs.views import app
from fludashboard import settings

def startup():
    """

    :return:
    """
    app.run(host=(settings.APP_HOST),
      port=(settings.APP_PORT),
      debug=(settings.DEBUG))
    return app


if __name__ == '__main__':
    startup()