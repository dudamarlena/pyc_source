# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Epigrass/rinterface.py
# Compiled at: 2019-08-30 11:41:07
# Size of source mod 2**32: 1025 bytes
"""
This module is a collection of fucntions to interface with "R":http://cran.r-project.org 

You need to have R and the following libraries installed for it to work:

*RMySQL

*DBI

*lattice
"""
from rpy import *

def qnplot(table):
    """
    This function query simulation results stored in a MySQL table
    and generates some plots.
    """
    s = 'library(DBI)\n    library(RMySQL)\n    library(lattice)\n    drv <- dbDriver("MySQL")\n    con <- dbConnect(drv, username=\'root\',password=\'mysql\', host=\'localhost\',dbname=\'epigrass\')\n    results<- dbReadTable(con,\'%s\')\n    names(results)\n    par(mfrow=c(2,2))\n    plot(results$I[results$geocode==230440005],type=\'l\',main=\'Fortaleza\')\n    plot(results$I[results$geocode==355030800],type=\'l\',main=\'São Paulo\')\n    plot(results$I[results$geocode==520880605],type=\'l\',main=\'goianira\')\n    plot(results$I[results$geocode==510760205],type=\'l\',main=\'Rondonopolis\')\n    x11()\n    xyplot(I~as.numeric(time),type="l",groups=results$geocode,data=results)\n    ' % table
    r(s)