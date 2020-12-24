# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/v_m_t/VolumeInfoeXist.py
# Compiled at: 2019-10-11 16:37:54
# Size of source mod 2**32: 1932 bytes
from typing import List, Any
from urllib import request
from v_m_t.VolumeInfoBase import VolumeInfoBase, VolInfo

class VolumeInfoeXist(VolumeInfoBase):
    __doc__ = '\n    this uses the exist db queries get the volume list of a work, including, for each volume:\n    - image list\n    - image group ID\n\n    The information should be fetched (in csv or json) from lds-pdi, query for W22084 for instance is:\n    http://www.tbrc.org/public?module=work&query=work-igs&arg=WorkRid\n    '

    def fetch(self, work_rid: str) -> []:
        """
        :param work_rid: Resource id
        :type work_rid: object
        """
        req = f"http://www.tbrc.org/public?module=work&query=work-igs&args={work_rid}"
        vol_info = []
        from lxml import etree
        try:
            with request.urlopen(req) as (response):
                info = response.read()
                info = info.decode('utf8').strip()
                igs = etree.fromstring(info).text.split(' ')
                vol_info = self.expand_groups(work_rid, igs)
        except etree.ParseError:
            pass

        return vol_info

    def expand_groups(self, work_rid: str, image_groups: []) -> object:
        """
        expands an image group into a list of its files
        :type image_groups: []
        :param work_rid: work resource Id
        :param image_groups: Image Groups to expand
        :return: VolInfo[] of all the images in all imagegroups in the input
        """
        vi = []
        for ig in image_groups:
            vol_infos = self.get_image_names_from_S3(work_rid, ig)
            vi.append(VolInfo(vol_infos, ig))

        return vi