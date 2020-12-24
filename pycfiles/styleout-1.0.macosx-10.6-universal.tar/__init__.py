# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.6/site-packages/styleout/__init__.py
# Compiled at: 2010-09-13 13:18:29
import os, warnings, yaml
try:
    import cssmin
except:
    cssmin = None

try:
    import cssprefixer
except:
    cssprefixer = None

try:
    import clevercss
except:
    clevercss = None

wstr = '%s is not installed - cannot %s the CSS'
sk_wstr = '%s is not installed - skipping %s'
gext = lambda a: a.split('.')[(-1)]
cli_compilers = {'less': 'lessc %s %s', 
   'sass': 'sass %s:%s', 
   'scss': 'sass %s:%s'}

class Config(object):

    def __init__(self, text):
        self.cnf = yaml.load(text)

    def process(self):
        for sheet in self.cnf:
            result = ''
            sht = self.cnf[sheet]
            for fl in sht['files']:
                ext = gext(fl)
                src = open(fl, 'r').read()
                if ext == 'css':
                    result += src
                elif ext == 'clevercss':
                    if clevercss != None:
                        result += clevercss.convert(src)
                    else:
                        warnings.warn(sk_wstr % ('CleverCSS', fl))
                else:
                    for c in cli_compilers:
                        if ext == c:
                            tmpf = '.tempfile'
                            os.system(cli_compilers[c] % (fl, tmpf))
                            result += open(tmpf, 'r').read()
                            os.remove(tmpf)

            if sht['prefix']:
                if cssprefixer != None:
                    result = cssprefixer.process(result)
                else:
                    warnings.warn(wstr % ('CSSPrefixer', 'prefix'))
            if sht['minify']:
                if cssmin != None:
                    result = cssmin.cssmin(result)
                else:
                    warnings.warn(wstr % ('cssmin', 'minify'))
            open(sheet, 'w').write(result)
            print 'Compiled ' + sheet

        return True