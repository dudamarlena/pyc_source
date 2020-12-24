# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/rdtypes/ANY/CNAME.py
# Compiled at: 2013-08-26 10:52:44
import dns.rdtypes.nsbase

class CNAME(dns.rdtypes.nsbase.NSBase):
    """CNAME record

    Note: although CNAME is officially a singleton type, dnspython allows
    non-singleton CNAME rdatasets because such sets have been commonly
    used by BIND and other nameservers for load balancing."""
    pass