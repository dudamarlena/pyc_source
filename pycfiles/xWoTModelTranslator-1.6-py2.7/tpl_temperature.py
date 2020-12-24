# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/xwot1/REST-Server-Skeleton/templates/tpl_temperature.py
# Compiled at: 2015-10-27 01:23:40
from twisted.web.template import Element, renderer, XMLFile, XMLString
from twisted.python.filepath import FilePath

class ExampleElement(Element):
    loader = XMLFile(FilePath('templates/tpl_temperature.xml'))

    def __init__(self, temp, hum):
        self.temperature = temp
        self.hummidity = hum
        self.extraTemperatureContent = XMLString('<input id="temperature" type="range" min="-100" max="100" value="' + self.temperature + '" class="xwot1 sensor columns large-12" />')
        self.extraHumidityContent = XMLString('<input id="humidity" type="range" min="0" max="100" value="' + self.hummidity + '" class="xwot1 sensor columns large-12" />')

    @renderer
    def header(self, request, tag):
        return tag('Header.')

    @renderer
    def temp(self, request, tag):
        return self.temperature

    @renderer
    def temperatureInput(self, request, tag):
        return self.extraTemperatureContent.load()

    @renderer
    def humidity(self, request, tag):
        return self.hummidity

    @renderer
    def humidityInput(self, request, tag):
        return self.extraHumidityContent.load()