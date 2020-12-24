# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: scripts/create_autocomplete_page.py
# Compiled at: 2017-10-08 10:33:46


def create_autocomplete_page():
    """

    FUNCTION: Create autocomplete page. 

    #INPUT:
    - ../data/manipulated_data/temporary_gene_key_data.txt - Stores all the information for each possible input and the associated figures for that output.

    #OUTPUT:
    - ../www/js/gene_name_auto.js  - a file that outputs all of the javascript for autocomplete file.
    """
    fileIN = open('tmp/search_lookup_file.txt')
    searchTerms = list()
    for i in fileIN:
        i = i.rstrip().split('\t')
        searchTerms.append(i[0])

    fileIN.close()
    searchTermUnique = list(set(searchTerms))
    fileOUT = open('web/js/gene_name_auto.js', 'w')
    fileOUT.write('var allTerms = [')
    outTerms = [ '{ value: "' + x + '"}' for x in searchTermUnique ]
    fileOUT.write((', ').join(outTerms) + ']\n')
    fileOUT.close()