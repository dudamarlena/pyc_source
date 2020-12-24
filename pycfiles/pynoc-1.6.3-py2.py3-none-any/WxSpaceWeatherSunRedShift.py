# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/PyNOAAGeoMagIndiceHandler/WxSpaceWeatherSunRedShift.py
# Compiled at: 2012-09-18 11:22:18
import re, os, sys, tempfile, WxSpaceWeatherDecor
from WxSpaceWeatherDecor import DecoratorWxWeather

class WxWeatherPyLabModuleLoaderFactory(object):
    UrlPath = {'url': 'http://www.spaceweather.com/', 
       'file-filter': [
                     '(?ui)images[0-9]{4}',
                     '(?ui)/+[0-9]{2}[a-z]{3}[0-9]{2}/+',
                     '(?ui)hmi4096']}
    BaseModuleLoad = {'list': [
              '__pylab__', '__urllib_pynav__', '__Image__', '__mathplotlib__', '__UrlPayload__',
              '__Filter_Image_Url__', '__Download_Image_Url__', '__Display_Image__'], 
       '__pylab__': {'modulelist': [
                                  'pylab'], 
                     'SystemExit': 'Pylab is essential to this example.'}, 
       '__urllib_pynav__': {'modulelist': [
                                         'urllib', 'urllib2',
                                         'pynav', {'pynav': 'Pynav', 'attr': 'PyNavUrlLoader'}], 
                            'SystemExit': 'This example need Network support with following module( urllib, urllib2, Pynav ).', 
                            'ModuleVar': {'Pynav': 'PyNavUrlLoader'}}, 
       '__Image__': {'modulelist': [
                                  'Image'], 
                     'SystemExit': 'PIL must be installed to run this example.'}, 
       '__mathplotlib__': {'modulelist': [{'matplotlib': 'cbook'}], 'SystemExit': 'matplotlib.cbook must be installed to run this example.'}, 
       '__UrlPayload__': {'modulelist': [], 'SystemExit': 'No PyNav Module-Attr available.'}, 
       '__Filter_Image_Url__': {'SystemExit': {'noattr': 'No Attr ImageRegList Provided within actual work-stream', 'main': 'No Images provided with actual work-stream.'}}, 
       '__Download_Image_Url__': {'modulelist': [], 'temp': 'c:\\docume~1\\admini~1\\locals~1\\temp\\', 
                                  'Section': {'name': 'ImagePattern', 
                                              'field': 'level', 
                                              'grade': 3, 
                                              'type': type(dict())}, 
                                  'SystemExit': {'noattr': 'No Attr ImagePattern Provided within actual work-stream', 
                                                 'main': 'No Downloading Images was provided with actual work-stream.'}}, 
       '__Display_Image__': {'modulelist': [], 'Section': {'name': 'ImageList', 
                                         'type': type(list())}, 
                             'SystemExit': {'noattr': 'No Attr ImageList Provided within actual work-stream', 
                                            'main': 'No Images was provided to display on view-screen.'}}}
    ImagePattern = {'level': {1: [], 2: [], 3: []}}
    ImageList = []
    DecorTransfertKeyStep = [{'modulelist': {'method-transfert': 'append'}}]
    IntDecorKeyId = 0
    CurrentFuncParsed = None
    CurrVarName = None
    CurrModule = None
    CurModuleName = None
    CurSectionName = None
    CurItemSecName = None

    def GetItemSecName(self):
        return self.CurItemSecName

    def SetItemSecName(self, value):
        self.CurItemSecName = value

    def GetSectionName(self):
        return self.CurSectionName

    def SetSectionName(self, value):
        self.CurSectionName = value

    def GetModuleName(self):
        return self.CurModuleName

    def SetModuleName(self, value):
        self.CurModuleName = value

    def GetVarName(self):
        return self.CurrVarName

    def SetVarName(self, value):
        self.CurrVarName = value

    def GetVarValue(self):
        return getattr(self, self.BaseModuleLoad[self.CurModuleName][self.CurSectionName][CurItemSecName])

    def SetVarValue(self, value):
        setattr(self, self.BaseModuleLoad[self.CurModuleName][self.CurSectionName][CurItemSecName], value)

    def GetRootValue(self):
        return GetVarValue()

    def SetRootVar(self, value):
        self.ModuleName, self.SectionName, self.CurItemSecName = value

    VarName = property(GetVarName, SetVarName)
    VarValue = property(GetVarValue, SetVarValue)
    ModuleName = property(GetModuleName, SetModuleName)
    SectionName = property(GetSectionName, SetSectionName)
    ItemSecName = property(GetSectionName, SetSectionName)
    RootValue = property(GetRootValue, SetRootVar)

    @DecoratorWxWeather.SetFuncName()
    def __pylab__(self):
        print 'end of function'

    @DecoratorWxWeather.SetFuncName()
    def __urllib_pynav__(self):
        print 'end of function'

    @DecoratorWxWeather.SetFuncName()
    def __Image__(self):
        print 'end of function'

    @DecoratorWxWeather.SetFuncName()
    def __mathplotlib__(self):
        print 'end of function'

    @DecoratorWxWeather.SetFuncName()
    def __UrlPayload__(self):
        if hasattr(self, 'PyNavUrlLoader'):
            self.ImageUrl = getattr(getattr(self, 'PyNavUrlLoader'), 'go')(self.UrlPath['url'])
            self.ImageRegList = getattr(getattr(self, 'PyNavUrlLoader'), 'get_all_links')()
            self.ImageRegListFilter = list()
        else:
            raise SystemExit(self.BaseModuleLoad[DecoratorWxWeather.FuncName]['SystemExit'])

    @DecoratorWxWeather.SetFuncName()
    def __Filter_Image_Url__(self):
        if hasattr(self, 'ImageRegList'):
            for ImageName in getattr(self, 'ImageRegList'):
                IntMatchCount = 0
                for RegExpRule in self.UrlPath['file-filter']:
                    CurrReg = re.compile(RegExpRule)
                    if CurrReg.search(ImageName):
                        IntMatchCount += 1

                if IntMatchCount not in self.ImagePattern['level'].keys():
                    self.ImagePattern['level'][IntMatchCount] = list()
                self.ImagePattern['level'][IntMatchCount].append(ImageName)

        else:
            raise SystemExit(self.BaseModuleLoad[DecoratorWxWeather.FuncName]['SystemExit']['noattr'])

    @DecoratorWxWeather.SetFuncName()
    def __Download_Image_Url__(self):
        StrTempPath = self.BaseModuleLoad[DecoratorWxWeather.FuncName]['temp']
        DefaultDicImage = self.BaseModuleLoad[DecoratorWxWeather.FuncName]['Section']['name']
        FieldImage = self.BaseModuleLoad[DecoratorWxWeather.FuncName]['Section']['field']
        IntDefaultGradeList = self.BaseModuleLoad[DecoratorWxWeather.FuncName]['Section']['grade']
        if hasattr(self, DefaultDicImage):
            for ImageSample in getattr(self, DefaultDicImage)[FieldImage][IntDefaultGradeList]:
                ListCleanFileName = ImageSample.split('?')
                print 'Processing File : %s , downloading to path : %s' % (ListCleanFileName[0], StrTempPath)
                self.ImageRegList = getattr(getattr(self, 'PyNavUrlLoader'), 'download')(ListCleanFileName[0], StrTempPath)
                self.ImageList.append(ListCleanFileName[0])

        else:
            raise SystemExit(self.BaseModuleLoad[DecoratorWxWeather.FuncName]['SystemExit']['noattr'])

    @DecoratorWxWeather.SetFuncName()
    def __Display_Image__(self):
        DefaultDicImage = self.BaseModuleLoad[DecoratorWxWeather.FuncName]['Section']['name']
        if hasattr(self, DefaultDicImage):
            for ItemImageFile in getattr(self, DefaultDicImage):
                datafile = cbook.get_sample_data(ItemImageFile)
                dataHandler = Image.open(datafile)
                dpi = rcParams['figure.dpi']
                figsize = (lena.size[0] / dpi, lena.size[1] / dpi)
                figure(figsize=figsize)
                ax = axes([0, 0, 1, 1], frameon=False)
                ax.set_axis_off()
                im = imshow(dataHandler, origin='lower')
                show()

        else:
            raise SystemExit(self.BaseModuleLoad[DecoratorWxWeather.FuncName]['SystemExit']['noattr'])

    def __StrutcTransfert__(self, ItemName, BasedModule, itemlist):
        return {ItemName: getattr(self, BasedModule)[self.CurrentFuncParsed][itemlist]}

    @DecoratorWxWeather.InitStructStart(IsProcessModuleList=True)
    def __init__(self):
        for ItemModule in self.BaseModuleLoad['list']:
            self.CurrentFuncParsed = ItemModule
            print 'Calling %s from Load.' % ItemModule
            DecoratorWxWeather.DecoratorExceptError = ImportError
            DecoratorWxWeather.DecoratorRaiseError = SystemExit
            DecoratorWxWeather.DecoratorRaiseMsg = self.BaseModuleLoad[ItemModule]['SystemExit']
            DecoratorWxWeather.ModuleList = self.BaseModuleLoad[self.CurrentFuncParsed]['modulelist']
            getattr(self, ItemModule)()


AWxModluleLoad = WxWeatherPyLabModuleLoaderFactory()