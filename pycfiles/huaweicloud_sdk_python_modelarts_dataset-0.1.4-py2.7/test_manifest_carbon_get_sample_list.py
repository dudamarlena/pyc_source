# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/modelarts/test/test_manifest_carbon_get_sample_list.py
# Compiled at: 2019-06-28 04:42:42
import os, sys
from modelarts import manifest
from modelarts.field_name import CARBONDATA
from obs import ObsClient

def test_single_default(path, obsClient):
    if obsClient is None:
        sources = manifest.getSources(path, CARBONDATA)
    else:
        sources = manifest.getSources(path, CARBONDATA, obsClient)
    assert 3 == len(sources)
    for source in sources:
        print source

    print 'Success: test_single_default'
    return


def main(argv):
    if len(argv) < 2:
        path1 = os.path.abspath('../../../') + '/resources/binary1557487619292.manifest'
        test_single_default(path1, None)
        print 'test local Success'
    else:
        path1 = 's3a://manifest/carbon/manifestcarbon/obsbinary1557717977531.manifest'
        ak = argv[1]
        sk = argv[2]
        endpoint = argv[3]
        obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint)
        test_single_default(path1, obsClient)
        print 'test OBS Success'
    return


if __name__ == '__main__':
    main(sys.argv)
    print 'Success'