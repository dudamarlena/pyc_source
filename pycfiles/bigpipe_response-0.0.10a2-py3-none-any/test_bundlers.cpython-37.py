# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\programming\eclipse_projects\bigpipe_response\bigpipe_response\js\test_bundlers.py
# Compiled at: 2019-12-31 14:49:56
# Size of source mod 2**32: 661 bytes
from webassets import Environment, Bundle
from webassets.filter import register_filter
from webassets_webpack import Webpack
register_filter(Webpack)
my_env = Environment(debug=False,
  directory='./node_modules',
  url='/')
js = Bundle('object-assign/index.js', 'react/cjs/react.production.min.js', 'react-dom/cjs/react-dom.production.min.js', 'create-react-class/create-react-class.min.js', filters='webpack',
  depends='js/**/*.js',
  output='D:\\programming\\eclipse_projects\\bigpipe_response\\bigpipe_response\\js\\dist\\1.js')
my_env.register('js_all', js)
print(my_env['js_all'].build()[0].data())