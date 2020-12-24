# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/tests/test_smartimagehandler.py
# Compiled at: 2008-12-23 17:55:57
"""
$Id: test_smartimagehandler.py 35335 2008-05-27 16:02:13Z anatoly $
"""
import unittest
from PIL import Image
from zope.app.testing import ztapi, setup, placelesssetup
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.component.hooks import setSite
from ks.smartimage.smartimagecache.interfaces import ISmartImageProp
from ks.smartimage.smartimagecache.smartimagecache import Scale, SmartImageCache
from ks.smartimage.smartimageadapter.interfaces import ISmartImageAdapter
from ks.smartimage.smartimageadapter.smartimageadapter import SmartImageAdapter
from ks.smartimage.smartimagehandler.smartimagehandler import addToSmartImageCashe, deleteFromSmartImageCashe, imageModify, imageDelete
from ks.smartimage.smartimage import SmartImage
from ks.smartimage.interfaces import ISmartImage
from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.folder.folder import Folder
from persistent.interfaces import IPersistent
from ZODB.interfaces import IConnection
from zope.app.keyreference.persistent import KeyReferenceToPersistent, connectionOfPersistent
from zope.app.keyreference.interfaces import IKeyReference
from zope.app.container.interfaces import IObjectAddedEvent, IObjectModifiedEvent
from zope.app.container.contained import ObjectAddedEvent, ObjectRemovedEvent
from zope.app.intid import addIntIdSubscriber, removeIntIdSubscriber
from zope.app.intid.interfaces import IIntIdAddedEvent, IIntIdRemovedEvent, IntIdRemovedEvent
zptlogo = b'GIF89a\x10\x00\x10\x00\xd5\x00\x00\xff\xff\xff\xff\xff\xfe\xfc\xfd\xfd\xfa\xfb\xfc\xf7\xf9\xfa\xf5\xf8\xf9\xf3\xf6\xf8\xf2\xf5\xf7\xf0\xf4\xf6\xeb\xf1\xf3\xe5\xed\xef\xde\xe8\xeb\xdc\xe6\xea\xd9\xe4\xe8\xd7\xe2\xe6\xd2\xdf\xe3\xd0\xdd\xe3\xcd\xdc\xe1\xcb\xda\xdf\xc9\xd9\xdf\xc8\xd8\xdd\xc6\xd7\xdc\xc4\xd6\xdc\xc3\xd4\xda\xc2\xd3\xd9\xc1\xd3\xd9\xc0\xd2\xd9\xbd\xd1\xd8\xbd\xd0\xd7\xbc\xcf\xd7\xbb\xcf\xd6\xbb\xce\xd5\xb9\xcd\xd4\xb6\xcc\xd4\xb6\xcb\xd3\xb5\xcb\xd2\xb4\xca\xd1\xb2\xc8\xd0\xb1\xc7\xd0\xb0\xc7\xcf\xaf\xc6\xce\xae\xc4\xce\xad\xc4\xcd\xab\xc3\xcc\xa9\xc2\xcb\xa8\xc1\xca\xa6\xc0\xc9\xa4\xbe\xc8\xa2\xbd\xc7\xa0\xbb\xc5\x9e\xba\xc4\x9b\xbf\xcc\x98\xb6\xc1\x8d\xae\xbaFgs\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x06z@\x80pH,\x12k\xc8$\xd2f\x04\xd4\x84\x01\x01\xe1\xf0d\x16\x9f\x80A\x01\x91\xc0ZmL\xb0\xcd\x00V\xd4\xc4a\x87z\xed\xb0-\x1a\xb3\xb8\x95\xbdf8\x1e\x11\xca,MoC$\x15\x18{\x006}m\x13\x16\x1a\x1f\x83\x85}6\x17\x1b $\x83\x00\x86\x19\x1d!%)\x8c\x866#\'+.\x8ca`\x1c`(,/1\x94B5\x19\x1e"&*-024\xacNq\xba\xbb\xb8h\xbeb\x00A\x00;'

class ConnectionStub(object):
    __module__ = __name__
    next = 1

    def db(self):
        return self

    database_name = 'ConnectionStub'

    def add(self, ob):
        ob._p_jar = self
        ob._p_oid = self.next
        self.next += 1


class ReferenceSetupMixin(object):
    __module__ = __name__

    def createSmartImage(self):
        u""" Метод для генерации экземпляря класа SmartImage (GIF-изображения)
        """
        smart_image = SmartImage()
        smart_image.contentType = 'image/gif'
        smart_image._setData(zptlogo)
        return smart_image

    def setUp(self):
        self.root = setup.placefulSetUp(site=True)
        ztapi.provideAdapter(IPersistent, IConnection, connectionOfPersistent)
        ztapi.provideAdapter(IPersistent, IKeyReference, KeyReferenceToPersistent)
        ztapi.provideAdapter(ISmartImage, ISmartImageAdapter, SmartImageAdapter)
        self.root._p_jar = ConnectionStub()
        self.root['folder1'] = self.folder1 = Folder()
        self.sm = setup.createSiteManager(self.folder1)
        setSite(self.folder1)
        sic = SmartImageCache()
        sic.format = 'GIF'
        sic.scales = (Scale(),)
        self.root['folder1']['sic'] = sic
        self.intids_utility = setup.addUtility(self.sm, '', IIntIds, IntIds())
        self.sic_utility = setup.addUtility(self.sm, '', ISmartImageProp, self.root['folder1']['sic'])
        self.root['folder1']['simg'] = self.createSmartImage()

    def tearDown(self):
        setup.placefulTearDown()


class testUsingImageCache(ReferenceSetupMixin, unittest.TestCase):
    __module__ = __name__

    def test_imageModify(self):
        smart_image = self.root['folder1']['simg']
        test_folder = self.root['folder1']
        events = []
        ztapi.subscribe([IIntIdAddedEvent], None, events.append)
        addIntIdSubscriber(smart_image, ObjectAddedEvent(test_folder))
        self.assertEquals(len(events), 1)
        self.assertEquals(events[0].original_event.object, test_folder)
        self.assertEquals(events[0].object, smart_image)
        self.assertEquals(len(self.sic_utility), 0)
        ztapi.subscribe([IObjectModifiedEvent], None, events.append)
        imageModify(smart_image, ObjectAddedEvent(test_folder))
        self.assertEquals(len(events), 2)
        self.assertEquals(events[1].object, self.sic_utility)
        self.assertEquals(len(self.sic_utility), 1)
        return

    def test_imageDelete(self):
        smart_image = self.root['folder1']['simg']
        test_folder = self.root['folder1']
        self.assertEquals(len(self.sic_utility), 0)
        id = self.intids_utility.register(smart_image)
        for cs in self.sic_utility.scales:
            simg = SmartImageAdapter(smart_image)
            simg.savetoCache(cs.name)

        self.assertEquals(len(self.sic_utility), 1)
        ztapi.subscribe([IIntIdRemovedEvent], None, imageDelete)
        removeIntIdSubscriber(smart_image, ObjectRemovedEvent(test_folder))
        self.assertRaises(KeyError, self.intids_utility.getObject, id)
        self.assertEquals(len(self.sic_utility), 0)
        return

    def test_addToSmartImageCashe(self):
        smart_image = self.root['folder1']['simg']
        test_folder = self.root['folder1']
        self.assertEquals(len(self.sic_utility), 0)
        self.assertEquals(self.sic_utility.elementsamount, 0)
        self.assertEquals(self.sic_utility.elementssize, 0.0)
        self.assertEquals(self.sic_utility.meansize, 0.0)
        addIntIdSubscriber(smart_image, ObjectAddedEvent(test_folder))
        imageModify(smart_image, ObjectAddedEvent(test_folder))
        self.assertEquals(len(self.sic_utility), 1)
        ztapi.subscribe([IObjectAddedEvent], None, addToSmartImageCashe)
        addToSmartImageCashe(smart_image, ObjectAddedEvent(smart_image, newParent=self.sic_utility))
        self.assertEquals(self.sic_utility.elementsamount, 1)
        self.assertEquals(self.sic_utility.elementssize, 0.34)
        self.assertEquals(self.sic_utility.meansize, 0.34)
        return

    def test_deleteFromSmartImageCashe(self):
        self.assertEquals(len(self.sic_utility), 0)
        self.test_addToSmartImageCashe()
        self.assertEquals(len(self.sic_utility), 1)
        self.assertEquals(self.sic_utility.elementsamount, 1)
        self.assertEquals(self.sic_utility.elementssize, 0.34)
        self.assertEquals(self.sic_utility.meansize, 0.34)
        smart_image = self.root['folder1']['simg']
        test_folder = self.root['folder1']
        id = self.intids_utility.getId(smart_image)
        deleteFromSmartImageCashe(smart_image, ObjectRemovedEvent(smart_image, oldParent=self.sic_utility))
        self.assertEquals(self.sic_utility.elementsamount, 0)
        self.assertEquals(self.sic_utility.elementssize, 0.0)
        self.assertEquals(self.sic_utility.meansize, 0.0)
        ztapi.subscribe([IIntIdRemovedEvent], None, imageDelete)
        removeIntIdSubscriber(smart_image, ObjectRemovedEvent(test_folder))
        self.assertEquals(len(self.sic_utility), 0)
        self.assertRaises(KeyError, self.intids_utility.getObject, id)
        return


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(testUsingImageCache),))


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())