# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/LinguaFace/events/handlers.py
# Compiled at: 2010-11-30 09:59:25
from urllib import quote, unquote
from OFS import Moniker
from zlib import compress, decompress
from marshal import loads, dumps
from OFS.CopySupport import CopyContainer
from Products.CMFPlone.interfaces.Translatable import ITranslatable
from Products.CMFPlone.utils import base_hasattr
manage_pasteObjects = CopyContainer.manage_pasteObjects

def _cb_encode(d):
    return quote(compress(dumps(d), 9))


def _cb_decode(s):
    return loads(decompress(unquote(s)))


def objectCopiedEvent(object, event=None):
    """ Is used to pass the original object to objectClonedEvent.
    """
    ob = object.object
    ob.original = object.original


def objectClonedEvent(object, event=None):
    """ This event is notified during the manage_pasteObjects and is used in
    in order to copy all the translations of an object at once.
    """
    ob = object.object
    orig_ob = ob.original
    del ob.original
    if base_hasattr(ob, '_first_object_to_paste'):
        orig_ob._first_object_to_paste._copy[orig_ob] = ob
        del orig_ob._first_object_to_paste
        del ob._first_object_to_paste
    elif base_hasattr(ob, 'getOtherTranslations'):
        ob._copy = {}
        ob._copy[orig_ob] = ob
        oblist = orig_ob.getOtherTranslations()
        for object in oblist:
            object._first_object_to_paste = ob

        new_oblist = []
        for object in oblist:
            m = Moniker.Moniker(object)
            new_oblist.append(m.dump())

        oblist = new_oblist
        cb_copy_data = _cb_encode((0, oblist))
        manage_pasteObjects(ob.aq_parent, cb_copy_data)
        copy = ob._copy
        del ob._copy
        for translation in copy:
            if not translation.isCanonical():
                copy[translation].addTranslationReference(copy[translation.getCanonical()])


def objectMovedEvent(object, event=None):
    """ This event is notified during the manage_pasteObjects and is used in
    in order to cut/paste all the translations of an object at once.
    """
    ob = object.object
    oldParent = object.oldParent
    oldName = object.oldName
    newParent = object.newParent
    newName = object.newName
    dont_move = False
    if base_hasattr(newParent, '_v__dont_move_translations__'):
        dont_move = True
    if oldParent == None and oldName == None:
        return
    if newName == None and newParent == None:
        return
    if oldParent == newParent:
        return
    if base_hasattr(ob, '_v__translation_to_remove__'):
        del ob._v__translation_to_remove__
        return
    if base_hasattr(ob, 'getOtherTranslations') and not dont_move:
        oblist = ob.getOtherTranslations()
        for object in oblist:
            object._v__translation_to_remove__ = False

        new_oblist = []
        for object in oblist:
            m = Moniker.Moniker(object)
            new_oblist.append(m.dump())

        oblist = new_oblist
        cb_copy_data = _cb_encode((1, oblist))
        manage_pasteObjects(newParent, cb_copy_data)
    return


def objectWillBeRemovedEvent(object, event=None):
    """This handler is called before deleting object"""
    if not ITranslatable.isImplementedBy(object):
        return
    if not object.isCanonical():
        return
    object._v_translations = object.getTranslations()


def objectRemovedEvent(object, event=None):
    """This handler is called after object has been deleted"""
    if not ITranslatable.isImplementedBy(object):
        return
    translations = getattr(object, '_v_translations', {})
    if not translations:
        return
    for (lang, value) in translations.items():
        translation = value[0]
        if translation is object:
            continue
        translation.reindexObject(idxs=['getCanonicalPath'])

    delattr(object, '_v_translations')