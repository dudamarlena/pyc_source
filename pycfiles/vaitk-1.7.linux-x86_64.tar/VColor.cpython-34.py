# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/gui/VColor.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 22485 bytes


class VColor:

    def __init__(self, rgb):
        self._rgb = rgb

    @property
    def rgb(self):
        return self._rgb

    def hexString(self):
        return '%0.2X%0.2X%0.2X' % self.rgb

    @property
    def r(self):
        return self._rgb[0]

    @property
    def g(self):
        return self._rgb[1]

    @property
    def b(self):
        return self._rgb[2]

    @staticmethod
    def distance(color1, color2):
        return (color1.r - color2.r) ** 2 + (color1.g - color2.g) ** 2 + (color1.b - color2.b) ** 2

    class tuple:

        @staticmethod
        def distance(color1, color2):
            return (color1[0] - color2[0]) ** 2 + (color1[1] - color2[1]) ** 2 + (color1[2] - color2[2]) ** 2


class VGlobalColor:
    __doc__ = 'This class defines colors according to the rgb palette'
    term_0 = VColor(rgb=(0, 0, 0))
    term_1 = VColor(rgb=(128, 0, 0))
    term_2 = VColor(rgb=(0, 128, 0))
    term_3 = VColor(rgb=(128, 128, 0))
    term_4 = VColor(rgb=(0, 0, 128))
    term_5 = VColor(rgb=(128, 0, 128))
    term_6 = VColor(rgb=(0, 128, 128))
    term_7 = VColor(rgb=(192, 192, 192))
    term_8 = VColor(rgb=(128, 128, 128))
    term_9 = VColor(rgb=(255, 0, 0))
    term_10 = VColor(rgb=(0, 255, 0))
    term_11 = VColor(rgb=(255, 255, 0))
    term_12 = VColor(rgb=(0, 0, 255))
    term_13 = VColor(rgb=(255, 0, 255))
    term_14 = VColor(rgb=(0, 255, 255))
    term_15 = VColor(rgb=(255, 255, 255))
    term_16 = VColor(rgb=(0, 0, 0))
    term_17 = VColor(rgb=(0, 0, 95))
    term_18 = VColor(rgb=(0, 0, 135))
    term_19 = VColor(rgb=(0, 0, 175))
    term_20 = VColor(rgb=(0, 0, 215))
    term_21 = VColor(rgb=(0, 0, 255))
    term_22 = VColor(rgb=(0, 95, 0))
    term_23 = VColor(rgb=(0, 95, 95))
    term_24 = VColor(rgb=(0, 95, 135))
    term_25 = VColor(rgb=(0, 95, 175))
    term_26 = VColor(rgb=(0, 95, 215))
    term_27 = VColor(rgb=(0, 95, 255))
    term_28 = VColor(rgb=(0, 135, 0))
    term_29 = VColor(rgb=(0, 135, 95))
    term_30 = VColor(rgb=(0, 135, 135))
    term_31 = VColor(rgb=(0, 135, 175))
    term_32 = VColor(rgb=(0, 135, 215))
    term_33 = VColor(rgb=(0, 135, 255))
    term_34 = VColor(rgb=(0, 175, 0))
    term_35 = VColor(rgb=(0, 175, 95))
    term_36 = VColor(rgb=(0, 175, 135))
    term_37 = VColor(rgb=(0, 175, 175))
    term_38 = VColor(rgb=(0, 175, 215))
    term_39 = VColor(rgb=(0, 175, 255))
    term_40 = VColor(rgb=(0, 215, 0))
    term_41 = VColor(rgb=(0, 215, 95))
    term_42 = VColor(rgb=(0, 215, 135))
    term_43 = VColor(rgb=(0, 215, 175))
    term_44 = VColor(rgb=(0, 215, 215))
    term_45 = VColor(rgb=(0, 215, 255))
    term_46 = VColor(rgb=(0, 255, 0))
    term_47 = VColor(rgb=(0, 255, 95))
    term_48 = VColor(rgb=(0, 255, 135))
    term_49 = VColor(rgb=(0, 255, 175))
    term_50 = VColor(rgb=(0, 255, 215))
    term_51 = VColor(rgb=(0, 255, 255))
    term_52 = VColor(rgb=(95, 0, 0))
    term_53 = VColor(rgb=(95, 0, 95))
    term_54 = VColor(rgb=(95, 0, 135))
    term_55 = VColor(rgb=(95, 0, 175))
    term_56 = VColor(rgb=(95, 0, 215))
    term_57 = VColor(rgb=(95, 0, 255))
    term_58 = VColor(rgb=(95, 95, 0))
    term_59 = VColor(rgb=(95, 95, 95))
    term_60 = VColor(rgb=(95, 95, 135))
    term_61 = VColor(rgb=(95, 95, 175))
    term_62 = VColor(rgb=(95, 95, 215))
    term_63 = VColor(rgb=(95, 95, 255))
    term_64 = VColor(rgb=(95, 135, 0))
    term_65 = VColor(rgb=(95, 135, 95))
    term_66 = VColor(rgb=(95, 135, 135))
    term_67 = VColor(rgb=(95, 135, 175))
    term_68 = VColor(rgb=(95, 135, 215))
    term_69 = VColor(rgb=(95, 135, 255))
    term_70 = VColor(rgb=(95, 175, 0))
    term_71 = VColor(rgb=(95, 175, 95))
    term_72 = VColor(rgb=(95, 175, 135))
    term_73 = VColor(rgb=(95, 175, 175))
    term_74 = VColor(rgb=(95, 175, 215))
    term_75 = VColor(rgb=(95, 175, 255))
    term_76 = VColor(rgb=(95, 215, 0))
    term_77 = VColor(rgb=(95, 215, 95))
    term_78 = VColor(rgb=(95, 215, 135))
    term_79 = VColor(rgb=(95, 215, 175))
    term_80 = VColor(rgb=(95, 215, 215))
    term_81 = VColor(rgb=(95, 215, 255))
    term_82 = VColor(rgb=(95, 255, 0))
    term_83 = VColor(rgb=(95, 255, 95))
    term_84 = VColor(rgb=(95, 255, 135))
    term_85 = VColor(rgb=(95, 255, 175))
    term_86 = VColor(rgb=(95, 255, 215))
    term_87 = VColor(rgb=(95, 255, 255))
    term_88 = VColor(rgb=(135, 0, 0))
    term_89 = VColor(rgb=(135, 0, 95))
    term_90 = VColor(rgb=(135, 0, 135))
    term_91 = VColor(rgb=(135, 0, 175))
    term_92 = VColor(rgb=(135, 0, 215))
    term_93 = VColor(rgb=(135, 0, 255))
    term_94 = VColor(rgb=(135, 95, 0))
    term_95 = VColor(rgb=(135, 95, 95))
    term_96 = VColor(rgb=(135, 95, 135))
    term_97 = VColor(rgb=(135, 95, 175))
    term_98 = VColor(rgb=(135, 95, 215))
    term_99 = VColor(rgb=(135, 95, 255))
    term_100 = VColor(rgb=(135, 135, 0))
    term_101 = VColor(rgb=(135, 135, 95))
    term_102 = VColor(rgb=(135, 135, 135))
    term_103 = VColor(rgb=(135, 135, 175))
    term_104 = VColor(rgb=(135, 135, 215))
    term_105 = VColor(rgb=(135, 135, 255))
    term_106 = VColor(rgb=(135, 175, 0))
    term_107 = VColor(rgb=(135, 175, 95))
    term_108 = VColor(rgb=(135, 175, 135))
    term_109 = VColor(rgb=(135, 175, 175))
    term_110 = VColor(rgb=(135, 175, 215))
    term_111 = VColor(rgb=(135, 175, 255))
    term_112 = VColor(rgb=(135, 215, 0))
    term_113 = VColor(rgb=(135, 215, 95))
    term_114 = VColor(rgb=(135, 215, 135))
    term_115 = VColor(rgb=(135, 215, 175))
    term_116 = VColor(rgb=(135, 215, 215))
    term_117 = VColor(rgb=(135, 215, 255))
    term_118 = VColor(rgb=(135, 255, 0))
    term_119 = VColor(rgb=(135, 255, 95))
    term_120 = VColor(rgb=(135, 255, 135))
    term_121 = VColor(rgb=(135, 255, 175))
    term_122 = VColor(rgb=(135, 255, 215))
    term_123 = VColor(rgb=(135, 255, 255))
    term_124 = VColor(rgb=(175, 0, 0))
    term_125 = VColor(rgb=(175, 0, 95))
    term_126 = VColor(rgb=(175, 0, 135))
    term_127 = VColor(rgb=(175, 0, 175))
    term_128 = VColor(rgb=(175, 0, 215))
    term_129 = VColor(rgb=(175, 0, 255))
    term_130 = VColor(rgb=(175, 95, 0))
    term_131 = VColor(rgb=(175, 95, 95))
    term_132 = VColor(rgb=(175, 95, 135))
    term_133 = VColor(rgb=(175, 95, 175))
    term_134 = VColor(rgb=(175, 95, 215))
    term_135 = VColor(rgb=(175, 95, 255))
    term_136 = VColor(rgb=(175, 135, 0))
    term_137 = VColor(rgb=(175, 135, 95))
    term_138 = VColor(rgb=(175, 135, 135))
    term_139 = VColor(rgb=(175, 135, 175))
    term_140 = VColor(rgb=(175, 135, 215))
    term_141 = VColor(rgb=(175, 135, 255))
    term_142 = VColor(rgb=(175, 175, 0))
    term_143 = VColor(rgb=(175, 175, 95))
    term_144 = VColor(rgb=(175, 175, 135))
    term_145 = VColor(rgb=(175, 175, 175))
    term_146 = VColor(rgb=(175, 175, 215))
    term_147 = VColor(rgb=(175, 175, 255))
    term_148 = VColor(rgb=(175, 215, 0))
    term_149 = VColor(rgb=(175, 215, 95))
    term_150 = VColor(rgb=(175, 215, 135))
    term_151 = VColor(rgb=(175, 215, 175))
    term_152 = VColor(rgb=(175, 215, 215))
    term_153 = VColor(rgb=(175, 215, 255))
    term_154 = VColor(rgb=(175, 255, 0))
    term_155 = VColor(rgb=(175, 255, 95))
    term_156 = VColor(rgb=(175, 255, 135))
    term_157 = VColor(rgb=(175, 255, 175))
    term_158 = VColor(rgb=(175, 255, 215))
    term_159 = VColor(rgb=(175, 255, 255))
    term_160 = VColor(rgb=(215, 0, 0))
    term_161 = VColor(rgb=(215, 0, 95))
    term_162 = VColor(rgb=(215, 0, 135))
    term_163 = VColor(rgb=(215, 0, 175))
    term_164 = VColor(rgb=(215, 0, 215))
    term_165 = VColor(rgb=(215, 0, 255))
    term_166 = VColor(rgb=(215, 95, 0))
    term_167 = VColor(rgb=(215, 95, 95))
    term_168 = VColor(rgb=(215, 95, 135))
    term_169 = VColor(rgb=(215, 95, 175))
    term_170 = VColor(rgb=(215, 95, 215))
    term_171 = VColor(rgb=(215, 95, 255))
    term_172 = VColor(rgb=(215, 135, 0))
    term_173 = VColor(rgb=(215, 135, 95))
    term_174 = VColor(rgb=(215, 135, 135))
    term_175 = VColor(rgb=(215, 135, 175))
    term_176 = VColor(rgb=(215, 135, 215))
    term_177 = VColor(rgb=(215, 135, 255))
    term_178 = VColor(rgb=(215, 175, 0))
    term_179 = VColor(rgb=(215, 175, 95))
    term_180 = VColor(rgb=(215, 175, 135))
    term_181 = VColor(rgb=(215, 175, 175))
    term_182 = VColor(rgb=(215, 175, 215))
    term_183 = VColor(rgb=(215, 175, 255))
    term_184 = VColor(rgb=(215, 215, 0))
    term_185 = VColor(rgb=(215, 215, 95))
    term_186 = VColor(rgb=(215, 215, 135))
    term_187 = VColor(rgb=(215, 215, 175))
    term_188 = VColor(rgb=(215, 215, 215))
    term_189 = VColor(rgb=(215, 215, 255))
    term_190 = VColor(rgb=(215, 255, 0))
    term_191 = VColor(rgb=(215, 255, 95))
    term_192 = VColor(rgb=(215, 255, 135))
    term_193 = VColor(rgb=(215, 255, 175))
    term_194 = VColor(rgb=(215, 255, 215))
    term_195 = VColor(rgb=(215, 255, 255))
    term_196 = VColor(rgb=(255, 0, 0))
    term_197 = VColor(rgb=(255, 0, 95))
    term_198 = VColor(rgb=(255, 0, 135))
    term_199 = VColor(rgb=(255, 0, 175))
    term_200 = VColor(rgb=(255, 0, 215))
    term_201 = VColor(rgb=(255, 0, 255))
    term_202 = VColor(rgb=(255, 95, 0))
    term_203 = VColor(rgb=(255, 95, 95))
    term_204 = VColor(rgb=(255, 95, 135))
    term_205 = VColor(rgb=(255, 95, 175))
    term_206 = VColor(rgb=(255, 95, 215))
    term_207 = VColor(rgb=(255, 95, 255))
    term_208 = VColor(rgb=(255, 135, 0))
    term_209 = VColor(rgb=(255, 135, 95))
    term_210 = VColor(rgb=(255, 135, 135))
    term_211 = VColor(rgb=(255, 135, 175))
    term_212 = VColor(rgb=(255, 135, 215))
    term_213 = VColor(rgb=(255, 135, 255))
    term_214 = VColor(rgb=(255, 175, 0))
    term_215 = VColor(rgb=(255, 175, 95))
    term_216 = VColor(rgb=(255, 175, 135))
    term_217 = VColor(rgb=(255, 175, 175))
    term_218 = VColor(rgb=(255, 175, 215))
    term_219 = VColor(rgb=(255, 175, 255))
    term_220 = VColor(rgb=(255, 215, 0))
    term_221 = VColor(rgb=(255, 215, 95))
    term_222 = VColor(rgb=(255, 215, 135))
    term_223 = VColor(rgb=(255, 215, 175))
    term_224 = VColor(rgb=(255, 215, 215))
    term_225 = VColor(rgb=(255, 215, 255))
    term_226 = VColor(rgb=(255, 255, 0))
    term_227 = VColor(rgb=(255, 255, 95))
    term_228 = VColor(rgb=(255, 255, 135))
    term_229 = VColor(rgb=(255, 255, 175))
    term_230 = VColor(rgb=(255, 255, 215))
    term_231 = VColor(rgb=(255, 255, 255))
    term_232 = VColor(rgb=(8, 8, 8))
    term_233 = VColor(rgb=(18, 18, 18))
    term_234 = VColor(rgb=(28, 28, 28))
    term_235 = VColor(rgb=(38, 38, 38))
    term_236 = VColor(rgb=(48, 48, 48))
    term_237 = VColor(rgb=(58, 58, 58))
    term_238 = VColor(rgb=(68, 68, 68))
    term_239 = VColor(rgb=(78, 78, 78))
    term_240 = VColor(rgb=(88, 88, 88))
    term_241 = VColor(rgb=(96, 96, 96))
    term_242 = VColor(rgb=(102, 102, 102))
    term_243 = VColor(rgb=(118, 118, 118))
    term_244 = VColor(rgb=(128, 128, 128))
    term_245 = VColor(rgb=(138, 138, 138))
    term_246 = VColor(rgb=(148, 148, 148))
    term_247 = VColor(rgb=(158, 158, 158))
    term_248 = VColor(rgb=(168, 168, 168))
    term_249 = VColor(rgb=(178, 178, 178))
    term_250 = VColor(rgb=(188, 188, 188))
    term_251 = VColor(rgb=(198, 198, 198))
    term_252 = VColor(rgb=(208, 208, 208))
    term_253 = VColor(rgb=(218, 218, 218))
    term_254 = VColor(rgb=(228, 228, 228))
    term_255 = VColor(rgb=(238, 238, 238))
    term_000000 = term_0
    term_800000 = term_1
    term_008000 = term_2
    term_808000 = term_3
    term_000080 = term_4
    term_800080 = term_5
    term_008080 = term_6
    term_c0c0c0 = term_7
    term_808080 = term_8
    term_ff0000 = term_9
    term_00ff00 = term_10
    term_ffff00 = term_11
    term_0000ff = term_12
    term_ff00ff = term_13
    term_00ffff = term_14
    term_ffffff = term_15
    term_000000 = term_16
    term_00005f = term_17
    term_000087 = term_18
    term_0000af = term_19
    term_0000d7 = term_20
    term_0000ff = term_21
    term_005f00 = term_22
    term_005f5f = term_23
    term_005f87 = term_24
    term_005faf = term_25
    term_005fd7 = term_26
    term_005fff = term_27
    term_008700 = term_28
    term_00875f = term_29
    term_008787 = term_30
    term_0087af = term_31
    term_0087d7 = term_32
    term_0087ff = term_33
    term_00af00 = term_34
    term_00af5f = term_35
    term_00af87 = term_36
    term_00afaf = term_37
    term_00afd7 = term_38
    term_00afff = term_39
    term_00d700 = term_40
    term_00d75f = term_41
    term_00d787 = term_42
    term_00d7af = term_43
    term_00d7d7 = term_44
    term_00d7ff = term_45
    term_00ff00 = term_46
    term_00ff5f = term_47
    term_00ff87 = term_48
    term_00ffaf = term_49
    term_00ffd7 = term_50
    term_00ffff = term_51
    term_5f0000 = term_52
    term_5f005f = term_53
    term_5f0087 = term_54
    term_5f00af = term_55
    term_5f00d7 = term_56
    term_5f00ff = term_57
    term_5f5f00 = term_58
    term_5f5f5f = term_59
    term_5f5f87 = term_60
    term_5f5faf = term_61
    term_5f5fd7 = term_62
    term_5f5fff = term_63
    term_5f8700 = term_64
    term_5f875f = term_65
    term_5f8787 = term_66
    term_5f87af = term_67
    term_5f87d7 = term_68
    term_5f87ff = term_69
    term_5faf00 = term_70
    term_5faf5f = term_71
    term_5faf87 = term_72
    term_5fafaf = term_73
    term_5fafd7 = term_74
    term_5fafff = term_75
    term_5fd700 = term_76
    term_5fd75f = term_77
    term_5fd787 = term_78
    term_5fd7af = term_79
    term_5fd7d7 = term_80
    term_5fd7ff = term_81
    term_5fff00 = term_82
    term_5fff5f = term_83
    term_5fff87 = term_84
    term_5fffaf = term_85
    term_5fffd7 = term_86
    term_5fffff = term_87
    term_870000 = term_88
    term_87005f = term_89
    term_870087 = term_90
    term_8700af = term_91
    term_8700d7 = term_92
    term_8700ff = term_93
    term_875f00 = term_94
    term_875f5f = term_95
    term_875f87 = term_96
    term_875faf = term_97
    term_875fd7 = term_98
    term_875fff = term_99
    term_878700 = term_100
    term_87875f = term_101
    term_878787 = term_102
    term_8787af = term_103
    term_8787d7 = term_104
    term_8787ff = term_105
    term_87af00 = term_106
    term_87af5f = term_107
    term_87af87 = term_108
    term_87afaf = term_109
    term_87afd7 = term_110
    term_87afff = term_111
    term_87d700 = term_112
    term_87d75f = term_113
    term_87d787 = term_114
    term_87d7af = term_115
    term_87d7d7 = term_116
    term_87d7ff = term_117
    term_87ff00 = term_118
    term_87ff5f = term_119
    term_87ff87 = term_120
    term_87ffaf = term_121
    term_87ffd7 = term_122
    term_87ffff = term_123
    term_af0000 = term_124
    term_af005f = term_125
    term_af0087 = term_126
    term_af00af = term_127
    term_af00d7 = term_128
    term_af00ff = term_129
    term_af5f00 = term_130
    term_af5f5f = term_131
    term_af5f87 = term_132
    term_af5faf = term_133
    term_af5fd7 = term_134
    term_af5fff = term_135
    term_af8700 = term_136
    term_af875f = term_137
    term_af8787 = term_138
    term_af87af = term_139
    term_af87d7 = term_140
    term_af87ff = term_141
    term_afaf00 = term_142
    term_afaf5f = term_143
    term_afaf87 = term_144
    term_afafaf = term_145
    term_afafd7 = term_146
    term_afafff = term_147
    term_afd700 = term_148
    term_afd75f = term_149
    term_afd787 = term_150
    term_afd7af = term_151
    term_afd7d7 = term_152
    term_afd7ff = term_153
    term_afff00 = term_154
    term_afff5f = term_155
    term_afff87 = term_156
    term_afffaf = term_157
    term_afffd7 = term_158
    term_afffff = term_159
    term_d70000 = term_160
    term_d7005f = term_161
    term_d70087 = term_162
    term_d700af = term_163
    term_d700d7 = term_164
    term_d700ff = term_165
    term_d75f00 = term_166
    term_d75f5f = term_167
    term_d75f87 = term_168
    term_d75faf = term_169
    term_d75fd7 = term_170
    term_d75fff = term_171
    term_d78700 = term_172
    term_d7875f = term_173
    term_d78787 = term_174
    term_d787af = term_175
    term_d787d7 = term_176
    term_d787ff = term_177
    term_d7af00 = term_178
    term_d7af5f = term_179
    term_d7af87 = term_180
    term_d7afaf = term_181
    term_d7afd7 = term_182
    term_d7afff = term_183
    term_d7d700 = term_184
    term_d7d75f = term_185
    term_d7d787 = term_186
    term_d7d7af = term_187
    term_d7d7d7 = term_188
    term_d7d7ff = term_189
    term_d7ff00 = term_190
    term_d7ff5f = term_191
    term_d7ff87 = term_192
    term_d7ffaf = term_193
    term_d7ffd7 = term_194
    term_d7ffff = term_195
    term_ff0000 = term_196
    term_ff005f = term_197
    term_ff0087 = term_198
    term_ff00af = term_199
    term_ff00d7 = term_200
    term_ff00ff = term_201
    term_ff5f00 = term_202
    term_ff5f5f = term_203
    term_ff5f87 = term_204
    term_ff5faf = term_205
    term_ff5fd7 = term_206
    term_ff5fff = term_207
    term_ff8700 = term_208
    term_ff875f = term_209
    term_ff8787 = term_210
    term_ff87af = term_211
    term_ff87d7 = term_212
    term_ff87ff = term_213
    term_ffaf00 = term_214
    term_ffaf5f = term_215
    term_ffaf87 = term_216
    term_ffafaf = term_217
    term_ffafd7 = term_218
    term_ffafff = term_219
    term_ffd700 = term_220
    term_ffd75f = term_221
    term_ffd787 = term_222
    term_ffd7af = term_223
    term_ffd7d7 = term_224
    term_ffd7ff = term_225
    term_ffff00 = term_226
    term_ffff5f = term_227
    term_ffff87 = term_228
    term_ffffaf = term_229
    term_ffffd7 = term_230
    term_ffffff = term_231
    term_080808 = term_232
    term_121212 = term_233
    term_1c1c1c = term_234
    term_262626 = term_235
    term_303030 = term_236
    term_3a3a3a = term_237
    term_444444 = term_238
    term_4e4e4e = term_239
    term_585858 = term_240
    term_606060 = term_241
    term_666666 = term_242
    term_767676 = term_243
    term_808080 = term_244
    term_8a8a8a = term_245
    term_949494 = term_246
    term_9e9e9e = term_247
    term_a8a8a8 = term_248
    term_b2b2b2 = term_249
    term_bcbcbc = term_250
    term_c6c6c6 = term_251
    term_d0d0d0 = term_252
    term_dadada = term_253
    term_e4e4e4 = term_254
    term_eeeeee = term_255
    transparent = None
    black = term_0
    red = term_1
    green = term_2
    brown = term_3
    blue = term_4
    magenta = term_5
    cyan = term_6
    white = term_7
    grey = term_8
    lightred = term_9
    lightgreen = term_10
    yellow = term_11
    lightblue = term_12
    lightmagenta = term_13
    lightcyan = term_14
    white = term_15
    pink = term_ff8787
    darkred = term_5f0000
    darkgreen = term_005f00
    darkblue = term_00005f
    darkmagenta = term_5f005f
    darkcyan = term_005f5f

    @staticmethod
    def nameToColor(name):
        """Perform lookup of the color by string. Returns None if the lookup fails."""
        return VGlobalColor.__dict__.get(name)