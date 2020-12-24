# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\Project\webapp\test\views.py
# Compiled at: 2018-01-21 06:12:33
from models import User
from mwebapp.httperror import redirect
from mwebapp.webapp import Route, ctx, render_html, render_json, url_for
index = Route()

@index.get('/')
def home():
    return render_html('template/index.html', {})


@index.get('/api/')
def api():
    user_list = User.find_by('where id<?', 1000)
    return render_json(user_list)


@index.get('/redirect/')
def redirect_test():
    return redirect(url_for(admin_index.path, ('admin', )))


@index.route('/:name/')
def other(name):
    request = ctx.request
    if request.request_method == 'POST':
        file = request.get('test')
        with open(file.filename, 'wb') as (f):
            f.write(file.body)
    content = {'name': name, 
       'topics': [
                'Python', 'Geometry', 'Juggling']}
    return render_html('template/other.html', content)


admin = Route(startpath='/admin')

@admin.get('/:name/')
def admin_index(name):
    return '<h1>welcome %s to admin</h1>' % name