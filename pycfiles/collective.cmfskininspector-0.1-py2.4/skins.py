# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/collective/cmfskininspector/skins.py
# Compiled at: 2007-08-29 10:11:16
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class SkinInspector(BrowserView):
    __module__ = __name__
    template = ViewPageTemplateFile('skins.pt')

    def getSkinObjects(self, folder):
        object_ids = folder.objectIds()
        results = {}
        for oid in object_ids:
            obj = getattr(folder, oid)
            results[oid] = data = {}
            data['name'] = oid
            data['meta_type'] = obj.meta_type
            data['icon'] = obj.icon
            if obj.isPrincipiaFolderish:
                data['subobjects'] = self.getSkinObjects(obj)

        return results

    def __call__(self):
        skin_tool = getToolByName(self.context, 'portal_skins')
        self.dirs = self.getSkinObjects(skin_tool)
        self.skinpaths = skin_tool.getSkinPaths()
        results = []
        for (skin, paths) in self.skinpaths:
            path_info = []
            for path in paths.split(','):
                obj = self.dirs
                for name in path.split('/'):
                    obj = obj.get(name)
                    if obj is None:
                        break
                    obj = obj['subobjects']

                data = {'name': path}
                if obj is not None:
                    data['content'] = obj
                path_info.append(data)

            results.append({'name': skin, 'paths': tuple(path_info)})

        self.skininfo = tuple(results)
        return self.template()