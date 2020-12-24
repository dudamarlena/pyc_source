# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chist.py
# Compiled at: 2018-09-19 06:10:00
# Size of source mod 2**32: 1076 bytes
import numpy as np, pandas as pd, matplotlib.pyplot as plt, click

@click.command()
@click.argument('filename')
@click.argument('column')
def hist(filename, column):
    df = pd.read_csv(filename)
    plt.hist(df[column])
    ax = plt.gca()
    ax.set(title=filename, xlabel=(column.title()), ylabel='Frequency')
    plt.show()


@click.command()
@click.argument('filename')
@click.argument('column')
@click.argument('column2')
def hist2(filename, column, column2):
    df = pd.read_csv(filename)
    H, x, y = np.histogram2d((df[column]), (df[column2]), bins=80)
    plt.imshow((H.T), extent=[x[0], x[(-1)], y[0], y[(-1)]], cmap='gray_r', origin='lower', aspect='auto')
    ax = plt.gca()
    ax.set(title=filename, xlabel=(column.title()), ylabel=(column2.title()))
    plt.show()


@click.command()
@click.argument('filename')
def show(filename):
    df = pd.read_csv(filename)
    summary = pd.DataFrame([df.dtypes, df.count(), df.min(), df.max()], index=['dtype', 'count', 'min', 'max']).T
    summary.index.name = 'column'
    print(summary)