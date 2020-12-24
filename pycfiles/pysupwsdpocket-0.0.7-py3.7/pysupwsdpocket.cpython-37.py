# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysupwsdpocket/pysupwsdpocket.py
# Compiled at: 2020-04-22 17:53:30
# Size of source mod 2**32: 724 bytes
import subprocess, json, os
from os import path

class PySupWSDPocket(object):

    def __init__(self, lang, model):
        self.lang = lang
        self.model = model
        self.HOME = os.environ['HOME']

    def wsd(self, raw_text):
        HERE = path.abspath(path.dirname(__file__))
        JAR_FILE = HERE + '/supwsd-pocket.jar'
        WORKSPACE = self.HOME + '/pysupwsdpocket_models'
        args = [
         raw_text, self.lang, self.model, WORKSPACE]
        try:
            doc = subprocess.check_output(['java', '-jar', JAR_FILE, *args], shell=False)
            doc = doc.decode('utf-8')
            return doc
        except Exception as err:
            try:
                return err
            finally:
                err = None
                del err