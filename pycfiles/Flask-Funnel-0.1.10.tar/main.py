# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /prj/rehandalal/flask-funnel/docs/example/main.py
# Compiled at: 2013-11-08 08:38:16
from flask import Flask, render_template
from flask.ext.funnel import Funnel
app = Flask(__name__)
Funnel(app)
app.config['JAVA_BIN'] = '/usr/java/latest/bin/java'
app.config['LESS_PREPROCESS'] = True
app.config['SCSS_PREPROCESS'] = True
app.config['STYLUS_PREPROCESS'] = True
app.config['COFFEE_PREPROCESS'] = True
app.config['AUTOPREFIXER_ENABLED'] = True
app.config['CSS_BUNDLES'] = {'1': ('css/1.css', ), 
   '2': ('css/2.css', ), 
   '3': ('css/3.css', ), 
   '1-2': ('css/1.css', 'css/2.css'), 
   'less-1': ('less/1.less', ), 
   'less-2': ('less/2.less', ), 
   'less-2-3': ('less/2.less', 'less/3.less'), 
   'scss': ('scss/test1.scss', 'scss/test2.scss'), 
   'stylus': ('stylus/1.styl', 'stylus/2.styl')}
app.config['JS_BUNDLES'] = {'coffee': ('coffee/test1.coffee', 'coffee/test2.coffee')}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/example1')
def example1():
    """Debug enabled, basic template functions"""
    app.config['DEBUG'] = True
    return render_template('example1.html')


@app.route('/example2')
def example2():
    """Debug enabled, LESS files"""
    app.config['DEBUG'] = True
    return render_template('example2.html')


@app.route('/example3')
def example3():
    """Debug enabled, LESS files"""
    app.config['DEBUG'] = True
    return render_template('example3.html')


@app.route('/example4')
def example4():
    """Debug enabled, LESS files"""
    app.config['DEBUG'] = True
    return render_template('example4.html')