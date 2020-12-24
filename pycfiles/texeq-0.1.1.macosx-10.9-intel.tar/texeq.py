# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/texeq/texeq.py
# Compiled at: 2014-01-04 10:35:05
import sys, subprocess, base64, argparse, os, shutil
validformats = set(['pdf', 'svg', 'png'])
formula = '\\documentclass[crop=true,border=0pt]{standalone}\n\\usepackage{amsmath}\n\\usepackage{varwidth}\n\\begin{document}\n\\begin{varwidth}{\\linewidth}\n\\[ \\formula \\]\n\\end{varwidth}\n\\end{document}'

def clearcache(cd=None):
    """clears the cache directory specified or the default one"""
    cd = os.environ.get('TEXEQ', 'texeq.dir')
    if not os.path.isdir(cd):
        return True
    else:
        cdm = os.path.join(cd, '.texeq')
        if not os.path.isfile(cdm):
            return False
        shutil.rmtree(cd)
        return True


def getequation(expression, cd=None, invalidate=False, format='pdf', showerror=False):
    if format not in validformats:
        return (False, 'not a valid format:' + str(validformats))
    else:
        if cd is None:
            cd = os.environ.get('TEXEQ', 'texeq.dir')
        cdm = os.path.join(cd, '.texeq')
        if not os.path.isdir(cd):
            os.mkdir(cd)
        if not os.path.isfile(cdm):
            x = open(cdm, 'w')
            x.close()
        if not os.path.isfile(cdm):
            return (False, 'cannot create files in cache dir ' + cd)
        ce = base64.b64encode(expression)
        fce = os.path.join(cd, ce)
        ftex = fce + '.tex'
        fpdf = fce + '.pdf'
        fout = fce + '.' + format
        if invalidate or not os.path.isfile(ftex):
            if os.path.isfile(fpdf):
                os.unlink(fpdf)
            o = open(ftex, 'w')
            o.write('\\def\\formula{' + expression + '}\n' + formula)
            o.close()
        if invalidate or not os.path.isfile(fpdf):
            if os.path.isfile(fout):
                os.unlink(fout)
            if not showerror:
                x = subprocess.PIPE
            else:
                x = None
            subprocess.call(['pdflatex', '-interaction', 'nonstopmode', '-output-directory=' + cd, ftex], stdout=x, stderr=x)
            if not os.path.isfile(fpdf):
                return (False, 'cannot create file. Error in latex:' + ftex)
            for x in ['.aux', '.log']:
                fx = fce + x
                if os.path.isfile(fx):
                    os.unlink(fx)

        if fpdf != fout:
            if invalidate or not os.path.isfile(fout):
                if format == 'svg':
                    subprocess.call(['pdf2svg', fpdf, fout])
                else:
                    if format == 'png':
                        subprocess.call(['convert', '-density', '300', fpdf, '-quality', '90', fout])
                    if not os.path.isfile(fout):
                        return (False, 'cannot convert file ' + fpdf + ' to ' + fout + ' (svg output requires pdf2svg, png output requires ImageMagick convert)')
        return (
         True, fout)


def run():
    parser = argparse.ArgumentParser(description='Latex equation generator (with cache)')
    parser.add_argument('expression', nargs='?', help='latex expression')
    parser.add_argument('--format', default='pdf', help='output format: pdf or svg or png')
    parser.add_argument('--auto', action='store_true', help='auto filename only if input')
    parser.add_argument('--input', help='input filename')
    parser.add_argument('--output', help='output filename')
    parser.add_argument('--invalidate', action='store_true', default=False, help='invalidate cached')
    parser.add_argument('--cachedir', help='cache folder. Default is ')
    parser.add_argument('--clear', action='store_true', help='clear cache')
    parser.add_argument('--showerror', action='store_true', help='show latex error')
    args = parser.parse_args()
    cd = args.cachedir
    if args.clear:
        if not clearcache(cd):
            print 'cannot clear cache'
            sys.exit(-2)
        else:
            print 'cleaned'
            sys.exit(0)
    elif args.input is not None:
        args.expression = open(args.input, 'r').read()
    elif args.expression is None:
        print 'missing expression'
        sys.exit(-2)
    if args.output is None:
        if args.auto:
            if args.input is not None:
                args.output = os.path.splitext(args.input)[0] + '.' + args.format
            else:
                print 'asked for auto output but missing input'
                sys.exit(-2)
    ok, what = getequation(args.expression, cd=cd, invalidate=args.invalidate, showerror=args.showerror, format=args.format)
    if not ok:
        print what
        sys.exit(-1)
    else:
        ro = what
    if args.output is not None:
        shutil.copyfile(ro, args.output)
        ro = args.output
    else:
        print ro
    return


if __name__ == '__main__':
    run()