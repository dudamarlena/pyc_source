# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danw/prj/exosite/pyonep/examples/provisioning.py
# Compiled at: 2015-09-12 16:15:07
# Size of source mod 2**32: 5787 bytes
import sys, random, logging
try:
    import httplib
except:
    from http import client as httplib

import pyonep
from pyonep.provision import Provision
from pyonep.onep import OnepV1
from pyonep.exceptions import ProvisionException
logging.basicConfig(stream=sys.stderr)
logging.getLogger('pyonep.onep').setLevel(logging.ERROR)
logging.getLogger('pyonep.provision').setLevel(logging.ERROR)

def provision_example(vendorname, vendortoken, clonerid, portalcik, portalrid):
    print('pyonep version ' + pyonep.__version__)
    r = random.randint(1, 10000000)
    model = 'MyTestModel' + str(r)
    sn1 = '001' + str(r)
    sn2 = '002' + str(r)
    sn3 = '003' + str(r)
    op = OnepV1()
    provision = Provision('m2.exosite.com', https=True, port=443, manage_by_cik=False, verbose=False, httptimeout=20, raise_api_exceptions=True, manage_by_sharecode=True)
    option = '["' + vendorname + '", "' + model + '"]'
    meta = {'meta': option}
    print('op.share', portalcik, clonerid, meta)
    isok, sharecode = op.share(portalcik, clonerid, meta)
    if not isok:
        print('failed to create share code')
        return False
    try:
        print('model_create() ', vendortoken, model, sharecode)
        provision.model_create(vendortoken, model, sharecode, aliases=False)
        print('model_list()')
        print(provision.model_list(vendortoken).body)
        print(provision.model_info(vendortoken, model).body)
        print('serialnumber_add()')
        provision.serialnumber_add(vendortoken, model, sn1)
        print('serialnumber_add_batch()')
        provision.serialnumber_add_batch(vendortoken, model, [sn2, sn3])
        print(provision.serialnumber_list(vendortoken, model, limit=10).body)
        print('serialnumber_remove_batch()')
        provision.serialnumber_remove_batch(vendortoken, model, [sn2, sn3])
        print(provision.serialnumber_list(vendortoken, model).body)
        print('serialnumber_enable()')
        provision.serialnumber_enable(vendortoken, model, sn1, portalrid)
        print('AFTER ENABLE:', provision.serialnumber_info(vendortoken, model, sn1).body)
        print('serialnumber_disable()')
        provision.serialnumber_disable(vendortoken, model, sn1)
        print('AFTER DISABLE:', provision.serialnumber_info(vendortoken, model, sn1).body)
        print('serialnumber_reenable()')
        provision.serialnumber_reenable(vendortoken, model, sn1)
        print('AFTER REENABLE:', provision.serialnumber_info(vendortoken, model, sn1).body)
        print('serialnumber_activate()')
        sn_cik = provision.serialnumber_activate(model, sn1, vendorname).body
        print('AFTER ACTIVATE:', provision.serialnumber_info(vendortoken, model, sn1).body)

        def test_content(content_id, content_data, content_type, content_meta):
            print('content_create()')
            provision.content_create(vendortoken, model, content_id, content_meta)
            print(provision.content_list(vendortoken, model))
            print('content_upload()')
            print(provision.content_upload(vendortoken, model, content_id, content_data, content_type))
            print(provision.content_list(vendortoken, model))
            print(provision.content_info(vendortoken, model, content_id))
            print('content_download()')
            print(provision.content_download(sn_cik, vendorname, model, content_id))
            print('content_remove()')
            provision.content_remove(vendortoken, model, content_id)

        test_content('a.txt', 'This is content data', 'text/plain', 'This is text')
        print('model_remove()')
        provision.model_remove(vendortoken, model)
    except ProvisionException:
        ex = sys.exc_info()[1]
        print('API Error: {0} {1}'.format(ex.response.status(), ex.response.reason()))
        return False
    except httplib.HTTPException:
        ex = sys.exc_info()[1]
        print('HTTPException: {0}'.format(ex))
        return False

    return True


if __name__ == '__main__':
    provision_example(vendorname='<VENDOR NAME HERE>', vendortoken='<VENDOR TOKEN HERE>', clonerid='<CLONE DEVICE RID HERE>', portalcik='<PORTAL CIK HERE>', portalrid='<PORTAL RID HERE>')