# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/plane_widgets_observer.py
# Compiled at: 2012-04-19 05:23:36
from gtk import gdk
import gtk, vtk, time
from markers import Marker, RingActor
from events import EventHandler, UndoRegistry
import numpy as np
from marker_window_interactor import MarkerWindowInteractor
from shared import shared
from rois import RoiEdgeActor
INTERACT_CURSOR, MOVE_CURSOR, COLOR_CURSOR, SELECT_CURSOR, DELETE_CURSOR, LABEL_CURSOR, SCREENSHOT_CURSOR = (
 gtk.gdk.ARROW, gtk.gdk.HAND2, gtk.gdk.SPRAYCAN, gtk.gdk.TCROSS, gtk.gdk.X_CURSOR, gtk.gdk.PENCIL, gtk.gdk.ICON)

class PlaneWidgetObserver(MarkerWindowInteractor):
    """
    Showing a slice view snychronised with planes widget
    """
    axes_labels_color = (0.0, 0.82, 1.0)

    def __init__(self, planeWidget, owner, orientation, imageData=None):
        if shared.debug:
            print 'PlaneWidgetObserver.__init__(): orientation=', orientation
        MarkerWindowInteractor.__init__(self)
        self.interactButtons = (1, 2, 3)
        self.pw = planeWidget
        self.owner = owner
        self.orientation = orientation
        self.observer = vtk.vtkImagePlaneWidget()
        self.camera = self.renderer.GetActiveCamera()
        self.ringActors = {}
        self.defaultRingLine = 1
        self.textActors = {}
        self.hasData = 0
        self.set_image_data(imageData)
        self.lastTime = 0
        self.set_mouse1_to_move()

    def set_image_data(self, imageData):
        if imageData is None:
            return
        else:
            self.imageData = imageData
            if not self.hasData:
                if shared.debug:
                    print 'PlaneWidgetObserver(', self.orientation, ').. AddObserver(self.interaction_event)'
                foo = self.pw.AddObserver('InteractionEvent', self.interaction_event)
                if shared.debug:
                    print 'PlaneWidgetObserver.set_image_data(): AddObserver call returns ', foo
                self.connect('scroll_event', self.scroll_widget_slice)
                self.hasData = 1
            self.observer.GetCursorProperty().SetOpacity(0.0)
            self.observer.TextureInterpolateOn()
            self.observer.TextureInterpolateOn()
            self.observer.SetKeyPressActivationValue(self.pw.GetKeyPressActivationValue())
            self.observer.GetPlaneProperty().SetColor(0, 0, 0)
            self.observer.SetResliceInterpolate(self.pw.GetResliceInterpolate())
            self.observer.SetLookupTable(self.pw.GetLookupTable())
            self.observer.DisplayTextOn()
            self.observer.SetInput(imageData)
            self.observer.SetInteractor(self.interactor)
            self.observer.On()
            self.observer.InteractionOff()
            self.update_plane()
            self.sliceIncrement = 0.1
            spacing = self.imageData.GetSpacing()
            self._ratio = np.mean(np.abs(spacing))
            shared.ratio = self._ratio
            return

    def add_axes_labels(self):
        labels = shared.labels
        self.axes_labels = labels
        self.axes_labels_actors = []
        size = abs(self.imageData.GetSpacing()[0]) * 5
        for i, b in enumerate(self.imageData.GetBounds()):
            coords = list(self.imageData.GetCenter())
            coords[i / 2] = b * 1.12
            idx_label = 1 * i
            label = labels[idx_label]
            if shared.debug:
                print i, b, coords, label
            if self.orientation == 0:
                if label in ('R', 'L'):
                    continue
            if self.orientation == 1:
                if label in ('A', 'P'):
                    continue
            if self.orientation == 2:
                if label in ('S', 'I'):
                    continue
            text = vtk.vtkVectorText()
            text.SetText(label)
            textMapper = vtk.vtkPolyDataMapper()
            textMapper.SetInput(text.GetOutput())
            textActor = vtk.vtkFollower()
            textActor.SetMapper(textMapper)
            textActor.SetScale(size, size, size)
            x, y, z = coords
            textActor.SetPosition(x, y, z)
            textActor.GetProperty().SetColor(*self.axes_labels_color)
            textActor.SetCamera(self.camera)
            self.axes_labels_actors.append(textActor)
            self.renderer.AddActor(textActor)

        center = self.imageData.GetCenter()
        spacing = self.imageData.GetSpacing()
        bounds = np.array(self.imageData.GetBounds())
        if shared.debug:
            print '***center,spacing,bounds', center, spacing, bounds
        pos = [
         center[0], center[1], center[2]]
        camera_up = [0, 0, 0]
        if self.orientation == 0:
            pos[0] += max(bounds[1::2] - bounds[0::2]) * 2
            camera_up[2] = 1
        elif self.orientation == 1:
            pos[1] += max(bounds[1::2] - bounds[0::2]) * 2
            camera_up[2] = 1
        elif self.orientation == 2:
            pos[2] += max(bounds[1::2] - bounds[0::2]) * 2
            camera_up[0] = -1
        if shared.debug:
            print camera_up
        fpu = (
         center, pos, tuple(camera_up))
        if shared.debug:
            print '***fpu2:', fpu
        self.set_camera(fpu)
        self.scroll_depth(self.sliceIncrement)

    def mouse1_mode_change(self, event):
        try:
            self.moveEvent
        except AttributeError:
            pass
        else:
            self.observer.RemoveObserver(self.moveEvent)

        try:
            self.startEvent
        except AttributeError:
            pass
        else:
            self.observer.RemoveObserver(self.startEvent)

        try:
            self.endEvent
        except AttributeError:
            pass
        else:
            self.observer.RemoveObserver(self.endEvent)

    def set_mouse1_to_move(self):
        self.markerAtPoint = None
        self.pressed1 = 0

        def move(*args):
            if self.markerAtPoint is None:
                return
            else:
                xyz = self.get_cursor_position_world()
                EventHandler().notify('move marker', self.markerAtPoint, xyz)
                return

        def button_down(*args):
            self.markerAtPoint = self.get_marker_at_point()
            if self.markerAtPoint is not None:
                self.lastPos = self.markerAtPoint.get_center()
            return

        def button_up(*args):
            if self.markerAtPoint is None:
                return
            else:
                thisPos = self.markerAtPoint.get_center()

                def undo_move(marker):
                    marker.set_center(self.lastPos)
                    ra = self.get_actor_for_marker(marker)
                    ra.update()
                    self.Render()

                if thisPos != self.lastPos:
                    UndoRegistry().push_command(undo_move, self.markerAtPoint)
                self.markerAtPoint = None
                return

        self.pressHooks[1] = button_down
        self.releaseHooks[1] = button_up
        self.moveEvent = self.observer.AddObserver('InteractionEvent', move)
        cursor = gtk.gdk.Cursor(MOVE_CURSOR)
        if self.window is not None:
            self.window.set_cursor(cursor)
        return

    def set_select_mode(self):
        pass

    def set_interact_mode(self):
        self.interactButtons = (1, 2, 3)
        self.set_mouse1_to_move()

    def get_marker_at_point(self):
        xyz = self.get_cursor_position_world()
        for actor in self.get_ring_actors_as_list():
            if not actor.GetVisibility():
                continue
            marker = actor.get_marker()
            if marker is None:
                return
            if marker.contains(xyz):
                return marker

        return

    def get_plane_points(self):
        return (self.pw.GetOrigin(), self.pw.GetPoint1(), self.pw.GetPoint2())

    def set_plane_points(self, pnts):
        o, p1, p2 = pnts
        self.pw.SetOrigin(o)
        self.pw.SetPoint1(p1)
        self.pw.SetPoint2(p2)
        self.pw.UpdatePlacement()
        self.update_plane()

    def OnButtonDown(self, wid, event):
        if not self.hasData:
            return
        self.lastPnts = self.get_plane_points()
        if event.button == 1:
            self.observer.InteractionOn()
        ret = MarkerWindowInteractor.OnButtonDown(self, wid, event)
        return ret

    def OnButtonUp(self, wid, event):
        if not hasattr(self, 'lastPnts'):
            return
        if not self.hasData:
            return
        if event.button == 1:
            self.observer.InteractionOff()
        MarkerWindowInteractor.OnButtonUp(self, wid, event)
        pnts = self.get_plane_points()
        if pnts != self.lastPnts:
            UndoRegistry().push_command(self.set_plane_points, self.lastPnts)
        return True

    def scroll_depth(self, step):
        p1 = np.array(self.pw.GetPoint1())
        p2 = np.array(self.pw.GetPoint2())
        origin = self.pw.GetOrigin()
        normal = self.pw.GetNormal()
        newPlane = vtk.vtkPlane()
        newPlane.SetNormal(normal)
        newPlane.SetOrigin(origin)
        newPlane.Push(step)
        newOrigin = newPlane.GetOrigin()
        delta = np.array(newOrigin) - np.array(origin)
        p1 += delta
        p2 += delta
        self.pw.SetPoint1(p1)
        self.pw.SetPoint2(p2)
        self.pw.SetOrigin(newOrigin)
        self.pw.UpdatePlacement()
        self.update_plane()

    def scroll_axis1(self, step):
        axis1 = [
         0, 0, 0]
        self.pw.GetVector1(axis1)
        transform = vtk.vtkTransform()
        axis2 = [
         0, 0, 0]
        self.pw.GetVector2(axis2)
        transform = vtk.vtkTransform()
        transform.RotateWXYZ(step, (
         axis1[0] + 0.5 * axis2[0],
         axis1[1] + 0.5 * axis2[2],
         axis1[2] + 0.5 * axis2[2]))
        o, p1, p2 = self.get_plane_points()
        o = transform.TransformPoint(o)
        p1 = transform.TransformPoint(p1)
        p2 = transform.TransformPoint(p2)
        self.set_plane_points((o, p1, p2))
        self.update_plane()

    def scroll_axis2(self, step):
        axis1 = [
         0, 0, 0]
        self.pw.GetVector2(axis1)
        transform = vtk.vtkTransform()
        axis2 = [
         0, 0, 0]
        self.pw.GetVector1(axis2)
        transform = vtk.vtkTransform()
        transform.RotateWXYZ(step, (
         axis1[0] + 0.5 * axis2[0],
         axis1[1] + 0.5 * axis2[2],
         axis1[2] + 0.5 * axis2[2]))
        o, p1, p2 = self.get_plane_points()
        o = transform.TransformPoint(o)
        p1 = transform.TransformPoint(p1)
        p2 = transform.TransformPoint(p2)
        self.set_plane_points((o, p1, p2))
        self.update_plane()

    def scroll_widget_slice(self, widget, event):
        now = time.time()
        elapsed = now - self.lastTime
        if elapsed < 0.001:
            return
        if event.direction == gdk.SCROLL_UP:
            step = 1
        elif event.direction == gdk.SCROLL_DOWN:
            step = -1
        if self.interactor.GetShiftKey():
            self.scroll_axis1(step)
        elif self.interactor.GetControlKey():
            self.scroll_axis2(step)
        else:
            self.scroll_depth(step * self.sliceIncrement)
        self.get_pwxyz().Render()
        self.update_rings()
        self.update_rois()
        self.Render()
        self.lastTime = time.time()

    def update_rings(self):
        for actor in self.get_ring_actors_as_list():
            vis = actor.update()
            textActor = self.textActors[actor.get_marker().uuid]
            if vis and EventHandler().get_labels_on():
                textActor.VisibilityOn()
            else:
                textActor.VisibilityOff()

    def update_rois(self):
        for actor in self.roi_actors.values():
            actor.update()

    def interaction_event(self, *args):
        self.update_plane()
        self.update_rings()
        self.update_rois()
        self.Render()

    def update_plane(self):
        p1 = self.pw.GetPoint1()
        p2 = self.pw.GetPoint2()
        o = self.pw.GetOrigin()
        self.observer.SetPoint1(p1)
        self.observer.SetPoint2(p2)
        self.observer.SetOrigin(o)
        self.observer.UpdatePlacement()
        self.renderer.ResetCameraClippingRange()

    def OnKeyPress(self, wid, event=None):
        if event.keyval == gdk.keyval_from_name('i') or event.keyval == gdk.keyval_from_name('I'):
            xyz = self.get_cursor_position_world()
            if xyz is None:
                return
            marker = Marker(xyz=xyz, rgb=EventHandler().get_default_color(), radius=self._ratio * shared.marker_size)
            EventHandler().add_marker(marker)
            return True
        else:
            if event.keyval == gdk.keyval_from_name('r') or event.keyval == gdk.keyval_from_name('R'):
                self.set_camera(self.resetCamera)
                return True
            return MarkerWindowInteractor.OnKeyPress(self, wid, event)

    def update_viewer(self, event, *args):
        MarkerWindowInteractor.update_viewer(self, event, *args)
        if event == 'add marker':
            marker = args[0]
            self.add_ring_actor(marker)
        elif event == 'remove marker':
            marker = args[0]
            self.remove_ring_actor(marker)
        elif event == 'move marker':
            marker, pos = args
            textActor = self.textActors[marker.uuid]
            textActor.SetPosition(pos)
        elif event == 'color marker':
            marker, color = args
            actor = self.get_actor_for_marker(marker)
            actor.update()
        elif event == 'label marker':
            marker, label = args
            self.label_ring_actor(marker, label)
        elif event == 'color marker':
            marker, color = args
            actor = self.get_actor_for_marker(marker)
            actor.update()
        elif event == 'select marker':
            marker = args[0]
            actor = self.get_actor_for_marker(marker)
            actor.set_selected(True)
        elif event == 'unselect marker':
            marker = args[0]
            actor = self.get_actor_for_marker(marker)
            if actor != None:
                actor.set_selected(False)
        elif event == 'observers update plane':
            self.update_plane()
        elif event == 'set axes directions':
            self.add_axes_labels()
        self.update_rings()
        self.update_rois()
        self.Render()
        return

    def add_ring_actor(self, marker):
        ringActor = RingActor(marker, self.pw, lineWidth=self.defaultRingLine)
        vis = ringActor.update()
        self.renderer.AddActor(ringActor)
        self.ringActors[marker.uuid] = ringActor
        text = vtk.vtkVectorText()
        text.SetText(marker.get_label())
        textMapper = vtk.vtkPolyDataMapper()
        textMapper.SetInput(text.GetOutput())
        textActor = vtk.vtkFollower()
        textActor.SetMapper(textMapper)
        size = 2 * marker.get_size()
        textActor.SetScale(size, size, size)
        x, y, z = marker.get_center()
        textActor.SetPosition(x, y, z)
        textActor.SetCamera(self.camera)
        textActor.GetProperty().SetColor(marker.get_label_color())
        if EventHandler().get_labels_on() and vis:
            textActor.VisibilityOn()
        else:
            textActor.VisibilityOff()
        self.textActors[marker.uuid] = textActor
        self.renderer.AddActor(textActor)

    def remove_ring_actor(self, marker):
        actor = self.get_actor_for_marker(marker)
        if actor is None:
            return
        else:
            self.renderer.RemoveActor(actor)
            del self.ringActors[marker.uuid]
            textActor = self.textActors[marker.uuid]
            self.renderer.RemoveActor(textActor)
            del self.textActors[marker.uuid]
            return

    def label_ring_actor(self, marker, label):
        marker.set_label(label)
        text = vtk.vtkVectorText()
        text.SetText(marker.get_label())
        textMapper = vtk.vtkPolyDataMapper()
        textMapper.SetInput(text.GetOutput())
        textActor = self.textActors[marker.uuid]
        textActor.SetMapper(textMapper)

    def get_actor_for_marker(self, marker):
        if self.ringActors.has_key(marker.uuid):
            return self.ringActors[marker.uuid]
        else:
            return

    def get_ring_actors_as_list(self):
        return self.ringActors.values()

    def get_cursor_position_world(self):
        x, y = self.GetEventPosition()
        xyz = [x, y, 0.0]
        picker = vtk.vtkWorldPointPicker()
        picker.Pick(xyz, self.renderer)
        ppos = picker.GetPickPosition()
        return ppos

    def get_cursor_position(self):
        xyzv = [
         0, 0, 0, 0]
        val = self.observer.GetCursorData(xyzv)
        if val:
            return xyzv[:3]
        else:
            return
            return

    def get_pwxyz(self):
        return self.owner.pwxyz

    def get_pw(self):
        return self.pw

    def get_orientation(self):
        return self.orientation

    def obs_to_world(self, pnt):
        if not self.hasData:
            return
        spacing = self.imageData.GetSpacing()
        transform = vtk.vtkTransform()
        transform.Scale(spacing)
        return transform.TransformPoint(pnt)

    def add_roi(self, uuid, pipe, color):
        actor = RoiEdgeActor(pipe, color, self.pw)
        self.renderer.AddActor(actor)
        actor.color = color
        self.roi_actors[uuid] = actor

    def remove_roi(self, uuid):
        actor = self._get_roi_actor(uuid)
        if actor:
            self.renderer.RemoveActor(actor)
            del self.roi_actors[uuid]

    def color_roi(self, uuid, color):
        actor = self._get_roi_actor(uuid)
        if actor:
            actor.set_color(color)