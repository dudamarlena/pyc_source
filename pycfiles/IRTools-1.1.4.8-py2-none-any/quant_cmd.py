# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zzeng/Documents/GitHub/IRTools/IRTools/quant_cmd.py
# Compiled at: 2017-05-01 23:26:31
"""Description

Setup script for IRTools -- a powerful toolset for intron retention detection

Copyright (c) 2015 Zhouhao Zeng <zzhlbj23@gwmail.gwu.edu>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file COPYING included with
the distribution).

@status:  beta
@version: $Revision$
@author:  Zhouhao Zeng
@contact: zzhlbj23@gwmail.gwu.edu
"""
import sys, logging

def run(args):
    if args.quanttype == 'IRI':
        from IRTools.quant_IRI import IRI_quant
        IRI_quanter = IRI_quant(args)
        IRI_quanter.quant()
        IRI_quanter.output_IRI_intron_level()
        IRI_quanter.output_IRI_gene_level()
        IRI_quanter.output_IRI_genome_wide()
        if args.ERCC:
            from quant_ERCC_spike_in import run_quant_ERCC_spike_in
            run_quant_ERCC_spike_in(args)
    elif args.quanttype == 'IRC':
        from IRTools.quant_IRC_class import IRC_quant
        IRC_quanter = IRC_quant(args)
        IRC_quanter.quant()
        IRC_quanter.output_IRC_junction_level()
        IRC_quanter.output_IRC_intron_level()
        IRC_quanter.output_IRC_gene_level()
        IRC_quanter.output_IRC_genome_wide()