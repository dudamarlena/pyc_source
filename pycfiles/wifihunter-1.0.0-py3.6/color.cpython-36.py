# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/handlers/color.py
# Compiled at: 2020-01-19 07:49:44
# Size of source mod 2**32: 3873 bytes
import sys

class Color(object):
    __doc__ = ' Helper object for easily printing colored text to the terminal. '
    colors = {'W':'\x1b[0m', 
     'R':'\x1b[31m', 
     'G':'\x1b[32m', 
     'O':'\x1b[33m', 
     'B':'\x1b[34m', 
     'P':'\x1b[35m', 
     'C':'\x1b[36m', 
     'GR':'\x1b[37m', 
     'D':'\x1b[2m'}
    replacements = {'{+}':' {W}{D}[{W}{G}+{W}{D}]{W}', 
     '{!}':' {O}[{R}!{O}]{W}', 
     '{?}':' {W}[{C}?{W}]'}
    last_sameline_length = 0

    @staticmethod
    def p(text):
        """
        Prints text using colored format on same line.
        Example:
            Color.p('{R}This text is red. {W} This text is white')
        """
        sys.stdout.write(Color.s(text))
        sys.stdout.flush()
        if '\r' in text:
            text = text[text.rfind('\r') + 1:]
            Color.last_sameline_length = len(text)
        else:
            Color.last_sameline_length += len(text)

    @staticmethod
    def pl(text):
        """Prints text using colored format with trailing new line."""
        Color.p('%s\n' % text)
        Color.last_sameline_length = 0

    @staticmethod
    def pe(text):
        """Prints text using colored format with leading and trailing new line to STDERR."""
        sys.stderr.write(Color.s('%s\n' % text))
        Color.last_sameline_length = 0

    @staticmethod
    def s(text):
        """ Returns colored string """
        output = text
        for key, value in Color.replacements.items():
            output = output.replace(key, value)

        for key, value in Color.colors.items():
            output = output.replace('{%s}' % key, value)

        return output

    @staticmethod
    def clear_line():
        spaces = ' ' * Color.last_sameline_length
        sys.stdout.write('\r%s\r' % spaces)
        sys.stdout.flush()
        Color.last_sameline_length = 0

    @staticmethod
    def clear_entire_line():
        import os
        rows, columns = os.popen('stty size', 'r').read().split()
        Color.p('\r' + ' ' * int(columns) + '\r')

    @staticmethod
    def pattack(attack_type, target, attack_name, progress):
        """
        Prints a one-liner for an attack.
        Includes attack type (WEP/WPA), target ESSID & power, attack type, and progress.
        ESSID (Pwr) Attack_Type: Progress
        e.g.: Router2G (23db) WEP replay attack: 102 IVs
        """
        essid = '{C}%s{W}' % target.essid if target.essid_known else '{O}unknown{W}'
        Color.p('\r{+} {G}%s{W} ({C}%sdb{W}) {G}%s {C}%s{W}: %s ' % (
         essid, target.power, attack_type, attack_name, progress))

    @staticmethod
    def pexception(exception):
        """Prints an exception. Includes stack trace if necessary."""
        Color.pl('\n{!} {R}Error: {O}%s' % str(exception))
        if 'No targets found' in str(exception):
            return
        from ..config import Configuration
        if Configuration.verbose > 0 or Configuration.print_stack_traces:
            Color.pl('\n{!} {O}Full stack trace below')
            from traceback import format_exc
            Color.p('\n{!}    ')
            err = format_exc().strip()
            err = err.replace('\n', '\n{!} {C}   ')
            err = err.replace('  File', '{W}File')
            err = err.replace('  Exception: ', '{R}Exception: {O}')
            Color.pl(err)


if __name__ == '__main__':
    Color.pl('{R}Testing{G}One{C}Two{P}Three{W}Done')
    print(Color.s('{C}Testing{P}String{W}'))
    Color.pl('{+} Good line')
    Color.pl('{!} Danger')