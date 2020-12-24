# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/examples/quickstart/app3.py
# Compiled at: 2016-06-26 14:14:34
from flask import Flask
from flask_admin import Admin, BaseView, expose

class MyView(BaseView):

    @expose('/')
    def index(self):
        return self.render('index.html')


app = Flask(__name__)
app.debug = True
admin = Admin(app, name='Example: Quickstart3')
admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(MyView(name='Hello 3', endpoint='test3', category='Test'))
if __name__ == '__main__':
    app.run()