# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/aconf.py
# Compiled at: 2019-06-26 11:45:46
"""
    Autoconf'ed variables for PDB2PQR

    This is an module for storing all autoconf'ed variables.

    ----------------------------
   
    PDB2PQR -- An automated pipeline for the setup, execution, and analysis of
    Poisson-Boltzmann electrostatics calculations

    Copyright (c) 2002-2011, Jens Erik Nielsen, University College Dublin; 
    Nathan A. Baker, Battelle Memorial Institute, Developed at the Pacific 
    Northwest National Laboratory, operated by Battelle Memorial Institute, 
    Pacific Northwest Division for the U.S. Department Energy.; 
    Paul Czodrowski & Gerhard Klebe, University of Marburg.

        All rights reserved.

        Redistribution and use in source and binary forms, with or without modification, 
        are permitted provided that the following conditions are met:

                * Redistributions of source code must retain the above copyright notice, 
                  this list of conditions and the following disclaimer.
                * Redistributions in binary form must reproduce the above copyright notice, 
                  this list of conditions and the following disclaimer in the documentation 
                  and/or other materials provided with the distribution.
        * Neither the names of University College Dublin, Battelle Memorial Institute,
          Pacific Northwest National Laboratory, US Department of Energy, or University
          of Marburg nor the names of its contributors may be used to endorse or promote
          products derived from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
        ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
        IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
        INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
        BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
        DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
        LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
        OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
        OF THE POSSIBILITY OF SUCH DAMAGE.

    ----------------------------
"""
__date__ = '8 July 2008'
__author__ = 'Yong Huang'
PDB2PQR_VERSION = 'master'
MAXATOMS = 10000
SRCPATH = '/mnt/c/Users/pedro/Documents/pypka/pdb2pqr_pypka/'
WEBSITE = 'http://DESKTOP-NGTO9J9/pdb2pqr/'
STYLESHEET = WEBSITE + 'pdb2pqr.css'
PDB2PQR_OPAL_URL = ''
HAVE_PDB2PQR_OPAL = PDB2PQR_OPAL_URL != ''
APBS_LOCATION = ''
HAVE_APBS = APBS_LOCATION != ''
APBS_OPAL_URL = ''
INSTALLDIR = '/home/pedror/pdb2pqr/'
TMPDIR = 'tmp/'