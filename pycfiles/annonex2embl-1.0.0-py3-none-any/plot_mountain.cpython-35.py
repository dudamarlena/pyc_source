# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/plot_mountain.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 1852 bytes
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot
matplotlib.pyplot.style.use('ggplot')

def plot_mountain_plot(input_file, output_name):
    poss = []
    values = []
    check = 0
    pre_check = 0
    f_h = open(input_file, 'r')
    while 1:
        line = f_h.readline()
        line = line.rstrip()
        if not line:
            matplotlib.pyplot.figure(1)
            matplotlib.pyplot.subplot(212)
            matplotlib.pyplot.xlabel('Nucleotide position')
            matplotlib.pyplot.ylabel('Entropy')
            matplotlib.pyplot.plot(values, color='black')
            matplotlib.pyplot.savefig(output_name, format='pdf')
            break
        else:
            if line == '&':
                line = f_h.readline()
                line = line.rstrip()
                check += 1
            else:
                poss.append(float(line[0:4].replace(' ', '')))
                values.append(float(line[5:].replace(' ', '')))
        if check != pre_check:
            pre_check = check
            if check == 1:
                matplotlib.pyplot.figure(1)
                matplotlib.pyplot.subplot(211)
                ylabel = 'Number of enclosing nucleotides\nor\nMin free energy structure'
                matplotlib.pyplot.ylabel(ylabel, fontsize=10, multialignment='left')
                matplotlib.pyplot.plot(values, label='pair probabilities')
                values = []
                poss = []
            elif check == 2:
                matplotlib.pyplot.plot(values, label='mfe structure')
                matplotlib.pyplot.legend(bbox_to_anchor=(0.0, 1.02, 1.0, 0.102), loc=3, ncol=2, mode='expand', borderaxespad=0.0)
                values = []
                poss = []

    f_h.close()
    matplotlib.pyplot.cla()
    matplotlib.pyplot.clf()