# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyslm/export.py
# Compiled at: 2020-04-18 09:59:31
# Size of source mod 2**32: 2959 bytes


class MTTExportFeature(Feature):

    def __init__(self, hatchFeature, name='MTTExporter'):
        Feature.__init__(self, name)
        self._layerThickness = 10
        self._filename = ''
        self._models = []
        self._hatchFeature = hatchFeature
        self._setAttributes([self._hatchFeature])
        self._value = []
        print('Constructed Export to Renishaw')

    @staticmethod
    def exportMTT(header, models, layers):
        import renishawExport as MTT
        MTT.exportMTT(header, models, layers)

    @staticmethod
    def version():
        return (1, 0)

    @property
    def filename(self):
        return self._filename

    def value(self, update=False):
        if not self.requiresRecompute():
            return
        if self.isDirty() or update:
            self.update()
        return self._value

    def update(self):
        import renishawExport as MTT
        layerChunk = self._hatchFeature.value()
        slmLayers = []
        for sliceLayer in layerChunk:
            layer = MTT.Layer()
            layer.layerId = sliceLayer.id
            layer.z = sliceLayer.z
            geoms = []
            for contour in sliceLayer.contours:
                layerGeom = MTT.LayerGeometry()
                layerGeom.type = 'contour'
                layerGeom.coords = contour.coords
                layerGeom.bid = 0
                layerGeom.mid = 0
                geoms.append(layerGeom)

            for hatches in sliceLayer.hatches:
                layerGeom = MTT.LayerGeometry()
                layerGeom.type = 'hatch'
                layerGeom.coords = hatches.coords
                layerGeom.bid = 0
                layerGeom.mid = 0
                geoms.append(layerGeom)

            for points in sliceLayer.points:
                layerGeom = MTT.LayerGeometry()
                layerGeom.type = 'point'
                layerGeom.coords = points.coords
                layerGeom.bid = 0
                layerGeom.mid = 0
                geoms.append(layerGeom)

            layer.geometry = geoms
            slmLayers.append(layer)

        self._value = slmLayers