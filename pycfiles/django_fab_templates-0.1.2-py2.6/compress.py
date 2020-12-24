# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/src/django_fab_templates/templates/vagrant_project/+project+/media_admin/js/compress.py
# Compiled at: 2011-04-13 14:50:43
import os, optparse, subprocess, sys
here = os.path.dirname(__file__)

def main():
    usage = 'usage: %prog [file1..fileN]'
    description = 'With no file paths given this script will automatically\ncompress all jQuery-based files of the admin app. Requires the Google Closure\nCompiler library and Java version 6 or later.'
    parser = optparse.OptionParser(usage, description=description)
    parser.add_option('-c', dest='compiler', default='~/bin/compiler.jar', help='path to Closure Compiler jar file')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    parser.add_option('-q', '--quiet', action='store_false', dest='verbose')
    (options, args) = parser.parse_args()
    compiler = os.path.expanduser(options.compiler)
    if not os.path.exists(compiler):
        sys.exit('Google Closure compiler jar file %s not found. Please use the -c option to specify the path.' % compiler)
    if not args:
        if options.verbose:
            sys.stdout.write('No filenames given; defaulting to admin scripts\n')
        args = [ os.path.join(here, f) for f in ['actions.js', 'collapse.js', 'inlines.js', 'prepopulate.js'] ]
    for arg in args:
        if not arg.endswith('.js'):
            arg = arg + '.js'
        to_compress = os.path.expanduser(arg)
        if os.path.exists(to_compress):
            to_compress_min = '%s.min.js' % ('').join(arg.rsplit('.js'))
            cmd = 'java -jar %s --js %s --js_output_file %s' % (compiler, to_compress, to_compress_min)
            if options.verbose:
                sys.stdout.write('Running: %s\n' % cmd)
            subprocess.call(cmd.split())
        else:
            sys.stdout.write('File %s not found. Sure it exists?\n' % to_compress)


if __name__ == '__main__':
    main()