# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pyoverflow/pyoverflow.py
# Compiled at: 2016-07-03 07:58:22
import webbrowser
from google import search
import sys
search_result = []

def submit_err(error_msg, no_solution):
    print '\n'
    print 'Please wait ................ '
    print 'Pyoverflow is checking for the top solutions for your code problems'
    print ':)'
    print '\n'
    search_word = 'python ' + str(error_msg)
    for url in search(search_word, stop=2):
        search_result.append(url)

    for i in range(0, no_solution):
        print 'Opening\t' + str(i) + ' solution in browser'
        webbrowser.open_new_tab(search_result[i])