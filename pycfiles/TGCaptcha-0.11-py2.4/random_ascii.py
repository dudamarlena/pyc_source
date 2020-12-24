# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/tgcaptcha/plugins/text/random_ascii.py
# Compiled at: 2007-05-31 01:59:00
import random
from turbogears import config
plugin_name = 'tgcaptcha.plugin.random_ascii.'
valid_chars = config.get(plugin_name + 'valid_chars', 'BCDEFGHJKLMNPQRTUVWXYacdefhijkmnprstuvwxyz378')
num_chars = int(config.get(plugin_name + 'num_chars', 5))

def generate_text():
    """Generate a random string to display as the captcha text."""
    s = []
    for i in range(num_chars):
        s.append(random.choice(valid_chars))

    return ('').join(s)