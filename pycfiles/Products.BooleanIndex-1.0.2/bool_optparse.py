# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/bool_optparse.py
# Compiled at: 2012-02-27 07:41:53
__doc__ = '\nA subclass of ``optparse.OptionParser`` that allows boolean long\noptions (like ``--verbose``) to also take arguments (like\n``--verbose=true``).  Arguments *must* use ``=``.\n'
import optparse
try:
    _ = optparse._
except AttributeError:
    from gettext import gettext as _

class BoolOptionParser(optparse.OptionParser):

    def _process_long_opt(self, rargs, values):
        arg = rargs.pop(0)
        if '=' in arg:
            (opt, next_arg) = arg.split('=', 1)
            rargs.insert(0, next_arg)
            had_explicit_value = True
        else:
            opt = arg
            had_explicit_value = False
        opt = self._match_long_opt(opt)
        option = self._long_opt[opt]
        if option.takes_value():
            nargs = option.nargs
            if len(rargs) < nargs:
                if nargs == 1:
                    self.error(_('%s option requires an argument') % opt)
                else:
                    self.error(_('%s option requires %d arguments') % (
                     opt, nargs))
            elif nargs == 1:
                value = rargs.pop(0)
            else:
                value = tuple(rargs[0:nargs])
                del rargs[0:nargs]
        elif had_explicit_value:
            value = rargs[0].lower().strip()
            del rargs[0:1]
            if value in ('true', 'yes', 'on', '1', 'y', 't'):
                value = None
            else:
                if value in ('false', 'no', 'off', '0', 'n', 'f'):
                    return
                self.error(_('%s option takes a boolean value only (true/false)') % opt)
        else:
            value = None
        option.process(opt, value, values, self)
        return