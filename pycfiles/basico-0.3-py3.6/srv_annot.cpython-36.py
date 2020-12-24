# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/basico/services/srv_annot.py
# Compiled at: 2019-03-31 12:04:48
# Size of source mod 2**32: 5497 bytes
"""
# File: srv_annot.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Annotations service
"""
import os, json, uuid, glob
from os.path import sep as SEP
from basico.core.mod_env import FILE, LPATH
from basico.core.mod_srv import Service

class Annotation(Service):

    def initialize(self):
        """
        Setup Annotation Service
        """
        self.get_services()

    def get_services(self):
        self.srvutl = self.get_service('Utils')

    def gen_aid(self, sid):
        """
        Generate new annotation id
        """
        return '%s@%s' % (sid, str(uuid.uuid4()))

    def create(self, annotation):
        ANNOTATION_FILE_METADATA = LPATH['ANNOTATIONS'] + annotation['AID'] + '.json'
        ANNOTATION_FILE_CONTENT = LPATH['ANNOTATIONS'] + annotation['AID'] + '.adoc'
        annotation['Timestamp'] = self.srvutl.timestamp()
        with open(ANNOTATION_FILE_CONTENT, 'w') as (fc):
            fc.write(annotation['Content'])
        del annotation['Content']
        with open(ANNOTATION_FILE_METADATA, 'w') as (fa):
            json.dump(annotation, fa)
        title = self.get_title(annotation['AID'])
        self.log.info("Annotation '%s' (%s) created" % (title, annotation['AID']))

    def update(self, annotation):
        ANNOTATION_FILE_METADATA = LPATH['ANNOTATIONS'] + annotation['AID'] + '.json'
        ANNOTATION_FILE_CONTENT = LPATH['ANNOTATIONS'] + annotation['AID'] + '.adoc'
        annotation['Timestamp'] = self.srvutl.timestamp()
        with open(ANNOTATION_FILE_CONTENT, 'w') as (fc):
            fc.write(annotation['Content'])
        del annotation['Content']
        with open(ANNOTATION_FILE_METADATA, 'w') as (fa):
            json.dump(annotation, fa)
        title = self.get_title(annotation['AID'])
        self.log.info("Annotation '%s' (%s) updated" % (title, annotation['AID']))

    def delete(self, aid):
        sid = self.get_sid(aid)
        ANNOTATION_FILE_METADATA = LPATH['ANNOTATIONS'] + aid + '.json'
        ANNOTATION_FILE_CONTENT = LPATH['ANNOTATIONS'] + aid + '.adoc'
        title = self.get_title(aid)
        if os.path.exists(ANNOTATION_FILE_METADATA):
            os.unlink(ANNOTATION_FILE_METADATA)
        if os.path.exists(ANNOTATION_FILE_CONTENT):
            os.unlink(ANNOTATION_FILE_CONTENT)
        self.log.info("Annotation '%s' (%s) deleted" % (title, aid))

    def get_by_sid(self, sid):
        ANNOTATION_FILES = LPATH['ANNOTATIONS'] + '%s*.json' % sid
        annotations = glob.glob(ANNOTATION_FILES)
        annotations.sort(reverse=True)
        return annotations

    def get_all(self):
        return glob.glob(LPATH['ANNOTATIONS'] + '*.json')

    def get_total(self):
        return len(self.get_all())

    def get_sid(self, aid):
        if '@' in aid:
            return aid[:aid.find('@')]
        else:
            return aid

    def get_metadata_from_file(self, aid=None):
        if aid is not None:
            ANNOTATION_FILE_METADATA = LPATH['ANNOTATIONS'] + aid + '.json'
            with open(ANNOTATION_FILE_METADATA, 'r') as (fa):
                annotation = json.load(fa)
            return annotation
        else:
            return

    def is_valid(self, aid):
        ANNOTATION_FILE = LPATH['ANNOTATIONS'] + aid + '.json'
        valid = os.path.exists(ANNOTATION_FILE)
        if valid is False:
            self.log.debug("Annotation %s is not valid or it doesn't exist yet." % aid)
        return valid

    def get_title(self, aid):
        ANNOTATION_FILE = LPATH['ANNOTATIONS'] + aid + '.json'
        with open(ANNOTATION_FILE, 'r') as (fa):
            metadata = json.load(fa)
            return metadata['Title']

    def search_term(self, term):
        matches = set()
        annotations = self.get_all()
        for fname in annotations:
            with open(fname, 'r') as (fa):
                try:
                    annotation = json.load(fa)
                    text = annotation['Title']
                    if term.upper() in text.upper():
                        matches.add(fname)
                except Exception as error:
                    self.log.error('%s: %s', fname, error)

        return matches

    def finalize(self):
        pass