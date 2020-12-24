# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_installed_product_ids.py
# Compiled at: 2019-11-14 13:57:46
import doctest
from ...parsers.installed_product_ids import InstalledProductIDs
from ...parsers import installed_product_ids
from ...tests import context_wrap
COMMAND_OUTPUT = '\n+-------------------------------------------+\nProduct Certificate\n+-------------------------------------------+\n\nCertificate:\n    Path: /etc/pki/product-default/69.pem\n    Version: 1.0\n    Serial: 12750047592154749739\n    Start Date: 2017-06-28 18:05:10+00:00\n    End Date: 2037-06-23 18:05:10+00:00\n\nSubject:\n    CN: Red Hat Product ID [4f9995e0-8dc4-4b4f-acfe-4ef1264b94f3]\n\nIssuer:\n    C: US\n    CN: Red Hat Entitlement Product Authority\n    O: Red Hat, Inc.\n    OU: Red Hat Network\n    ST: North Carolina\n    emailAddress: ca-support@redhat.com\n\nProduct:\n    ID: 69\n    Name: Red Hat Enterprise Linux Server\n    Version: 7.4\n    Arch: x86_64\n    Tags: rhel-7,rhel-7-server\n    Brand Type:\n    Brand Name:\n\n\n+-------------------------------------------+\n    Product Certificate\n+-------------------------------------------+\n\nCertificate:\n    Path: /etc/pki/product/69.pem\n    Version: 1.0\n    Serial: 12750047592154751271\n    Start Date: 2018-04-13 11:23:50+00:00\n    End Date: 2038-04-08 11:23:50+00:00\n\nSubject:\n    CN: Red Hat Product ID [f3c92a95-26be-4bdf-800f-02c044503896]\n\nIssuer:\n    C: US\n    CN: Red Hat Entitlement Product Authority\n    O: Red Hat, Inc.\n    OU: Red Hat Network\n    ST: North Carolina\n    emailAddress: ca-support@redhat.com\n\nProduct:\n    ID: 69\n    Name: Red Hat Enterprise Linux Server\n    Version: 7.6\n    Arch: x86_64\n    Tags: rhel-7,rhel-7-server\n    Brand Type:\n    Brand Name:\n'
NONE_FOUND = "\nfind: '/etc/pki/product-default/': No such file or directory\nfind: '/etc/pki/product/': No such file or directory\n"
BAD_FILE = "\nUnable to read certificate file '/etc/pki/product/some_file.pem': Error loading certificate\n"

def test_installed_product_ids():
    results = InstalledProductIDs(context_wrap(COMMAND_OUTPUT))
    assert results is not None
    assert results.ids == set(['69', '69'])
    results = InstalledProductIDs(context_wrap(NONE_FOUND))
    assert results is not None
    assert results.ids == set([])
    results = InstalledProductIDs(context_wrap(BAD_FILE))
    assert results is not None
    assert results.ids == set([])
    return


def test_installed_product_ids_docs():
    env = {'products': InstalledProductIDs(context_wrap(COMMAND_OUTPUT))}
    failed, total = doctest.testmod(installed_product_ids, globs=env)
    assert failed == 0