# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sphinxcontrib/email.py
# Compiled at: 2011-01-29 12:48:02
from docutils import nodes
import re, string
rot_13_trans = string.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm')

def rot_13_encrypt(line):
    """Rotate 13 encryption.

    """
    line = line.translate(rot_13_trans)
    line = re.sub('(?=[\\"])', '\\\\', line)
    line = re.sub('\n', '\\n', line)
    line = re.sub('@', '\\\\100', line)
    line = re.sub('\\.', '\\\\056', line)
    line = re.sub('/', '\\\\057', line)
    return line


def js_obfuscated_text(text):
    """ROT 13 encryption with embedded in Javascript code to decrypt
    in the browser.

    """
    return '<script type="text/javascript">document.write(\n              "%s".replace(/[a-zA-Z]/g,\n              function(c){\n                return String.fromCharCode(\n                (c<="Z"?90:122)>=(c=c.charCodeAt(0)+13)?c:c-26);}));\n                </script>' % rot_13_encrypt(text)


def js_obfuscated_mailto(email, displayname=None):
    """ROT 13 encryption within an Anchor tag w/ a mailto: attribute

    """
    if not displayname:
        displayname = email
    return js_obfuscated_text('<a href="mailto:%s">%s</a>' % (
     email, displayname))


def email_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to obfuscate e-mail addresses.
    """
    text = text.decode('utf-8').encode('utf-8')
    if '<' in text and '>' in text:
        (name, email) = text.split('<')
        email = email.split('>')[0]
    elif '(' in text and ')' in text:
        (name, email) = text.split('(')
        email = email.split(')')[0]
    else:
        name = text
        email = name
    obfuscated = js_obfuscated_mailto(email, displayname=name)
    node = nodes.raw('', obfuscated, format='html')
    return ([node], [])


def setup(app):
    app.add_role('email', email_role)