# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thibault/Work/Recherche/F2/F2Python/f2web/f2_rest.py
# Compiled at: 2017-02-24 09:56:02
"""f2_rest : a REST API to access an F2 database.
   Th.Estier - aout 2014
   version 0.1
   
   uses web.py framework, a great piece of soft from Aaron Schwartz (see webpy.org)
"""
import web, F2
f2 = F2.connect('rpc:127.0.0.1:8081')
render = web.template.render('templates/', base='layout')
urls = ('/', 'index')

class index:
    """F2 server: root welcoming page"""

    def GET(self):
        i = web.input(dbName=None, clName=None)
        db = f2.Database(name=i.dbName)
        if db:
            db = db[0]
        cl = f2.CLASS(className=i.clName, db=db)
        if cl:
            cl = cl[0]
        return render.index(db, cl, f2)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()