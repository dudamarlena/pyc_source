# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/inbound/app.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1203 bytes
"""Receiver module for processing SendGrid Inbound Parse messages.

See README.txt for usage instructions."""
try:
    from config import Config
except:
    from sendgrid.helpers.inbound.config import Config

try:
    from parse import Parse
except:
    from sendgrid.helpers.inbound.parse import Parse

from flask import Flask, request, render_template
import os
app = Flask(__name__)
config = Config()

@app.route('/', methods=['GET'])
def index():
    """Show index page to confirm that server is running."""
    return render_template('index.html')


@app.route((config.endpoint), methods=['POST'])
def inbound_parse():
    """Process POST from Inbound Parse and print received data."""
    parse = Parse(config, request)
    print(parse.key_values())
    return 'OK'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', config.port))
    if port != config.port:
        config.debug = False
    app.run(host='0.0.0.0', debug=(config.debug_mode), port=port)