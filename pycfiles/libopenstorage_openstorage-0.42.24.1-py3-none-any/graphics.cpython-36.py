# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/graphics.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 38259 bytes
"""
    pygments.lexers.graphics
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for computer graphics and plotting related languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, words, include, bygroups, using, this, default
from pygments.token import Text, Comment, Operator, Keyword, Name, Number, Punctuation, String
__all__ = [
 'GLShaderLexer', 'PostScriptLexer', 'AsymptoteLexer', 'GnuplotLexer',
 'PovrayLexer', 'HLSLShaderLexer']

class GLShaderLexer(RegexLexer):
    __doc__ = '\n    GLSL (OpenGL Shader) lexer.\n\n    .. versionadded:: 1.1\n    '
    name = 'GLSL'
    aliases = ['glsl']
    filenames = ['*.vert', '*.frag', '*.geo']
    mimetypes = ['text/x-glslsrc']
    tokens = {'root': [
              (
               '^#.*', Comment.Preproc),
              (
               '//.*', Comment.Single),
              (
               '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
              (
               '\\+|-|~|!=?|\\*|/|%|<<|>>|<=?|>=?|==?|&&?|\\^|\\|\\|?',
               Operator),
              (
               '[?:]', Operator),
              (
               '\\bdefined\\b', Operator),
              (
               '[;{}(),\\[\\]]', Punctuation),
              (
               '[+-]?\\d*\\.\\d+([eE][-+]?\\d+)?', Number.Float),
              (
               '[+-]?\\d+\\.\\d*([eE][-+]?\\d+)?', Number.Float),
              (
               '0[xX][0-9a-fA-F]*', Number.Hex),
              (
               '0[0-7]*', Number.Oct),
              (
               '[1-9][0-9]*', Number.Integer),
              (
               words(('attribute', 'const', 'uniform', 'varying', 'buffer', 'shared', 'in', 'out',
       'layout', 'flat', 'smooth', 'noperspective', 'centroid', 'sample', 'patch',
       'inout', 'lowp', 'mediump', 'highp', 'precision', 'invariant', 'precise',
       'coherent', 'volatile', 'restrict', 'readonly', 'writeonly', 'break', 'continue',
       'do', 'for', 'while', 'switch', 'case', 'default', 'if', 'else', 'subroutine',
       'discard', 'return', 'struct'),
                 prefix='\\b',
                 suffix='\\b'),
               Keyword),
              (
               words(('true', 'false'),
                 prefix='\\b',
                 suffix='\\b'),
               Keyword.Constant),
              (
               words(('void', 'atomic_uint', 'float', 'vec2', 'vec3', 'vec4', 'double', 'dvec2', 'dvec3',
       'dvec4', 'int', 'ivec2', 'ivec3', 'ivec4', 'uint', 'uvec2', 'uvec3', 'uvec4',
       'bool', 'bvec2', 'bvec3', 'bvec4', 'mat2', 'mat3', 'mat4', 'dmat2', 'dmat3',
       'dmat4', 'mat2x2', 'mat2x3', 'mat2x4', 'dmat2x2', 'dmat2x3', 'dmat2x4', 'mat3x2',
       'mat3x3', 'mat3x4', 'dmat3x2', 'dmat3x3', 'dmat3x4', 'mat4x2', 'mat4x3', 'mat4x4',
       'dmat4x2', 'dmat4x3', 'dmat4x4', 'sampler1D', 'sampler2D', 'sampler3D', 'samplerCube',
       'sampler1DArray', 'sampler2DArray', 'samplerCubeArray', 'sampler2DRect', 'samplerBuffer',
       'sampler2DMS', 'sampler2DMSArray', 'sampler1DShadow', 'sampler2DShadow', 'samplerCubeShadow',
       'sampler1DArrayShadow', 'sampler2DArrayShadow', 'samplerCubeArrayShadow',
       'sampler2DRectShadow', 'isampler1D', 'isampler2D', 'isampler3D', 'isamplerCube',
       'isampler1DArray', 'isampler2DArray', 'isamplerCubeArray', 'isampler2DRect',
       'isamplerBuffer', 'isampler2DMS', 'isampler2DMSArray', 'usampler1D', 'usampler2D',
       'usampler3D', 'usamplerCube', 'usampler1DArray', 'usampler2DArray', 'usamplerCubeArray',
       'usampler2DRect', 'usamplerBuffer', 'usampler2DMS', 'usampler2DMSArray', 'image1D',
       'image2D', 'image3D', 'imageCube', 'image1DArray', 'image2DArray', 'imageCubeArray',
       'image2DRect', 'imageBuffer', 'image2DMS', 'image2DMSArray', 'iimage1D', 'iimage2D',
       'iimage3D', 'iimageCube', 'iimage1DArray', 'iimage2DArray', 'iimageCubeArray',
       'iimage2DRect', 'iimageBuffer', 'iimage2DMS', 'iimage2DMSArray', 'uimage1D',
       'uimage2D', 'uimage3D', 'uimageCube', 'uimage1DArray', 'uimage2DArray', 'uimageCubeArray',
       'uimage2DRect', 'uimageBuffer', 'uimage2DMS', 'uimage2DMSArray'),
                 prefix='\\b',
                 suffix='\\b'),
               Keyword.Type),
              (
               words(('common', 'partition', 'active', 'asm', 'class', 'union', 'enum', 'typedef',
       'template', 'this', 'resource', 'goto', 'inline', 'noinline', 'public', 'static',
       'extern', 'external', 'interface', 'long', 'short', 'half', 'fixed', 'unsigned',
       'superp', 'input', 'output', 'hvec2', 'hvec3', 'hvec4', 'fvec2', 'fvec3',
       'fvec4', 'sampler3DRect', 'filter', 'sizeof', 'cast', 'namespace', 'using'),
                 prefix='\\b',
                 suffix='\\b'),
               Keyword.Reserved),
              (
               'gl_\\w*', Name.Builtin),
              (
               '[a-zA-Z_]\\w*', Name),
              (
               '\\.', Punctuation),
              (
               '\\s+', Text)]}


class HLSLShaderLexer(RegexLexer):
    __doc__ = '\n    HLSL (Microsoft Direct3D Shader) lexer.\n\n    .. versionadded:: 2.3\n    '
    name = 'HLSL'
    aliases = ['hlsl']
    filenames = ['*.hlsl', '*.hlsli']
    mimetypes = ['text/x-hlsl']
    tokens = {'root':[
      (
       '^#.*', Comment.Preproc),
      (
       '//.*', Comment.Single),
      (
       '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
      (
       '\\+|-|~|!=?|\\*|/|%|<<|>>|<=?|>=?|==?|&&?|\\^|\\|\\|?',
       Operator),
      (
       '[?:]', Operator),
      (
       '\\bdefined\\b', Operator),
      (
       '[;{}(),.\\[\\]]', Punctuation),
      (
       '[+-]?\\d*\\.\\d+([eE][-+]?\\d+)?f?', Number.Float),
      (
       '[+-]?\\d+\\.\\d*([eE][-+]?\\d+)?f?', Number.Float),
      (
       '0[xX][0-9a-fA-F]*', Number.Hex),
      (
       '0[0-7]*', Number.Oct),
      (
       '[1-9][0-9]*', Number.Integer),
      (
       '"', String, 'string'),
      (
       words(('asm', 'asm_fragment', 'break', 'case', 'cbuffer', 'centroid', 'class', 'column_major',
       'compile', 'compile_fragment', 'const', 'continue', 'default', 'discard',
       'do', 'else', 'export', 'extern', 'for', 'fxgroup', 'globallycoherent', 'groupshared',
       'if', 'in', 'inline', 'inout', 'interface', 'line', 'lineadj', 'linear', 'namespace',
       'nointerpolation', 'noperspective', 'NULL', 'out', 'packoffset', 'pass', 'pixelfragment',
       'point', 'precise', 'return', 'register', 'row_major', 'sample', 'sampler',
       'shared', 'stateblock', 'stateblock_state', 'static', 'struct', 'switch',
       'tbuffer', 'technique', 'technique10', 'technique11', 'texture', 'typedef',
       'triangle', 'triangleadj', 'uniform', 'vertexfragment', 'volatile', 'while'),
         prefix='\\b',
         suffix='\\b'),
       Keyword),
      (
       words(('true', 'false'), prefix='\\b', suffix='\\b'),
       Keyword.Constant),
      (
       words(('auto', 'catch', 'char', 'const_cast', 'delete', 'dynamic_cast', 'enum', 'explicit',
       'friend', 'goto', 'long', 'mutable', 'new', 'operator', 'private', 'protected',
       'public', 'reinterpret_cast', 'short', 'signed', 'sizeof', 'static_cast',
       'template', 'this', 'throw', 'try', 'typename', 'union', 'unsigned', 'using',
       'virtual'),
         prefix='\\b',
         suffix='\\b'),
       Keyword.Reserved),
      (
       words(('dword', 'matrix', 'snorm', 'string', 'unorm', 'unsigned', 'void', 'vector',
       'BlendState', 'Buffer', 'ByteAddressBuffer', 'ComputeShader', 'DepthStencilState',
       'DepthStencilView', 'DomainShader', 'GeometryShader', 'HullShader', 'InputPatch',
       'LineStream', 'OutputPatch', 'PixelShader', 'PointStream', 'RasterizerState',
       'RenderTargetView', 'RasterizerOrderedBuffer', 'RasterizerOrderedByteAddressBuffer',
       'RasterizerOrderedStructuredBuffer', 'RasterizerOrderedTexture1D', 'RasterizerOrderedTexture1DArray',
       'RasterizerOrderedTexture2D', 'RasterizerOrderedTexture2DArray', 'RasterizerOrderedTexture3D',
       'RWBuffer', 'RWByteAddressBuffer', 'RWStructuredBuffer', 'RWTexture1D', 'RWTexture1DArray',
       'RWTexture2D', 'RWTexture2DArray', 'RWTexture3D', 'SamplerState', 'SamplerComparisonState',
       'StructuredBuffer', 'Texture1D', 'Texture1DArray', 'Texture2D', 'Texture2DArray',
       'Texture2DMS', 'Texture2DMSArray', 'Texture3D', 'TextureCube', 'TextureCubeArray',
       'TriangleStream', 'VertexShader'),
         prefix='\\b',
         suffix='\\b'),
       Keyword.Type),
      (
       words(('bool', 'double', 'float', 'int', 'half', 'min16float', 'min10float', 'min16int',
       'min12int', 'min16uint', 'uint'),
         prefix='\\b',
         suffix='([1-4](x[1-4])?)?\\b'),
       Keyword.Type),
      (
       words(('abort', 'abs', 'acos', 'all', 'AllMemoryBarrier', 'AllMemoryBarrierWithGroupSync',
       'any', 'AppendStructuredBuffer', 'asdouble', 'asfloat', 'asin', 'asint', 'asuint',
       'asuint', 'atan', 'atan2', 'ceil', 'CheckAccessFullyMapped', 'clamp', 'clip',
       'CompileShader', 'ConsumeStructuredBuffer', 'cos', 'cosh', 'countbits', 'cross',
       'D3DCOLORtoUBYTE4', 'ddx', 'ddx_coarse', 'ddx_fine', 'ddy', 'ddy_coarse',
       'ddy_fine', 'degrees', 'determinant', 'DeviceMemoryBarrier', 'DeviceMemoryBarrierWithGroupSync',
       'distance', 'dot', 'dst', 'errorf', 'EvaluateAttributeAtCentroid', 'EvaluateAttributeAtSample',
       'EvaluateAttributeSnapped', 'exp', 'exp2', 'f16tof32', 'f32tof16', 'faceforward',
       'firstbithigh', 'firstbitlow', 'floor', 'fma', 'fmod', 'frac', 'frexp', 'fwidth',
       'GetRenderTargetSampleCount', 'GetRenderTargetSamplePosition', 'GlobalOrderedCountIncrement',
       'GroupMemoryBarrier', 'GroupMemoryBarrierWithGroupSync', 'InterlockedAdd',
       'InterlockedAnd', 'InterlockedCompareExchange', 'InterlockedCompareStore',
       'InterlockedExchange', 'InterlockedMax', 'InterlockedMin', 'InterlockedOr',
       'InterlockedXor', 'isfinite', 'isinf', 'isnan', 'ldexp', 'length', 'lerp',
       'lit', 'log', 'log10', 'log2', 'mad', 'max', 'min', 'modf', 'msad4', 'mul',
       'noise', 'normalize', 'pow', 'printf', 'Process2DQuadTessFactorsAvg', 'Process2DQuadTessFactorsMax',
       'Process2DQuadTessFactorsMin', 'ProcessIsolineTessFactors', 'ProcessQuadTessFactorsAvg',
       'ProcessQuadTessFactorsMax', 'ProcessQuadTessFactorsMin', 'ProcessTriTessFactorsAvg',
       'ProcessTriTessFactorsMax', 'ProcessTriTessFactorsMin', 'QuadReadLaneAt',
       'QuadSwapX', 'QuadSwapY', 'radians', 'rcp', 'reflect', 'refract', 'reversebits',
       'round', 'rsqrt', 'saturate', 'sign', 'sin', 'sincos', 'sinh', 'smoothstep',
       'sqrt', 'step', 'tan', 'tanh', 'tex1D', 'tex1D', 'tex1Dbias', 'tex1Dgrad',
       'tex1Dlod', 'tex1Dproj', 'tex2D', 'tex2D', 'tex2Dbias', 'tex2Dgrad', 'tex2Dlod',
       'tex2Dproj', 'tex3D', 'tex3D', 'tex3Dbias', 'tex3Dgrad', 'tex3Dlod', 'tex3Dproj',
       'texCUBE', 'texCUBE', 'texCUBEbias', 'texCUBEgrad', 'texCUBElod', 'texCUBEproj',
       'transpose', 'trunc', 'WaveAllBitAnd', 'WaveAllMax', 'WaveAllMin', 'WaveAllBitOr',
       'WaveAllBitXor', 'WaveAllEqual', 'WaveAllProduct', 'WaveAllSum', 'WaveAllTrue',
       'WaveAnyTrue', 'WaveBallot', 'WaveGetLaneCount', 'WaveGetLaneIndex', 'WaveGetOrderedIndex',
       'WaveIsHelperLane', 'WaveOnce', 'WavePrefixProduct', 'WavePrefixSum', 'WaveReadFirstLane',
       'WaveReadLaneAt'),
         prefix='\\b',
         suffix='\\b'),
       Name.Builtin),
      (
       words(('SV_ClipDistance', 'SV_ClipDistance0', 'SV_ClipDistance1', 'SV_Culldistance',
       'SV_CullDistance0', 'SV_CullDistance1', 'SV_Coverage', 'SV_Depth', 'SV_DepthGreaterEqual',
       'SV_DepthLessEqual', 'SV_DispatchThreadID', 'SV_DomainLocation', 'SV_GroupID',
       'SV_GroupIndex', 'SV_GroupThreadID', 'SV_GSInstanceID', 'SV_InnerCoverage',
       'SV_InsideTessFactor', 'SV_InstanceID', 'SV_IsFrontFace', 'SV_OutputControlPointID',
       'SV_Position', 'SV_PrimitiveID', 'SV_RenderTargetArrayIndex', 'SV_SampleIndex',
       'SV_StencilRef', 'SV_TessFactor', 'SV_VertexID', 'SV_ViewportArrayIndex'),
         prefix='\\b',
         suffix='\\b'),
       Name.Decorator),
      (
       '\\bSV_Target[0-7]?\\b', Name.Decorator),
      (
       words(('allow_uav_condition', 'branch', 'call', 'domain', 'earlydepthstencil', 'fastopt',
       'flatten', 'forcecase', 'instance', 'loop', 'maxtessfactor', 'numthreads',
       'outputcontrolpoints', 'outputtopology', 'partitioning', 'patchconstantfunc',
       'unroll'),
         prefix='\\b',
         suffix='\\b'),
       Name.Decorator),
      (
       '[a-zA-Z_]\\w*', Name),
      (
       '\\\\$', Comment.Preproc),
      (
       '\\s+', Text)], 
     'string':[
      (
       '"', String, '#pop'),
      (
       '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|[0-7]{1,3})',
       String.Escape),
      (
       '[^\\\\"\\n]+', String),
      (
       '\\\\\\n', String),
      (
       '\\\\', String)]}


class PostScriptLexer(RegexLexer):
    __doc__ = '\n    Lexer for PostScript files.\n\n    The PostScript Language Reference published by Adobe at\n    <http://partners.adobe.com/public/developer/en/ps/PLRM.pdf>\n    is the authority for this.\n\n    .. versionadded:: 1.4\n    '
    name = 'PostScript'
    aliases = ['postscript', 'postscr']
    filenames = ['*.ps', '*.eps']
    mimetypes = ['application/postscript']
    delimiter = '()<>\\[\\]{}/%\\s'
    delimiter_end = '(?=[%s])' % delimiter
    valid_name_chars = '[^%s]' % delimiter
    valid_name = '%s+%s' % (valid_name_chars, delimiter_end)
    tokens = {'root':[
      (
       '^%!.+\\n', Comment.Preproc),
      (
       '%%.*\\n', Comment.Special),
      (
       '(^%.*\\n){2,}', Comment.Multiline),
      (
       '%.*\\n', Comment.Single),
      (
       '\\(', String, 'stringliteral'),
      (
       '[{}<>\\[\\]]', Punctuation),
      (
       '<[0-9A-Fa-f]+>' + delimiter_end, Number.Hex),
      (
       '[0-9]+\\#(\\-|\\+)?([0-9]+\\.?|[0-9]*\\.[0-9]+|[0-9]+\\.[0-9]*)((e|E)[0-9]+)?' + delimiter_end, Number.Oct),
      (
       '(\\-|\\+)?([0-9]+\\.?|[0-9]*\\.[0-9]+|[0-9]+\\.[0-9]*)((e|E)[0-9]+)?' + delimiter_end, Number.Float),
      (
       '(\\-|\\+)?[0-9]+' + delimiter_end, Number.Integer),
      (
       '\\/%s' % valid_name, Name.Variable),
      (
       valid_name, Name.Function),
      (
       '(false|true)' + delimiter_end, Keyword.Constant),
      (
       '(eq|ne|g[et]|l[et]|and|or|not|if(?:else)?|for(?:all)?)' + delimiter_end, Keyword.Reserved),
      (
       words(('abs', 'add', 'aload', 'arc', 'arcn', 'array', 'atan', 'begin', 'bind', 'ceiling',
       'charpath', 'clip', 'closepath', 'concat', 'concatmatrix', 'copy', 'cos',
       'currentlinewidth', 'currentmatrix', 'currentpoint', 'curveto', 'cvi', 'cvs',
       'def', 'defaultmatrix', 'dict', 'dictstackoverflow', 'div', 'dtransform',
       'dup', 'end', 'exch', 'exec', 'exit', 'exp', 'fill', 'findfont', 'floor',
       'get', 'getinterval', 'grestore', 'gsave', 'gt', 'identmatrix', 'idiv', 'idtransform',
       'index', 'invertmatrix', 'itransform', 'length', 'lineto', 'ln', 'load', 'log',
       'loop', 'matrix', 'mod', 'moveto', 'mul', 'neg', 'newpath', 'pathforall',
       'pathbbox', 'pop', 'print', 'pstack', 'put', 'quit', 'rand', 'rangecheck',
       'rcurveto', 'repeat', 'restore', 'rlineto', 'rmoveto', 'roll', 'rotate', 'round',
       'run', 'save', 'scale', 'scalefont', 'setdash', 'setfont', 'setgray', 'setlinecap',
       'setlinejoin', 'setlinewidth', 'setmatrix', 'setrgbcolor', 'shfill', 'show',
       'showpage', 'sin', 'sqrt', 'stack', 'stringwidth', 'stroke', 'strokepath',
       'sub', 'syntaxerror', 'transform', 'translate', 'truncate', 'typecheck', 'undefined',
       'undefinedfilename', 'undefinedresult'),
         suffix=delimiter_end),
       Name.Builtin),
      (
       '\\s+', Text)], 
     'stringliteral':[
      (
       '[^()\\\\]+', String),
      (
       '\\\\', String.Escape, 'escape'),
      (
       '\\(', String, '#push'),
      (
       '\\)', String, '#pop')], 
     'escape':[
      (
       '[0-8]{3}|n|r|t|b|f|\\\\|\\(|\\)', String.Escape, '#pop'),
      default('#pop')]}


class AsymptoteLexer(RegexLexer):
    __doc__ = '\n    For `Asymptote <http://asymptote.sf.net/>`_ source code.\n\n    .. versionadded:: 1.2\n    '
    name = 'Asymptote'
    aliases = ['asy', 'asymptote']
    filenames = ['*.asy']
    mimetypes = ['text/x-asymptote']
    _ws = '(?:\\s|//.*?\\n|/\\*.*?\\*/)+'
    tokens = {'whitespace':[
      (
       '\\n', Text),
      (
       '\\s+', Text),
      (
       '\\\\\\n', Text),
      (
       '//(\\n|(.|\\n)*?[^\\\\]\\n)', Comment),
      (
       '/(\\\\\\n)?\\*(.|\\n)*?\\*(\\\\\\n)?/', Comment)], 
     'statements':[
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       "'", String, 'string'),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[lL]?', Number.Float),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
      (
       '0x[0-9a-fA-F]+[Ll]?', Number.Hex),
      (
       '0[0-7]+[Ll]?', Number.Oct),
      (
       '\\d+[Ll]?', Number.Integer),
      (
       '[~!%^&*+=|?:<>/-]', Operator),
      (
       '[()\\[\\],.]', Punctuation),
      (
       '\\b(case)(.+?)(:)', bygroups(Keyword, using(this), Text)),
      (
       '(and|controls|tension|atleast|curl|if|else|while|for|do|return|break|continue|struct|typedef|new|access|import|unravel|from|include|quote|static|public|private|restricted|this|explicit|true|false|null|cycle|newframe|operator)\\b',
       Keyword),
      (
       '(Braid|FitResult|Label|Legend|TreeNode|abscissa|arc|arrowhead|binarytree|binarytreeNode|block|bool|bool3|bounds|bqe|circle|conic|coord|coordsys|cputime|ellipse|file|filltype|frame|grid3|guide|horner|hsv|hyperbola|indexedTransform|int|inversion|key|light|line|linefit|marginT|marker|mass|object|pair|parabola|path|path3|pen|picture|point|position|projection|real|revolution|scaleT|scientific|segment|side|slice|splitface|string|surface|tensionSpecifier|ticklocate|ticksgridT|tickvalues|transform|transformation|tree|triangle|trilinear|triple|vector|vertex|void)(?=\\s+[a-zA-Z])',
       Keyword.Type),
      (
       '(Braid|FitResult|TreeNode|abscissa|arrowhead|block|bool|bool3|bounds|coord|frame|guide|horner|int|linefit|marginT|pair|pen|picture|position|real|revolution|slice|splitface|ticksgridT|tickvalues|tree|triple|vertex|void)\\b',
       Keyword.Type),
      (
       '[a-zA-Z_]\\w*:(?!:)', Name.Label),
      (
       '[a-zA-Z_]\\w*', Name)], 
     'root':[
      include('whitespace'),
      (
       '((?:[\\w*\\s])+?(?:\\s|\\*))([a-zA-Z_]\\w*)(\\s*\\([^;]*?\\))(' + _ws + ')(\\{)',
       bygroups(using(this), Name.Function, using(this), using(this), Punctuation),
       'function'),
      (
       '((?:[\\w*\\s])+?(?:\\s|\\*))([a-zA-Z_]\\w*)(\\s*\\([^;]*?\\))(' + _ws + ')(;)',
       bygroups(using(this), Name.Function, using(this), using(this), Punctuation)),
      default('statement')], 
     'statement':[
      include('whitespace'),
      include('statements'),
      (
       '[{}]', Punctuation),
      (
       ';', Punctuation, '#pop')], 
     'function':[
      include('whitespace'),
      include('statements'),
      (
       ';', Punctuation),
      (
       '\\{', Punctuation, '#push'),
      (
       '\\}', Punctuation, '#pop')], 
     'string':[
      (
       "'", String, '#pop'),
      (
       '\\\\([\\\\abfnrtv"\\\'?]|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
      (
       '\\n', String),
      (
       "[^\\\\'\\n]+", String),
      (
       '\\\\\\n', String),
      (
       '\\\\n', String),
      (
       '\\\\', String)]}

    def get_tokens_unprocessed(self, text):
        from pygments.lexers._asy_builtins import ASYFUNCNAME, ASYVARNAME
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if value in ASYFUNCNAME:
                    token = Name.Function
            if token is Name:
                if value in ASYVARNAME:
                    token = Name.Variable
            yield (
             index, token, value)


def _shortened(word):
    dpos = word.find('$')
    return '|'.join(word[:dpos] + word[dpos + 1:i] + '\\b' for i in range(len(word), dpos, -1))


def _shortened_many(*words):
    return '|'.join(map(_shortened, words))


class GnuplotLexer(RegexLexer):
    __doc__ = '\n    For `Gnuplot <http://gnuplot.info/>`_ plotting scripts.\n\n    .. versionadded:: 0.11\n    '
    name = 'Gnuplot'
    aliases = ['gnuplot']
    filenames = ['*.plot', '*.plt']
    mimetypes = ['text/x-gnuplot']
    tokens = {'root':[
      include('whitespace'),
      (
       _shortened('bi$nd'), Keyword, 'bind'),
      (
       _shortened_many('ex$it', 'q$uit'), Keyword, 'quit'),
      (
       _shortened('f$it'), Keyword, 'fit'),
      (
       '(if)(\\s*)(\\()', bygroups(Keyword, Text, Punctuation), 'if'),
      (
       'else\\b', Keyword),
      (
       _shortened('pa$use'), Keyword, 'pause'),
      (
       _shortened_many('p$lot', 'rep$lot', 'sp$lot'), Keyword, 'plot'),
      (
       _shortened('sa$ve'), Keyword, 'save'),
      (
       _shortened('se$t'), Keyword, ('genericargs', 'optionarg')),
      (
       _shortened_many('sh$ow', 'uns$et'),
       Keyword, ('noargs', 'optionarg')),
      (
       _shortened_many('low$er', 'ra$ise', 'ca$ll', 'cd$', 'cl$ear', 'h$elp', '\\?$', 'hi$story', 'l$oad', 'pr$int', 'pwd$', 're$read', 'res$et', 'scr$eendump', 'she$ll', 'sy$stem', 'up$date'),
       Keyword, 'genericargs'),
      (
       _shortened_many('pwd$', 're$read', 'res$et', 'scr$eendump', 'she$ll', 'test$'),
       Keyword, 'noargs'),
      (
       '([a-zA-Z_]\\w*)(\\s*)(=)',
       bygroups(Name.Variable, Text, Operator), 'genericargs'),
      (
       '([a-zA-Z_]\\w*)(\\s*\\(.*?\\)\\s*)(=)',
       bygroups(Name.Function, Text, Operator), 'genericargs'),
      (
       '@[a-zA-Z_]\\w*', Name.Constant),
      (
       ';', Keyword)], 
     'comment':[
      (
       '[^\\\\\\n]', Comment),
      (
       '\\\\\\n', Comment),
      (
       '\\\\', Comment),
      default('#pop')], 
     'whitespace':[
      (
       '#', Comment, 'comment'),
      (
       '[ \\t\\v\\f]+', Text)], 
     'noargs':[
      include('whitespace'),
      (
       ';', Punctuation, '#pop'),
      (
       '\\n', Text, '#pop')], 
     'dqstring':[
      (
       '"', String, '#pop'),
      (
       '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
      (
       '[^\\\\"\\n]+', String),
      (
       '\\\\\\n', String),
      (
       '\\\\', String),
      (
       '\\n', String, '#pop')], 
     'sqstring':[
      (
       "''", String),
      (
       "'", String, '#pop'),
      (
       "[^\\\\'\\n]+", String),
      (
       '\\\\\\n', String),
      (
       '\\\\', String),
      (
       '\\n', String, '#pop')], 
     'genericargs':[
      include('noargs'),
      (
       '"', String, 'dqstring'),
      (
       "'", String, 'sqstring'),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+', Number.Float),
      (
       '(\\d+\\.\\d*|\\.\\d+)', Number.Float),
      (
       '-?\\d+', Number.Integer),
      (
       '[,.~!%^&*+=|?:<>/-]', Operator),
      (
       '[{}()\\[\\]]', Punctuation),
      (
       '(eq|ne)\\b', Operator.Word),
      (
       '([a-zA-Z_]\\w*)(\\s*)(\\()',
       bygroups(Name.Function, Text, Punctuation)),
      (
       '[a-zA-Z_]\\w*', Name),
      (
       '@[a-zA-Z_]\\w*', Name.Constant),
      (
       '\\\\\\n', Text)], 
     'optionarg':[
      include('whitespace'),
      (
       _shortened_many('a$ll', 'an$gles', 'ar$row', 'au$toscale', 'b$ars', 'bor$der', 'box$width', 'cl$abel', 'c$lip', 'cn$trparam', 'co$ntour', 'da$ta', 'data$file', 'dg$rid3d', 'du$mmy', 'enc$oding', 'dec$imalsign', 'fit$', 'font$path', 'fo$rmat', 'fu$nction', 'fu$nctions', 'g$rid', 'hid$den3d', 'his$torysize', 'is$osamples', 'k$ey', 'keyt$itle', 'la$bel', 'li$nestyle', 'ls$', 'loa$dpath', 'loc$ale', 'log$scale', 'mac$ros', 'map$ping', 'map$ping3d', 'mar$gin', 'lmar$gin', 'rmar$gin', 'tmar$gin', 'bmar$gin', 'mo$use', 'multi$plot', 'mxt$ics', 'nomxt$ics', 'mx2t$ics', 'nomx2t$ics', 'myt$ics', 'nomyt$ics', 'my2t$ics', 'nomy2t$ics', 'mzt$ics', 'nomzt$ics', 'mcbt$ics', 'nomcbt$ics', 'of$fsets', 'or$igin', 'o$utput', 'pa$rametric', 'pm$3d', 'pal$ette', 'colorb$ox', 'p$lot', 'poi$ntsize', 'pol$ar', 'pr$int', 'obj$ect', 'sa$mples', 'si$ze', 'st$yle', 'su$rface', 'table$', 't$erminal', 'termo$ptions', 'ti$cs', 'ticsc$ale', 'ticsl$evel', 'timef$mt', 'tim$estamp', 'tit$le', 'v$ariables', 've$rsion', 'vi$ew', 'xyp$lane', 'xda$ta', 'x2da$ta', 'yda$ta', 'y2da$ta', 'zda$ta', 'cbda$ta', 'xl$abel', 'x2l$abel', 'yl$abel', 'y2l$abel', 'zl$abel', 'cbl$abel', 'xti$cs', 'noxti$cs', 'x2ti$cs', 'nox2ti$cs', 'yti$cs', 'noyti$cs', 'y2ti$cs', 'noy2ti$cs', 'zti$cs', 'nozti$cs', 'cbti$cs', 'nocbti$cs', 'xdti$cs', 'noxdti$cs', 'x2dti$cs', 'nox2dti$cs', 'ydti$cs', 'noydti$cs', 'y2dti$cs', 'noy2dti$cs', 'zdti$cs', 'nozdti$cs', 'cbdti$cs', 'nocbdti$cs', 'xmti$cs', 'noxmti$cs', 'x2mti$cs', 'nox2mti$cs', 'ymti$cs', 'noymti$cs', 'y2mti$cs', 'noy2mti$cs', 'zmti$cs', 'nozmti$cs', 'cbmti$cs', 'nocbmti$cs', 'xr$ange', 'x2r$ange', 'yr$ange', 'y2r$ange', 'zr$ange', 'cbr$ange', 'rr$ange', 'tr$ange', 'ur$ange', 'vr$ange', 'xzeroa$xis', 'x2zeroa$xis', 'yzeroa$xis', 'y2zeroa$xis', 'zzeroa$xis', 'zeroa$xis', 'z$ero'), Name.Builtin, '#pop')], 
     'bind':[
      (
       '!', Keyword, '#pop'),
      (
       _shortened('all$windows'), Name.Builtin),
      include('genericargs')], 
     'quit':[
      (
       'gnuplot\\b', Keyword),
      include('noargs')], 
     'fit':[
      (
       'via\\b', Name.Builtin),
      include('plot')], 
     'if':[
      (
       '\\)', Punctuation, '#pop'),
      include('genericargs')], 
     'pause':[
      (
       '(mouse|any|button1|button2|button3)\\b', Name.Builtin),
      (
       _shortened('key$press'), Name.Builtin),
      include('genericargs')], 
     'plot':[
      (
       _shortened_many('ax$es', 'axi$s', 'bin$ary', 'ev$ery', 'i$ndex', 'mat$rix', 's$mooth', 'thru$', 't$itle', 'not$itle', 'u$sing', 'w$ith'),
       Name.Builtin),
      include('genericargs')], 
     'save':[
      (
       _shortened_many('f$unctions', 's$et', 't$erminal', 'v$ariables'),
       Name.Builtin),
      include('genericargs')]}


class PovrayLexer(RegexLexer):
    __doc__ = '\n    For `Persistence of Vision Raytracer <http://www.povray.org/>`_ files.\n\n    .. versionadded:: 0.11\n    '
    name = 'POVRay'
    aliases = ['pov']
    filenames = ['*.pov', '*.inc']
    mimetypes = ['text/x-povray']
    tokens = {'root': [
              (
               '/\\*[\\w\\W]*?\\*/', Comment.Multiline),
              (
               '//.*\\n', Comment.Single),
              (
               '(?s)"(?:\\\\.|[^"\\\\])+"', String.Double),
              (
               words(('break', 'case', 'debug', 'declare', 'default', 'define', 'else', 'elseif',
       'end', 'error', 'fclose', 'fopen', 'for', 'if', 'ifdef', 'ifndef', 'include',
       'local', 'macro', 'range', 'read', 'render', 'statistics', 'switch', 'undef',
       'version', 'warning', 'while', 'write'),
                 prefix='#', suffix='\\b'),
               Comment.Preproc),
              (
               words(('aa_level', 'aa_threshold', 'abs', 'acos', 'acosh', 'adaptive', 'adc_bailout',
       'agate', 'agate_turb', 'all', 'alpha', 'ambient', 'ambient_light', 'angle',
       'aperture', 'arc_angle', 'area_light', 'asc', 'asin', 'asinh', 'assumed_gamma',
       'atan', 'atan2', 'atanh', 'atmosphere', 'atmospheric_attenuation', 'attenuating',
       'average', 'background', 'black_hole', 'blue', 'blur_samples', 'bounded_by',
       'box_mapping', 'bozo', 'break', 'brick', 'brick_size', 'brightness', 'brilliance',
       'bumps', 'bumpy1', 'bumpy2', 'bumpy3', 'bump_map', 'bump_size', 'case', 'caustics',
       'ceil', 'checker', 'chr', 'clipped_by', 'clock', 'color', 'color_map', 'colour',
       'colour_map', 'component', 'composite', 'concat', 'confidence', 'conic_sweep',
       'constant', 'control0', 'control1', 'cos', 'cosh', 'count', 'crackle', 'crand',
       'cube', 'cubic_spline', 'cylindrical_mapping', 'debug', 'declare', 'default',
       'degrees', 'dents', 'diffuse', 'direction', 'distance', 'distance_maximum',
       'div', 'dust', 'dust_type', 'eccentricity', 'else', 'emitting', 'end', 'error',
       'error_bound', 'exp', 'exponent', 'fade_distance', 'fade_power', 'falloff',
       'falloff_angle', 'false', 'file_exists', 'filter', 'finish', 'fisheye', 'flatness',
       'flip', 'floor', 'focal_point', 'fog', 'fog_alt', 'fog_offset', 'fog_type',
       'frequency', 'gif', 'global_settings', 'glowing', 'gradient', 'granite', 'gray_threshold',
       'green', 'halo', 'hexagon', 'hf_gray_16', 'hierarchy', 'hollow', 'hypercomplex',
       'if', 'ifdef', 'iff', 'image_map', 'incidence', 'include', 'int', 'interpolate',
       'inverse', 'ior', 'irid', 'irid_wavelength', 'jitter', 'lambda', 'leopard',
       'linear', 'linear_spline', 'linear_sweep', 'location', 'log', 'looks_like',
       'look_at', 'low_error_factor', 'mandel', 'map_type', 'marble', 'material_map',
       'matrix', 'max', 'max_intersections', 'max_iteration', 'max_trace_level',
       'max_value', 'metallic', 'min', 'minimum_reuse', 'mod', 'mortar', 'nearest_count',
       'no', 'normal', 'normal_map', 'no_shadow', 'number_of_waves', 'octaves', 'off',
       'offset', 'omega', 'omnimax', 'on', 'once', 'onion', 'open', 'orthographic',
       'panoramic', 'pattern1', 'pattern2', 'pattern3', 'perspective', 'pgm', 'phase',
       'phong', 'phong_size', 'pi', 'pigment', 'pigment_map', 'planar_mapping', 'png',
       'point_at', 'pot', 'pow', 'ppm', 'precision', 'pwr', 'quadratic_spline', 'quaternion',
       'quick_color', 'quick_colour', 'quilted', 'radial', 'radians', 'radiosity',
       'radius', 'rainbow', 'ramp_wave', 'rand', 'range', 'reciprocal', 'recursion_limit',
       'red', 'reflection', 'refraction', 'render', 'repeat', 'rgb', 'rgbf', 'rgbft',
       'rgbt', 'right', 'ripples', 'rotate', 'roughness', 'samples', 'scale', 'scallop_wave',
       'scattering', 'seed', 'shadowless', 'sin', 'sine_wave', 'sinh', 'sky', 'sky_sphere',
       'slice', 'slope_map', 'smooth', 'specular', 'spherical_mapping', 'spiral',
       'spiral1', 'spiral2', 'spotlight', 'spotted', 'sqr', 'sqrt', 'statistics',
       'str', 'strcmp', 'strength', 'strlen', 'strlwr', 'strupr', 'sturm', 'substr',
       'switch', 'sys', 't', 'tan', 'tanh', 'test_camera_1', 'test_camera_2', 'test_camera_3',
       'test_camera_4', 'texture', 'texture_map', 'tga', 'thickness', 'threshold',
       'tightness', 'tile2', 'tiles', 'track', 'transform', 'translate', 'transmit',
       'triangle_wave', 'true', 'ttf', 'turbulence', 'turb_depth', 'type', 'ultra_wide_angle',
       'up', 'use_color', 'use_colour', 'use_index', 'u_steps', 'val', 'variance',
       'vaxis_rotate', 'vcross', 'vdot', 'version', 'vlength', 'vnormalize', 'volume_object',
       'volume_rendered', 'vol_with_light', 'vrotate', 'v_steps', 'warning', 'warp',
       'water_level', 'waves', 'while', 'width', 'wood', 'wrinkles', 'yes'),
                 prefix='\\b', suffix='\\b'),
               Keyword),
              (
               words(('bicubic_patch', 'blob', 'box', 'camera', 'cone', 'cubic', 'cylinder', 'difference',
       'disc', 'height_field', 'intersection', 'julia_fractal', 'lathe', 'light_source',
       'merge', 'mesh', 'object', 'plane', 'poly', 'polygon', 'prism', 'quadric',
       'quartic', 'smooth_triangle', 'sor', 'sphere', 'superellipsoid', 'text', 'torus',
       'triangle', 'union'),
                 suffix='\\b'),
               Name.Builtin),
              (
               '[\\[\\](){}<>;,]', Punctuation),
              (
               '[-+*/=]', Operator),
              (
               '\\b(x|y|z|u|v)\\b', Name.Builtin.Pseudo),
              (
               '[a-zA-Z_]\\w*', Name),
              (
               '[0-9]+\\.[0-9]*', Number.Float),
              (
               '\\.[0-9]+', Number.Float),
              (
               '[0-9]+', Number.Integer),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               '\\s+', Text)]}