# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: scripts/dataset_class.py
# Compiled at: 2017-10-08 10:33:46
import file_manipulation as FM, talk_with_google

class Dataset:

    def __init__(self):
        self.setkey = 'NA'
        self.search = 'MULTIPLE'
        self.imgdirP = 'NA'
        self.genesP = 'NA'
        self.setname = 'NA'
        self.btnname = 'NA'
        self.citetxt = 'NA'
        self.citelink = 'NA'
        self.info = 'NA'

    def read_in_dataset_parameters(self, paramFilePath):
        """
        DESCRIPTION:
        NOTES: Owner of this is the dataset class
        OUTPUT:
        """
        paramDict = FM.create_dict_from_file(paramFilePath, skip=0)
        for key in paramDict:
            setattr(self, key, paramDict[key])

    def upload_image_files(self, bucket):
        """
        NAME: upload_image_files
        DESCRIPTION:
            - Uploads the data into the bucket. 
            - Name of directory will be the set key. 
        """
        talk_with_google.gsutil_cp_rsync_file_to_cloud_storage(self.imgdirP, bucket + '/' + self.setkey)