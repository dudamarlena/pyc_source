# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/roster/roster.py
# Compiled at: 2018-07-19 13:18:03
# Size of source mod 2**32: 533 bytes
from flask import Flask, render_template
app = Flask(__name__)
Gs = [
 {'GPU_TASK_NO':'1', 
  'RUNNING_STATE':'FALSE', 
  'STOP_STATE':'FALSE', 
  'PAUSE_STATE':'FALSE'},
 {'GPU_TASK_NO':'2', 
  'RUNNING_STATE':'TRUE', 
  'STOP_STATE':'FALSE', 
  'PAUSE_STATE':'FALSE'}]

@app.route('/')
def home():
    return render_template('roster.html', Gs=Gs)


@app.route('/about')
def about():
    return '<h1>About</h1>'


if __name__ == '__main__':
    app.run(debug=True)