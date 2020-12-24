# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/motmot/wxvalidatedtext/demo.py
# Compiled at: 2009-05-10 22:06:09
import pkg_resources, wxvalidatedtext as wxvt, wx, wx.xrc as xrc, os
RESFILE = pkg_resources.resource_filename(__name__, 'demo.xrc')
RESDIR = os.path.split(RESFILE)[0]
RES = xrc.EmptyXmlResource()
RES.LoadFromString(open(RESFILE).read())

def validate_int_range(val_str):
    try:
        val = int(val_str)
    except ValueError, err:
        return False

    if 20 < val < 100:
        return True
    else:
        return False


class MyApp(wx.App):

    def OnInit(self):
        self.frame = RES.LoadFrame(None, 'TEST_FRAME')
        ctrl = xrc.XRCCTRL(self.frame, 'TEXT_ENTRY_INT')
        wxvt.setup_validated_integer_callback(ctrl, ctrl.GetId(), self.OnValidInteger)
        ctrl = xrc.XRCCTRL(self.frame, 'TEXT_ENTRY_FLOAT')
        wxvt.setup_validated_float_callback(ctrl, ctrl.GetId(), self.OnValidFloat)
        ctrl = xrc.XRCCTRL(self.frame, 'TEXT_ENTRY_CUSTOM')
        validator = wxvt.Validator(ctrl, ctrl.GetId(), self.OnValidCustom, validate_int_range)
        self.frame.Show(True)
        return True

    def OnValidInteger(self, event):
        print 'validated integer:', int(event.GetEventObject().GetValue())

    def OnValidFloat(self, event):
        print 'validated float:', float(event.GetEventObject().GetValue())

    def OnValidCustom(self, event):
        print 'validated custom value:', int(event.GetEventObject().GetValue())


def main():
    app = MyApp(0)
    app.MainLoop()


if __name__ == '__main__':
    main()