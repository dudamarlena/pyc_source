# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/textgrids/templates.py
# Compiled at: 2020-01-21 09:57:13
# Size of source mod 2**32: 1058 bytes
__doc__ = '\n\n  templates.py\n\n  2019-07-15    Done.\n  2019-08-02    Bug fix. Always TEXT_{LONG|SHORT}, never\n                {LONG|SHORT}_TEXT.\n  2019-08-04    Bug fix (line breaks, indentation in templates).\n\n'
TEXT_LONG = 0
TEXT_SHORT = 1
BINARY = 2
long_header = 'File type = "ooTextFile"\nObject class = "TextGrid"\n\nxmin = {}\nxmax = {}\ntiers? <exists>\nsize = {}\nitem []:'
short_header = 'File type = "ooTextFile"\nObject class = "TextGrid"\n\n{xmin}\n{xmax}\n<exists>\n{length}\n'
long_tier = '\n    item [{}]:\n        class = "{}"\n        name = "{}"\n        xmin = {}\n        xmax = {}\n        {}: size = {}'
short_tier = '"{tier_type}"\n"{name}"\n{xmin}\n{xmax}\n{length}\n'
long_point = '\n            points [{}]:\n                xpos = {}\n                text = "{}"'
short_point = '{xpos}\n"{text}"\n'
long_interval = '\n            intervals [{}]:\n                xmin = {}\n                xmax = {}\n                text = "{}"'
short_interval = '{xmin}\n{xmax}\n"{text}"\n'