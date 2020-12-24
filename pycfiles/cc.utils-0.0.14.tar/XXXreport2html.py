# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cc/buildout_reports/XXXreport2html.py
# Compiled at: 2007-08-22 13:54:45
__doc__ = 'Beautify a XXX report.\n\nCreates a HTML file from a XXXReport file.\n\n$Id$\n'
import sys, time
if len(sys.argv) < 3:
    print 'Usage: beautifyXXX.py <input-filename> <output-filename>'
    sys.exit()
inputname = sys.argv[1]
outputname = sys.argv[2]
inputfile = open(inputname, 'r')
outputfile = open(outputname, 'w')
comments = []
current = [
 '', 0, []]
for x in inputfile.readlines():
    if x == '--\n':
        print '.',
        comments.append(current)
        current = ['', 0, []]
        currentfile = None
        continue
    if not current[0]:
        splitted = x.split(':')
        current[0] = splitted[0]
        current[1] = splitted[1]
        x = (':').join(splitted[2:])
    else:
        splitted = x.split('-')
        x = ('-').join(splitted[2:])
    current[2].append(x)

outputfile.write('<html><head><title>XXX/YYY/ZZZTODO-Comment report</title>\n</head>\n\n<body>\n<h1>Developer report: XXX/YYY/ZZZ/TODO comments</h1>\n<p>Generated on %(reporttime)s</p>\n<hr>\n<h3>Summary</h3>\n<p>\n There are currently %(commentcount)s XXX/YYY/ZZZ/TODO comments.\n</p>\n<hr/>\n<h3>Listing</h3>\n<ol>' % {'commentcount': len(comments), 'reporttime': time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime())})
for x in comments:
    outputfile.write('<li><b>File: %(filename)s:%(line)s</b><br/><pre>%(text)s</pre></li>' % {'filename': x[0], 'line': x[1], 'text': ('').join(x[2])})

outputfile.write('<ol></body></html>')
outputfile.flush()
outputfile.close()