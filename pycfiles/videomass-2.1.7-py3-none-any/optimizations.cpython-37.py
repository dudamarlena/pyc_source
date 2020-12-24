# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_utils/optimizations.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 8534 bytes


def vp9(prename):
    """
    evaluate the prename of optimization and return an corresponding
    string object wich must be evaluate by builtin function eval()
    
    """
    if prename == 'Default':
        return "(\n                self.ckbx_web.SetValue(False), self.on_WebOptimize(self),\n                self.ckbx_pass.SetValue(False), \n                self.cmb_Vcod.SetStringSelection('Vp9'),\n                self.spinMinr.SetValue(0), self.spinMaxr.SetValue(0),\n                self.spinBufsize.SetValue(0), self.cmb_Pixfrm.SetSelection(1),\n                self.videoCodec(self),)"
    if prename == 'Vp9 best for Archive':
        return "(\n                self.ckbx_web.SetValue(False), self.on_WebOptimize(self),\n                self.ckbx_pass.SetValue(False), self.on_Pass(self),\n                self.cmb_Vcod.SetStringSelection('Vp9'), self.videoCodec(self),\n                self.spin_Vbrate.SetValue(0), self.on_Vbitrate(self),\n                self.spinMinr.SetValue(0), self.spinMaxr.SetValue(0),\n                self.spinBufsize.SetValue(0),\n                self.slider_CRF.SetValue(30), self.on_Crf(self),\n                self.rdb_deadline.SetStringSelection('best'), \n                self.on_Deadline(self), self.spin_cpu.SetValue(1), \n                self.ckbx_rowMt1.SetValue(True),\n                self.cmb_Pixfrm.SetSelection(0), \n                self.rdb_a.SetStringSelection('OPUS'),\n                self.on_AudioCodecs(self),)"
    if prename == 'Vp9 CBR Web streaming':
        return "(\n                self.ckbx_web.SetValue(True), self.on_WebOptimize(self),\n                self.ckbx_pass.SetValue(False), self.on_Pass(self),\n                self.cmb_Vcod.SetStringSelection('Vp9'), self.videoCodec(self),\n                self.spin_Vbrate.SetValue(1000), self.on_Vbitrate(self),\n                self.spinMinr.SetValue(1000), self.spinMaxr.SetValue(1000),\n                self.spinBufsize.SetValue(0),\n                self.slider_CRF.SetValue(-1), self.on_Crf(self),\n                self.rdb_deadline.SetStringSelection('good'), \n                self.on_Deadline(self), self.spin_cpu.SetValue(0), \n                self.ckbx_rowMt1.SetValue(True),\n                self.cmb_Pixfrm.SetSelection(1),)"
    if prename == 'Vp9 Constrained ABR-VBV live streaming':
        return "(\n                self.cmb_Vcod.SetStringSelection('Vp9'), self.videoCodec(self),\n                self.ckbx_web.SetValue(True), self.on_WebOptimize(self),\n                self.ckbx_pass.SetValue(True), self.on_Pass(self),\n                self.spin_Vbrate.SetValue(1000), self.on_Vbitrate(self),\n                self.spinMaxr.SetValue(0),\n                self.spinMinr.SetValue(1000), self.spinBufsize.SetValue(2000),\n                self.slider_CRF.SetValue(-1), self.on_Crf(self),\n                self.rdb_deadline.SetStringSelection('good'), \n                self.on_Deadline(self), self.spin_cpu.SetValue(0), \n                self.ckbx_rowMt1.SetValue(True),\n                self.cmb_Pixfrm.SetSelection(0),)"


def hevc_avc(prename):
    """
    x264, x265
    evaluate the prename of optimization and return an corresponding
    string object wich must be evaluate by builtin function eval()
    
    """
    if prename == 'Default':
        return "(\n                self.ckbx_web.SetValue(False), self.on_WebOptimize(self),\n                self.ckbx_pass.SetValue(False), \n                self.cmb_Vcod.SetStringSelection('x264'),\n                self.spinMinr.SetValue(0), self.spinMaxr.SetValue(0),\n                self.spinBufsize.SetValue(0), self.cmb_Pixfrm.SetSelection(1),\n                self.videoCodec(self),)"
    if prename == 'x264 best for Archive':
        return "(\n                self.spinMinr.SetValue(0), self.spinMaxr.SetValue(0),\n                self.spinBufsize.SetValue(0),\n                self.ckbx_web.SetValue(False), self.on_WebOptimize(self),\n                self.ckbx_pass.SetValue(False), self.on_Pass(self),\n                self.cmb_Vcod.SetStringSelection('x264'), self.videoCodec(self),\n                self.cmb_Vcont.SetSelection(0), self.on_Container(self),\n                self.cmb_Pixfrm.SetSelection(0),)"
    if prename == 'x265 best for Archive':
        return "(\n                self.spinMinr.SetValue(0), self.spinMaxr.SetValue(0),\n                self.spinBufsize.SetValue(0),\n                self.ckbx_web.SetValue(False), self.on_WebOptimize(self),\n                self.ckbx_pass.SetValue(False), self.on_Pass(self),\n                self.cmb_Vcod.SetStringSelection('x265'), self.videoCodec(self),\n                self.cmb_Vcont.SetSelection(0), self.on_Container(self), \n                self.cmb_Pixfrm.SetSelection(0),)"
    if prename == 'x264 ABR for devices':
        return "(\n                self.spinMinr.SetValue(0), self.spinMaxr.SetValue(0),\n                self.spinBufsize.SetValue(0),\n                self.ckbx_web.SetValue(True), self.on_WebOptimize(self),\n                self.ckbx_pass.SetValue(True), self.on_Pass(self),\n                self.cmb_Vcod.SetStringSelection('x264'), self.videoCodec(self),\n                self.cmb_Vcont.SetSelection(0), self.on_Container(self),\n                self.spin_Vbrate.SetValue(1000), self.on_Vbitrate(self), \n                self.cmb_Pixfrm.SetSelection(1),)"
    if prename == 'x265 ABR for devices':
        return "(\n                self.spinMinr.SetValue(0), self.spinMaxr.SetValue(0),\n                self.spinBufsize.SetValue(0),\n                self.ckbx_web.SetValue(True), self.on_WebOptimize(self),\n                self.ckbx_pass.SetValue(True), self.on_Pass(self),\n                self.cmb_Vcod.SetStringSelection('x265'), self.videoCodec(self),\n                self.cmb_Vcont.SetSelection(0), self.on_Container(self),\n                self.spin_Vbrate.SetValue(1000), self.on_Vbitrate(self), \n                self.cmb_Pixfrm.SetSelection(1),)"
    if prename == 'x264 ABR-VBV live streaming':
        return "(\n                self.spinMinr.SetValue(0), self.spinMaxr.SetValue(1000),\n                self.spinBufsize.SetValue(2000),\n                self.ckbx_web.SetValue(True), self.on_WebOptimize(self),\n                self.ckbx_pass.SetValue(True), self.on_Pass(self),\n                self.cmb_Vcod.SetStringSelection('x264'), self.videoCodec(self),\n                self.cmb_Vcont.SetSelection(0), self.on_Container(self),\n                self.spin_Vbrate.SetValue(1000), self.on_Vbitrate(self), \n                self.cmb_Pixfrm.SetSelection(1),)"
    if prename == 'x265 ABR-VBV live streaming':
        return "(\n                self.spinMinr.SetValue(0), self.spinMaxr.SetValue(1000),\n                self.spinBufsize.SetValue(2000),\n                self.ckbx_web.SetValue(True), self.on_WebOptimize(self),\n                self.ckbx_pass.SetValue(True), self.on_Pass(self),\n                self.cmb_Vcod.SetStringSelection('x265'), self.videoCodec(self),\n                self.cmb_Vcont.SetSelection(0), self.on_Container(self),\n                self.spin_Vbrate.SetValue(1000), self.on_Vbitrate(self), \n                self.cmb_Pixfrm.SetSelection(1),)"