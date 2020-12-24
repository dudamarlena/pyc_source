# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/ripl/md2py.py
# Compiled at: 2017-03-01 09:16:28
# Size of source mod 2**32: 2622 bytes
"""
This one is going to read markdown.

For now, I am trying to read a talk outline and turn it into something
that will create a slideshow.

"""
import os

class Mark2Py:

    def __init__(self):
        pass

    def interpret(self, infile):
        """ Process a file of rest and return list of dicts """
        data = []
        for record in self.generate_records(infile):
            data.append(record)

        return data

    def hash_count(self, line):
        """ Count hashes at start of line

        Sad but true..
        """
        count = 0
        for c in line:
            if c != '#':
                break
            count += 1

        return count

    def generate_lines(self, infile):
        """ Split file into lines

        return dict with line=input, depth=n
        """
        pound = '#'
        for line in infile:
            heading = 0
            if line.startswith(pound):
                heading = self.hash_count(line)
            yield dict(line=line, heading=heading)

    def generate_records(self, infile):
        """ Process a file of rest and yield dictionaries """
        state = 0
        record = {}
        for item in self.generate_lines(infile):
            line = item['line']
            heading = item['heading']
            if heading:
                record['heading'] = True
                record['caption'] = line[1:].strip()
                state = 'caption'
                continue
            if not line[0].isspace():
                if state == 'caption':
                    yield record
                    record = {}
                    state = 0
            if state == 'caption':
                record['caption'] += '\n' + line[:-1]
            else:
                fields = line.split(',')
                if not fields:
                    pass
                else:
                    image = fields[0].strip()
                    if not image:
                        pass
                    else:
                        record['image'] = image
                        try:
                            time = float(fields[1])
                        except:
                            time = 0

                        record['time'] = time
                        try:
                            caption = fields[2].strip()
                        except:
                            caption = None

                if caption:
                    record['caption'] = caption
                if record:
                    yield record
                    record = {}


x = Mark2Py()
interpret = x.interpret