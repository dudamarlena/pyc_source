# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/forecaster/common/conf.py
# Compiled at: 2012-02-16 09:53:47
"""
Created on 14. 12. 2011.

@author: kermit
"""
write_to_file = True
combine_plots = True
start_date = 1965
end_date = 2007
__countries = '\nalb\ndza\narg\narm\naze\nbgd\nblr\nben\nbmu\nbih\nbra\nbgr\nbfa\nbdi\ncmr\ncpv\ncaf\ntcd\nchl\nchn\ncol\ncod\ncog\ncri\nciv\nhrv\ncze\ndji\ndom\necu\negy\nslv\ngnq\neri\nest\nfin\ngeo\ngha\ngin\ngnb\nguy\nhti\nhun\nind\nisr\njam\njpn\njor\nken\nkor\nkwt\nkgz\nlva\nlbn\nlbr\nltu\nmkd\nmdg\nmys\nmli\nmrt\nmex\nmar\nmoz\nnpl\nnic\nner\nnga\nnor\npan\npry\nper\nphl\npol\nrou\nrus\nstp\nsen\nsle\nsvk\nsvn\nesp\nlka\nswz\nswe\ntza\ntha\ntgo\ntun\ntur\nuga\nukr\ngbr\nusa\nury\nyem\nzmb\nzwe\n'
__indicators = '\nSL.AGR.EMPL.ZS-agr_emp\nTX.VAL.AGRI.ZS.UN-agr_exp\n'
__process_indicators = '\nFR.INR.RINR\nSL.UEM.TOTL.ZS\n'
__state_indicators = '\nSP.POP.65UP.TO.ZS\n'
sample_selection_file = 'odabir_uzoraka-imf-odabrane.xls'
look_back_years = 3
testing_percentage = 0.0
wb_pause = 0
sparse = False
listify = lambda txt: [ el for el in txt.split('\n') if el != '' ]
listify_no_tails = lambda txt: [ el.split('-')[0] for el in txt.split('\n') if el != '' ]
countries = listify(__countries)
indicators_with_translations = listify(__indicators)
indicators = listify_no_tails(__indicators)
process_indicators = set(listify(__process_indicators))
state_indicators = listify(__state_indicators)