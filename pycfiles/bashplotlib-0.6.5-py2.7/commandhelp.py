# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bashplotlib/utils/commandhelp.py
# Compiled at: 2016-02-06 16:56:13
"""
Usage messages for bashplotlib system commands
"""
hist = {'usage': 'hist is a command for making histograms. it accepts a series of values in one of the following formats:\n        1) txt file w/ 1 column of numbers\n        2) standard in piped from another command line cat or curl\n\n    for some examples of how to use hist, you can type the command:\n        hist --demo\n    or visit https://github.com/glamp/bashplotlib/blob/master/examples/sample.sh\n    '}
scatter = {'usage': 'scatterplot is a command for making xy plots. it accepts a series of x values and a series of y values in the\n    following formats:\n        1) a txt file or standard in value w/ 2 comma seperated columns of x,y values\n        2) 2 txt files. 1 w/ designated x values and another with designated y values.\n\n    scatter -x <xcoords> -y <ycoords>\n    cat <file_with_x_and_y_coords> | scatter\n    '}