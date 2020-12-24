# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/musy/Projects/vtkplotter/vtkplotter/backends.py
# Compiled at: 2020-03-06 08:21:29
from __future__ import division, print_function
import vtk, numpy, os, vtkplotter.colors as colors
from vtkplotter.mesh import Mesh
from vtkplotter.volume import Volume
import vtkplotter.settings as settings, vtkplotter.addons as addons, vtkplotter.utils as utils
from vtk.util.numpy_support import vtk_to_numpy
__all__ = []

def getNotebookBackend(actors2show, zoom, viewup):
    vp = settings.plotter_instance
    if 'itk' in settings.notebookBackend:
        from itkwidgets import view
        if sum(vp.shape) != 2:
            colors.printc('Warning: multirendering is not supported in jupyter.', c=1)
        settings.notebook_plotter = view(actors=actors2show, cmap='jet', ui_collapsed=True, gradient_opacity=False)
    elif settings.notebookBackend == 'k3d':
        import k3d
        if vp.shape[0] != 1 or vp.shape[1] != 1:
            colors.printc('Warning: multirendering is not supported in jupyter.', c=1)
        actors2show2 = []
        for ia in actors2show:
            if isinstance(ia, vtk.vtkAssembly):
                acass = ia.unpack()
                actors2show2 += acass
            else:
                actors2show2.append(ia)

        vbb, sizes, min_bns, max_bns = addons.computeVisibleBounds()
        kgrid = (vbb[0], vbb[2], vbb[4], vbb[1], vbb[3], vbb[5])
        settings.notebook_plotter = k3d.plot(axes=[vp.xtitle, vp.ytitle, vp.ztitle], menu_visibility=True, height=int(vp.size[1] / 2))
        settings.notebook_plotter.grid = kgrid
        settings.notebook_plotter.lighting = 1.2
        settings.notebook_plotter.camera_auto_fit = False
        eps = 1 + numpy.random.random() * 0.0001
        if settings.plotter_instance and settings.plotter_instance.camera:
            k3dc = utils.vtkCameraToK3D(settings.plotter_instance.camera)
            k3dc[2] = k3dc[2] * eps
            settings.notebook_plotter.camera = k3dc
        else:
            vsx, vsy, vsz = vbb[0] - vbb[1], vbb[2] - vbb[3], vbb[4] - vbb[5]
            vss = numpy.linalg.norm([vsx, vsy, vsz])
            if zoom:
                vss /= zoom
            vfp = (
             (vbb[0] + vbb[1]) / 2, (vbb[2] + vbb[3]) / 2, (vbb[4] + vbb[5]) / 2)
            if viewup == 'z':
                vup = (0, 0, 1)
                vpos = (vfp[0] + vss / 1.9, vfp[1] + vss / 1.9, vfp[2] + vss * 0.01)
            else:
                if viewup == 'x':
                    vup = (1, 0, 0)
                    vpos = (vfp[0] + vss * 0.01, vfp[1] + vss / 1.5, vfp[2])
                else:
                    vup = (0, 1, 0)
                    vpos = (vfp[0] + vss * 0.01, vfp[1] + vss * 0.01, vfp[2] + vss / 1.5)
                settings.notebook_plotter.camera = [
                 vpos[0], vpos[1], vpos[2] * eps,
                 vfp[0], vfp[1], vfp[2],
                 vup[0], vup[1], vup[2]]
            if not vp.axes:
                settings.notebook_plotter.grid_visible = False
            for ia in actors2show2:
                kobj = None
                kcmap = None
                if isinstance(ia, Mesh) and ia.N():
                    iap = ia.GetProperty()
                    iapoly = ia.clone().clean().triangulate().computeNormals().polydata()
                    vtkscals = None
                    color_attribute = None
                    if ia.mapper().GetScalarVisibility():
                        vtkdata = iapoly.GetPointData()
                        vtkscals = vtkdata.GetScalars()
                        if vtkscals is None:
                            vtkdata = iapoly.GetCellData()
                            vtkscals = vtkdata.GetScalars()
                            if vtkscals is not None:
                                c2p = vtk.vtkCellDataToPointData()
                                c2p.SetInputData(iapoly)
                                c2p.Update()
                                iapoly = c2p.GetOutput()
                                vtkdata = iapoly.GetPointData()
                                vtkscals = vtkdata.GetScalars()
                        if vtkscals is not None:
                            if not vtkscals.GetName():
                                vtkscals.SetName('scalars')
                            scals_min, scals_max = ia.mapper().GetScalarRange()
                            color_attribute = (vtkscals.GetName(), scals_min, scals_max)
                            lut = ia.mapper().GetLookupTable()
                            lut.Build()
                            kcmap = []
                            nlut = lut.GetNumberOfTableValues()
                            for i in range(nlut):
                                r, g, b, a = lut.GetTableValue(i)
                                kcmap += [i / (nlut - 1), r, g, b]

                    if iapoly.GetNumberOfPolys() > 0:
                        name = None
                        if ia.filename:
                            name = os.path.basename(ia.filename)
                        kobj = k3d.vtk_poly_data(iapoly, name=name, color=colors.rgb2int(iap.GetColor()), color_attribute=color_attribute, color_map=kcmap, opacity=iap.GetOpacity(), wireframe=iap.GetRepresentation() == 1)
                        if iap.GetInterpolation() == 0:
                            kobj.flat_shading = True
                    else:
                        kcols = []
                        if color_attribute is not None:
                            scals = vtk_to_numpy(vtkscals)
                            kcols = k3d.helpers.map_colors(scals, kcmap, [
                             scals_min, scals_max]).astype(numpy.uint32)
                        sqsize = numpy.sqrt(numpy.dot(sizes, sizes))
                        if ia.NPoints() == ia.NCells():
                            kobj = k3d.points(ia.points().astype(numpy.float32), color=colors.rgb2int(iap.GetColor()), colors=kcols, opacity=iap.GetOpacity(), shader='3d', point_size=iap.GetPointSize() * sqsize / 400)
                        else:
                            kobj = k3d.line(ia.points().astype(numpy.float32), color=colors.rgb2int(iap.GetColor()), colors=kcols, opacity=iap.GetOpacity(), shader='thick', width=iap.GetLineWidth() * sqsize / 1000)
                    settings.notebook_plotter += kobj
                elif isinstance(ia, Volume):
                    kx, ky, kz = ia.dimensions()
                    arr = ia.getPointArray()
                    kimage = arr.reshape(-1, ky, kx)
                    colorTransferFunction = ia.GetProperty().GetRGBTransferFunction()
                    kcmap = []
                    for i in range(128):
                        r, g, b = colorTransferFunction.GetColor(i / 127)
                        kcmap += [i / 127, r, g, b]

                    kbounds = numpy.array(ia.imagedata().GetBounds()) + numpy.repeat(numpy.array(ia.imagedata().GetSpacing()) / 2.0, 2) * numpy.array([-1, 1] * 3)
                    kobj = k3d.volume(kimage.astype(numpy.float32), color_map=kcmap, alpha_coef=10, bounds=kbounds)
                    settings.notebook_plotter += kobj
                elif hasattr(ia, 'info') and 'formula' in ia.info.keys():
                    pos = (
                     ia.GetPosition()[0], ia.GetPosition()[1])
                    kobj = k3d.text2d(ia.info['formula'], position=pos)
                    settings.notebook_plotter += kobj

    elif settings.notebookBackend == 'panel' and hasattr(vp, 'window') and vp.window:
        import panel
        vp.renderer.ResetCamera()
        settings.notebook_plotter = panel.pane.VTK(vp.window, width=int(vp.size[0] / 1.5), height=int(vp.size[1] / 2))
    elif '2d' in settings.notebookBackend.lower() and hasattr(vp, 'window') and vp.window:
        import PIL.Image
        try:
            import IPython
        except ImportError:
            raise Exception('IPython not available.')
            return

        from vtkplotter.vtkio import screenshot
        settings.screeshotLargeImage = True
        nn = screenshot(returnNumpy=True, scale=settings.screeshotScale + 2)
        pil_img = PIL.Image.fromarray(nn)
        settings.notebook_plotter = IPython.display.display(pil_img)
    return settings.notebook_plotter