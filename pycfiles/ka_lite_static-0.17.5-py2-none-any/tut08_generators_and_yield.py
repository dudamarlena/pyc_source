# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/tutorial/tut08_generators_and_yield.py
# Compiled at: 2018-07-11 18:15:31
"""
Bonus Tutorial: Using generators to return result bodies

Instead of returning a complete result string, you can use the yield
statement to return one result part after another. This may be convenient
in situations where using a template package like CherryPy or Cheetah
would be overkill, and messy string concatenation too uncool. ;-)
"""
import cherrypy

class GeneratorDemo:

    def header(self):
        return '<html><body><h2>Generators rule!</h2>'

    def footer(self):
        return '</body></html>'

    def index(self):
        users = [
         'Remi', 'Carlos', 'Hendrik', 'Lorenzo Lamas']
        yield self.header()
        yield '<h3>List of users:</h3>'
        for user in users:
            yield '%s<br/>' % user

        yield self.footer()

    index.exposed = True


import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')
if __name__ == '__main__':
    cherrypy.quickstart(GeneratorDemo(), config=tutconf)
else:
    cherrypy.tree.mount(GeneratorDemo(), config=tutconf)