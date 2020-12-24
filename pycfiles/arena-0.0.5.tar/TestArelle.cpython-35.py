# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ubuntu/arelle/TestArelle.py
# Compiled at: 2018-07-25 04:57:42
# Size of source mod 2**32: 1620 bytes
import arelle, time
from arelle import ViewFileFactList, ModelXbrl, ModelManager, FileSource, Cntlr, ModelDocument
import json, os

def extractXbrl(path):
    modelManager = arelle.ModelManager.initialize(arelle.Cntlr.Cntlr())
    xbrl = arelle.ModelXbrl.load(modelManager, path)
    jsonobject = arelle.ViewFileFactList.viewFacts(xbrl, 'xbrlDocument.json')
    return jsonobject


def run_test(dir_with_samples):
    print('Running tests inside {}'.format(dir_with_samples))
    for file in os.listdir(dir_with_samples):
        if not file.endswith('.xhtml'):
            pass
        else:
            path = os.path.join(dir_with_samples, file)
            ModelDocument.AWESOME_MODS = False
            st = time.time()
            org = json.dumps(extractXbrl(path))
            end = time.time()
            ModelDocument.AWESOME_MODS = True
            st2 = time.time()
            quick = json.dumps(extractXbrl(path))
            end2 = time.time()
            print('[{}] XBLR load: {:.3f}s vs. {:.3f}s'.format(os.path.basename(path), end - st, end2 - st2))
            if org != quick:
                print('Org: {}'.format(org))
                print('Qck: {}\n'.format(quick))
            break


if __name__ == '__main__':
    ModelDocument.AWESOME_MODS = True
    st2 = time.time()
    quick = json.dumps(extractXbrl('samples/test01.xhtml'))
    end2 = time.time()
    print('XBLR load: {:.3f}s'.format(end2 - st2))