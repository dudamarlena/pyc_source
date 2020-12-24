# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_glsl.py
# Compiled at: 2012-03-17 12:57:53
"""
FILE: glsl.py                                                                
@author: Cody Precord                                                       
@summary: Lexer configuration file for GLSL source files.
                                                                         
"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id$'
__revision__ = '$Revision$'
import wx.stc as stc, re, synglob, syndata, _cpp
GLSL_KEYWORDS = (0, 'attribute uniform varying const layout centroid varying flat smooth noperspective patch sample break continue do for while switch case default if else subroutine in out inout true false invariant discard return lowp mediump highp precision')
GLSL_TYPES = (1, 'mat2 mat3 float double int void bool mat4 dmat2 dmat3 dmat4 mat2x2 mat2x3 mat2x4 dmat2x2 dmat2x3 dmat2x4 mat3x2 mat3x3 mat3x4 dmat3x2 dmat3x3 dmat3x4 mat4x2 mat4x3 mat4x4 dmat4x2 dmat4x3 dmat4x4 vec2 vec3 vec4 ivec2 ivec3 ivec4 bvec2 bvec3 bvec4 dvec2 dvec3 dvec4 uint uvec2 uvec3 uvec4 sampler1D sampler2D sampler3D samplerCube sampler1DShadow sampler2DShadow samplerCubeShadow sampler1DArray sampler2DArray sampler1DArrayShadow sampler2DArrayShadow isampler1D isampler2D isampler3D isamplerCube isampler1DArray isampler2DArray usampler1D usampler2D usampler3D usamplerCube usampler1DArray usampler2DArray sampler2DRect sampler2DRectShadow isampler2DRect usampler2DRect samplerBuffer isamplerBuffer usamplerBuffer sampler2DMS isampler2DMS usampler2DMS sampler2DMSArray isampler2DMSArray usampler2DMSArray samplerCubeArray samplerCubeArrayShadow isamplerCubeArray usamplerCubeArray struct')

class SyntaxData(_cpp.SyntaxData):
    """SyntaxData object for many C like languages"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)

    def GetKeywords(self):
        """Returns Specified Keywords List"""
        return [
         GLSL_KEYWORDS, GLSL_TYPES, _cpp.DOC_KEYWORDS]