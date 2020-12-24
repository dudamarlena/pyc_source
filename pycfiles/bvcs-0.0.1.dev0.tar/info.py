# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/anaconda2/lib/python2.7/site-packages/bvcopula/info.py
# Compiled at: 2018-11-01 00:24:18
__doc__ = "\nBVCOPULA\n========\n\nThis module mainly contains routines of probability distribution\nfunctions, density functions, random sample generating functions,\nH-functions and Inverse H-functions for six (and it will become more\nthan ten in the coming version, includes BB1, BB6, BB7, BB8 etc\nfamilies) bivariate copulas families. These ten bivariate copula has\nbeen deeply looked into by acamedic fields also own some popularity in\nindustry fields. The names of these ten copula families are listed\nbelow each with an integer label.\n\n        0 ~ Independent\n        1 ~ Normal \n        2 ~ Student t \n        3 ~ Clayton\n        4 ~ Gumbel\n        5 ~ Frank\n        6 ~ Joe\n        7 ~ BB1 (coming soon)\n        8 ~ BB6 (coming soon)\n        9 ~ BB7 (coming soon)\n       10 ~ BB8 (coming soon)\n\n\n\nThis package implementing these common seen bivariate copula here\nmainly serves as a toolbox for the package 'pyvine', in which these\nbivariate copula play a role of building block to construct regular\nvine copulas. We don't think our work for this package is recreate tie\nbecause we focus on the precision, range of parameters and\nperformances of those routines related to these copula. All these\nadvantages is attributed to optimized algorithm and approximation when\noverflow occurs, which are implemented in fortran and wrapped via\nf2py.\n"
__all__ = [
 'bv_cop_mle',
 'bv_cop_cdf',
 'bv_cop_pdf',
 'bv_cop_loglik',
 'bv_cop_sim',
 'bv_cop_hfunc',
 'bv_cop_inv_hfunc',
 'bv_cop_model_selection']