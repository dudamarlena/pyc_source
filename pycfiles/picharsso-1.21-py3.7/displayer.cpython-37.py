# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/picharsso/displayer.py
# Compiled at: 2019-11-08 16:27:15
# Size of source mod 2**32: 609 bytes


class Displayer:
    __doc__ = 'A wrapper for displaying output\n    '

    def display(self):
        """Displays text art and saves it to a file if necessary
        """
        output = {'ansi':lambda x: '\n'.join([''.join(row) for row in x]), 
         'html':lambda x: '<div>{}</div>'.format('\n<br />'.join([''.join(row) for row in x]))}
        art = output.get(self.args.output_type)(self.text)
        if not self.args.quiet:
            print(art)
        if self.args.output_file:
            with open(self.args.output_file, 'w') as (f):
                f.write(art)