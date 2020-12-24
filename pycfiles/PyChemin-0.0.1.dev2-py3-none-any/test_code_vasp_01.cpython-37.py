# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/PyChemia/tests/test_code_vasp_01.py
# Compiled at: 2019-05-21 16:26:52
# Size of source mod 2**32: 12302 bytes
import sys, math, pychemia
SURFACE_TYPE = {
 'PLANE', 'SPHERE', 'PARAMETRIC_SURFACE'}

def WritePMG(ren, fn, magnification=1):
    """
    Save the image as a PNG

    :param ren: The renderer.
    :param fn: The file name.
    :param magnification: The magnification, usually 1.
    """
    renLgeIm = vtk.vtkRenderLargeImage()
    imgWriter = vtk.vtkPNGWriter()
    renLgeIm.SetInput(ren)
    renLgeIm.SetMagnification(magnification)
    imgWriter.SetInputConnection(renLgeIm.GetOutputPort())
    imgWriter.SetFileName(fn)
    imgWriter.Write()


def MakeBands(dR, numberOfBands, nearestInteger):
    """
    Divide a range into bands

    :param dR: [min, max] the range that is to be covered by the bands.
    :param numberOfBands: the number of bands, a positive integer.
    :param nearestInteger: if True then [floor(min), ceil(max)] is used.
    :return: A List consisting of [min, midpoint, max] for each band.
    """
    bands = list()
    if dR[1] < dR[0] or numberOfBands <= 0:
        return bands
    x = list(dR)
    if nearestInteger:
        x[0] = math.floor(x[0])
        x[1] = math.ceil(x[1])
    dx = (x[1] - x[0]) / float(numberOfBands)
    b = [x[0], x[0] + dx / 2.0, x[0] + dx]
    i = 0
    while i < numberOfBands:
        bands.append(b)
        b = [b[0] + dx, b[1] + dx, b[2] + dx]
        i += 1

    return bands


def MakeIntegralBands(dR):
    """
    Divide a range into integral bands
    :param: dR - [min, max] the range that is to be covered by the bands.
    :return: A List consisting of [min, midpoint, max] for each band.
    """
    bands = list()
    if dR[1] < dR[0]:
        return bands
    x = list(dR)
    x[0] = math.floor(x[0])
    x[1] = math.ceil(x[1])
    numberOfBands = int(abs(x[1]) + abs(x[0]))
    return MakeBands(x, numberOfBands, False)


def MakeElevations(src):
    """
    Generate elevations over the surface.
    :param: src - the vtkPolyData source.
    :return: - vtkPolyData source with elevations.
    """
    bounds = [
     0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    src.GetBounds(bounds)
    elevFilter = vtk.vtkElevationFilter()
    elevFilter.SetInputData(src)
    elevFilter.SetLowPoint(0, bounds[2], 0)
    elevFilter.SetHighPoint(0, bounds[3], 0)
    elevFilter.SetScalarRange(bounds[2], bounds[3])
    elevFilter.Update()
    return elevFilter.GetPolyDataOutput()


def MakePlane():
    """
    Make a plane as the source.
    :return: vtkPolyData with normal and scalar data.
    """
    source = vtk.vtkPlaneSource()
    source.SetOrigin(-10.0, -10.0, 0.0)
    source.SetPoint2(-10.0, 10.0, 0.0)
    source.SetPoint1(10.0, -10.0, 0.0)
    source.SetXResolution(20)
    source.SetYResolution(20)
    source.Update()
    return MakeElevations(source.GetOutput())


def MakeSphere():
    """
    Make a sphere as the source.
    :return: vtkPolyData with normal and scalar data.
    """
    source = vtk.vtkSphereSource()
    source.SetCenter(0.0, 0.0, 0.0)
    source.SetRadius(10.0)
    source.SetThetaResolution(32)
    source.SetPhiResolution(32)
    source.Update()
    return MakeElevations(source.GetOutput())


def MakeParametricSource():
    """
    Make a parametric surface as the source.
    :return: vtkPolyData with normal and scalar data.
    """
    fn = vtk.vtkParametricRandomHills()
    fn.AllowRandomGenerationOn()
    fn.SetRandomSeed(1)
    fn.SetNumberOfHills(30)
    if fn.GetClassName() == 'vtkParametricRandomHills':
        fn.ClockwiseOrderingOff()
    source = vtk.vtkParametricFunctionSource()
    source.SetParametricFunction(fn)
    source.SetUResolution(50)
    source.SetVResolution(50)
    source.SetScalarModeToZ()
    source.Update()
    source.GetOutput().GetPointData().GetNormals().SetName('Normals')
    source.GetOutput().GetPointData().GetScalars().SetName('Scalars')
    return source.GetOutput()


def MakeLUT():
    """
    Make a lookup table using vtkColorSeries.
    :return: An indexed lookup table.
    """
    colorSeries = vtk.vtkColorSeries()
    colorSeriesEnum = colorSeries.BREWER_QUALITATIVE_SET3
    colorSeries.SetColorScheme(colorSeriesEnum)
    lut = vtk.vtkLookupTable()
    colorSeries.BuildLookupTable(lut)
    lut.SetNanColor(1, 0, 0, 1)
    return lut


def ReverseLUT(lut):
    """
    Create a lookup table with the colors reversed.
    :param: lut - An indexed lookup table.
    :return: The reversed indexed lookup table.
    """
    lutr = vtk.vtkLookupTable()
    lutr.DeepCopy(lut)
    t = lut.GetNumberOfTableValues() - 1
    for i in reversed(range(t + 1)):
        rgba = [
         0, 0, 0]
        v = float(i)
        lut.GetColor(v, rgba)
        rgba.append(lut.GetOpacity(v))
        lutr.SetTableValue(t - i, rgba)

    t = lut.GetNumberOfAnnotatedValues() - 1
    for i in reversed(range(t + 1)):
        lutr.SetAnnotation(t - i, lut.GetAnnotation(i))

    return lutr


def Frequencies(bands, src):
    """
    Count the number of scalars in each band.
    :param: bands - the bands.
    :param: src - the vtkPolyData source.
    :return: The frequencies of the scalars in each band.
    """
    freq = dict()
    for i in range(len(bands)):
        freq[i] = 0

    tuples = src.GetPointData().GetScalars().GetNumberOfTuples()
    for i in range(tuples):
        x = src.GetPointData().GetScalars().GetTuple1(i)
        for j in range(len(bands)):
            if x <= bands[j][2]:
                freq[j] += 1
                break

    return freq


def MakeGlyphs(src, reverseNormals):
    """
    Glyph the normals on the surface.

    You may need to adjust the parameters for maskPts, arrow and glyph for a
    nice appearance.

    :param: src - the surface to glyph.
    :param: reverseNormals - if True the normals on the surface are reversed.
    :return: The glyph object.

    """
    reverse = vtk.vtkReverseSense()
    maskPts = vtk.vtkMaskPoints()
    maskPts.SetOnRatio(5)
    maskPts.RandomModeOn()
    if reverseNormals:
        reverse.SetInputData(src)
        reverse.ReverseCellsOn()
        reverse.ReverseNormalsOn()
        maskPts.SetInputConnection(reverse.GetOutputPort())
    else:
        maskPts.SetInputData(src)
    arrow = vtk.vtkArrowSource()
    arrow.SetTipResolution(16)
    arrow.SetTipLength(0.3)
    arrow.SetTipRadius(0.1)
    glyph = vtk.vtkGlyph3D()
    glyph.SetSourceConnection(arrow.GetOutputPort())
    glyph.SetInputConnection(maskPts.GetOutputPort())
    glyph.SetVectorModeToUseNormal()
    glyph.SetScaleFactor(1)
    glyph.SetColorModeToColorByVector()
    glyph.SetScaleModeToScaleByVector()
    glyph.OrientOn()
    glyph.Update()
    return glyph


def DisplaySurface(st):
    """
    Make and display the surface.
    :param: st - the surface to display.
    :return The vtkRenderWindowInteractor.
    """
    surface = st.upper()
    if surface not in SURFACE_TYPE:
        print(st, 'is not a surface.')
        iren = vtk.vtkRenderWindowInteractor()
        return iren
    else:
        src = vtk.vtkPolyData()
        if surface == 'PLANE':
            src = MakePlane()
        elif surface == 'SPHERE':
            src = MakeSphere()
        elif surface == 'PARAMETRIC_SURFACE':
            src = MakeParametricSource()
            src.GetPointData().GetScalars().SetName('Elevation')
    scalarRange = src.GetScalarRange()
    lut = MakeLUT()
    lut.SetTableRange(scalarRange)
    numberOfBands = lut.GetNumberOfTableValues()
    bands = MakeBands(scalarRange, numberOfBands, False)
    labels = []
    for i in range(len(bands)):
        labels.append('{:4.2f}'.format(bands[i][1]))

    values = vtk.vtkVariantArray()
    for i in range(len(labels)):
        values.InsertNextValue(vtk.vtkVariant(labels[i]))

    for i in range(values.GetNumberOfTuples()):
        lut.SetAnnotation(i, values.GetValue(i).ToString())

    lutr = ReverseLUT(lut)
    bcf = vtk.vtkBandedPolyDataContourFilter()
    bcf.SetInputData(src)
    for i in range(0, numberOfBands):
        bcf.SetValue(i, bands[i][2])

    bcf.SetScalarModeToIndex()
    bcf.GenerateContourEdgesOn()
    glyph = MakeGlyphs(src, False)
    srcMapper = vtk.vtkPolyDataMapper()
    srcMapper.SetInputConnection(bcf.GetOutputPort())
    srcMapper.SetScalarRange(scalarRange)
    srcMapper.SetLookupTable(lut)
    srcMapper.SetScalarModeToUseCellData()
    srcActor = vtk.vtkActor()
    srcActor.SetMapper(srcMapper)
    srcActor.RotateX(-45)
    srcActor.RotateZ(45)
    edgeMapper = vtk.vtkPolyDataMapper()
    edgeMapper.SetInputData(bcf.GetContourEdgesOutput())
    edgeMapper.SetResolveCoincidentTopologyToPolygonOffset()
    edgeActor = vtk.vtkActor()
    edgeActor.SetMapper(edgeMapper)
    edgeActor.GetProperty().SetColor(0, 0, 0)
    edgeActor.RotateX(-45)
    edgeActor.RotateZ(45)
    glyphMapper = vtk.vtkPolyDataMapper()
    glyphMapper.SetInputConnection(glyph.GetOutputPort())
    glyphMapper.SetScalarModeToUsePointFieldData()
    glyphMapper.SetColorModeToMapScalars()
    glyphMapper.ScalarVisibilityOn()
    glyphMapper.SelectColorArray('Elevation')
    glyphMapper.SetScalarRange(scalarRange)
    glyphActor = vtk.vtkActor()
    glyphActor.SetMapper(glyphMapper)
    glyphActor.RotateX(-45)
    glyphActor.RotateZ(45)
    scalarBar = vtk.vtkScalarBarActor()
    scalarBar.SetLookupTable(lutr)
    scalarBar.SetTitle('Elevation (m)')
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    iren = vtk.vtkRenderWindowInteractor()
    renWin.AddRenderer(ren)
    iren.SetRenderWindow(renWin)
    ren.AddViewProp(srcActor)
    ren.AddViewProp(edgeActor)
    ren.AddViewProp(glyphActor)
    ren.AddActor2D(scalarBar)
    ren.SetBackground(0.7, 0.8, 1.0)
    renWin.SetSize(800, 800)
    renWin.Render()
    ren.GetActiveCamera().Zoom(1.5)
    return iren


if __name__ == '__main__':
    if pychemia.HAS_VTK:
        import vtk
        iren = DisplaySurface('PARAMETRIC_SURFACE')
        iren.Render()
        iren.Start()
        WritePMG(iren.GetRenderWindow().GetRenderers().GetFirstRenderer(), 'ElevationBandsWithGlyphs.png')