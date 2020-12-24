# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/qPCR2quantitation.py
# Compiled at: 2014-12-19 21:47:15
import os, matplotlib as mpl, matplotlib.pyplot as plt

def qPCR2quantitation(inputfile, output_formats):
    outputbasename = os.path.splitext(os.path.basename(inputfile))[0]
    ip = open(inputfile, 'r')
    for line in ip:
        if line.startswith('Step'):
            fields = line.split(',')
            if fields[0] != 'Step' or fields[1] != 'Cycle' or fields[2] != 'Dye' or fields[3] != 'Temp.':
                raise ValueError, 'Expected line like: "Step,Cycle,Dye,Temp.,..."'
            curve_labels = fields[4:-1]
            break

    for line in ip:
        if line.strip() == 'Analysis Options':
            break

    for line in ip:
        if line.startswith('Step') and 'Quantitation' in line:
            line_id = line.split()[1].strip(':')
            break

    ip.close()
    cycles = []
    curves = [ [] for curve in curve_labels ]
    ip = open(inputfile, 'r')
    for line in ip:
        if line.startswith('Step'):
            break

    for line in ip:
        if line.strip() == '':
            break
        if line.split(',')[0] == line_id:
            cycles.append(int(line.split(',')[1]))
            data = map(float, line.split(',')[4:-1])
            for i, value in enumerate(data):
                curves[i].append(value)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for label, curve in zip(curve_labels, curves):
        ax.plot(cycles, curve, label=label)

    ax.legend(loc=2)
    ax.set_xlabel('Cycles')
    ax.set_ylabel('Fluorescence (a.u.)')
    for format in output_formats:
        fig.savefig(outputbasename + '.quantitation.' + format)


if __name__ == '__main__':
    import sys, optparse
    output_formats = set()

    def append_format(option, opt_str, value, parser):
        output_formats.add(opt_str.strip('-'))


    option_parser = optparse.OptionParser()
    option_parser.add_option('--png', action='callback', callback=append_format)
    option_parser.add_option('--pdf', action='callback', callback=append_format)
    option_parser.add_option('--eps', action='callback', callback=append_format)
    options, args = option_parser.parse_args()
    if len(args) != 1:
        raise ValueError, 'Must give a single file as input.'
    output_formats = list(output_formats)
    if output_formats == []:
        output_formats.append('pdf')
        output_formats.append('png')
    inputfile = args[0]
    qPCR2quantitation(inputfile, output_formats)