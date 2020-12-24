# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\toolboxes\rgb2spec\smits_mitsuba.py
# Compiled at: 2019-07-10 05:18:11
# Size of source mod 2**32: 26787 bytes
"""
Module for Smits-style RGB to Spectrum conversion

based on https://github.com/mitsuba-renderer/mitsuba/blob/1fd0f671dfcb77f813c0d6a36f2aa4e480b5ca8e/src/libcore/spectrum.cpp
.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import np, cie_interp, getwlr, _WL3
import copy
__all__ = [
 'rgb2spec_entries', 'rgb_to_spec_smits']
RGB2Spec_wavelengths = np.array([380.0, 390.967743, 401.935486, 412.903229, 423.870972, 434.838715,
 445.806458, 456.7742, 467.741943, 478.709686, 489.677429, 500.645172,
 511.612915, 522.580627, 533.54834, 544.516052, 555.483765, 566.451477,
 577.419189, 588.386902, 599.354614, 610.322327, 621.290039, 632.257751,
 643.225464, 654.193176, 665.160889, 676.128601, 687.096313, 698.064026,
 709.031738, 720.0])
RGBRefl2SpecWhite_entries = np.array([1.0618958571272863, 1.0615019980348779,
 1.0614335379927147, 1.0622711654692485,
 1.0622036218416742, 1.0625059965187085,
 1.0623938486985884, 1.0624706448043137,
 1.0625048144827762, 1.0624366131308856,
 1.0620694238892607, 1.0613167586932164,
 1.061033402937702, 1.0613868564828413,
 1.0614215366116762, 1.0620336151299086,
 1.062549745480505, 1.0624317487992085,
 1.062524914055448, 1.0624277664486914,
 1.062474985409077, 1.0625538581025402,
 1.0625326910104864, 1.0623922312225325,
 1.062365098035413, 1.0625256476715284,
 1.0612277619533155, 1.0594262608698046,
 1.0599810758292072, 1.0602547314449409,
 1.0601263046243634, 1.0606565756823634])
RGBRefl2SpecCyan_entries = np.array([1.041462802142675, 1.0328661533771188,
 1.0126146228964314, 1.035046052483621,
 1.0078661447098567, 1.042228038508128,
 1.0442596738499825, 1.0535238290294409,
 1.018077622693812, 1.0442729908727713,
 1.052936254192075, 1.0537034271160244,
 1.053390186921597, 1.0537782700979574,
 1.0527093770467102, 1.0530449040446797,
 1.0550554640191208, 1.055367361072482,
 1.0454306634683976, 0.623489506392308,
 0.18038071613188977, -0.007630375920198454,
 -0.00015217847035781367, -0.007510225734725831,
 -0.002170863932849147, 0.0006591946660236964,
 0.01227881531853978, -0.004466977563720803,
 0.017119799082865147, 0.00492110897597598,
 0.0058762925143334985, 0.02525939941555008])
RGBRefl2SpecMagenta_entries = np.array([0.9942213815123685, 0.9898693712297568,
 0.9829365828611696, 0.9962786839985931,
 1.0198955019000133, 1.016639550121036,
 1.0220913178757398, 0.9965166604068244,
 1.0097766178917882, 1.0215422470827016,
 0.6403195338779096, 0.0025012379477078184,
 0.006533993955576994, 0.0028334080462675826,
 -5.1209675389074505e-11, -0.009059229164664638,
 0.00339367183233312, -0.0030638741121828406,
 0.22203936168286292, 0.6314114002481197,
 0.9748098557650096, 0.9720956233359057,
 1.017377030286815, 0.9987519432273413,
 0.9470172573960224, 0.852586231543548,
 0.9489779858166084, 0.9475187609652149,
 0.9959894419105979, 0.8630135150380908,
 0.8915098785352314, 0.8486649265284508])
RGBRefl2SpecYellow_entries = np.array([0.005574062292492087, -0.004798283163144679,
 -0.00525365642986138, -0.006457148004449971,
 -0.005969351465800701, -0.002183671603768672,
 0.016781120601055327, 0.09609635542906264,
 0.21217357081986446, 0.3616913329068507,
 0.5396101154323253, 0.7440881049217151,
 0.9220957114839405, 1.0460304298411225,
 1.0513824989063714, 1.0511991822135085,
 1.0510530911991052, 1.051739723036051,
 1.0516043086790485, 1.051194403206146,
 1.0511590325868068, 1.051661246548303,
 1.0514038526836869, 1.0515941029228475,
 1.051146043696084, 1.0515123758830476,
 1.0508871369510702, 1.050892370810238,
 1.0477492815668303, 1.0493272144017338,
 1.0435963333422726, 1.0392280772051465])
RGBRefl2SpecRed_entries = np.array([0.1657560486708618, 0.11846442802747797,
 0.12408293329637447, 0.11371272058349924,
 0.07899243451889913, 0.03220560359310655,
 -0.010798365407877875, 0.018051975516730392,
 0.005340719659873053, 0.013654918729501336,
 -0.005956421354564284, -0.0018444365067353252,
 -0.010571884361529504, -0.002937552107800001,
 -0.010790476271835936, -0.008022430669750363,
 -0.002266916770249594, 0.007020024049470663,
 -0.00815284690002993, 0.6077286696925279,
 0.988315608654324, 0.9939169104407882,
 1.0039338994753197, 0.9923449986116712,
 0.9992653085885552, 1.008462155761727,
 0.9835829682744122, 1.0085023660099048,
 0.974511383265687, 0.9854326957005994,
 0.9349576398096204, 0.987139077923194])
RGBRefl2SpecGreen_entries = np.array([0.0026494153587602255, -0.005017501342973224,
 -0.012547236272489583, -0.009455496430838867,
 -0.012526086181600525, -0.007917069776043777,
 -0.007995573520417569, -0.009355943344446907,
 0.0654686119829993, 0.3957287551763414,
 0.7524402229988666, 0.9637647869021856,
 0.9985443385516233, 0.9999297702528792,
 0.9993908675114045, 0.999943722670714,
 0.9993912181341867, 0.9991123731042448,
 0.9601958487827158, 0.6318627933843244,
 0.2579740102876347, 0.009401488852733564,
 -0.0030798345608649747, -0.0045230367033685034,
 -0.006893341038827404, -0.00903521955390154,
 -0.008591366716534021, -0.00836908691202894,
 -0.007868583233875431, -8.365757871108513e-06,
 0.005430122544281718, -0.0027745589759259194])
RGBRefl2SpecBlue_entries = np.array([0.9920977146972068, 0.9887642605936913,
 0.9953904074450564, 0.9952931735300822,
 0.9918144741163395, 1.0002584039673432,
 0.9996847843734251, 0.9998812076665717,
 0.9850401214637043, 0.7902984905303128,
 0.5608219861746397, 0.3313345851399653,
 0.13692410840839175, 0.01891490655966415,
 -5.112977093255089e-06, -0.00042395493167891873,
 -0.00041934593101534273, 0.0017473028136486615,
 0.0037999160177631316, -0.0005510147490658864,
 -4.3716662898480967e-05, 0.00758745017487328,
 0.02579565078055402, 0.03816837653250055,
 0.04948958640803083, 0.049595992290102905,
 0.04981481950581225, 0.03984091106497802,
 0.03050102493723387, 0.02124305476524108,
 0.00695965321043564, 0.0041733649330980525])
RGBIllum2SpecWhite_entries = np.array([1.1565232050369776, 1.156722500011914,
 1.1566203150243823, 1.1555782088080084,
 1.15621755092157, 1.1567674012207332,
 1.156802319480863, 1.156767744548552,
 1.156356318295283, 1.1567054702510189,
 1.1565134139372772, 1.1564336176499312,
 1.1568023181530034, 1.1473147688514642,
 1.1339317140561065, 1.1293876490671435,
 1.1290515328639648, 1.0504864823782283,
 1.0459696042230884, 0.9936668716859569,
 0.9560166926539394, 0.924674820335118,
 0.9149994470205176, 0.8993946765845346,
 0.8954252075133111, 0.8887056669381475,
 0.8822284381422811, 0.8799831137382668,
 0.8763524461224458, 0.8800036833170911,
 0.8806566542844112, 0.883047064602769])
RGBIllum2SpecCyan_entries = np.array([1.1334479663682135, 1.1266762330194116,
 1.1346827504710164, 1.1357395805744794,
 1.1356371830149636, 1.1361152989346193,
 1.1362179057706772, 1.1364819652587022,
 1.1355107110714324, 1.1364060941199556,
 1.1360363621722465, 1.1360122641141395,
 1.135426688246703, 1.1363099407179136,
 1.1355450412632506, 1.1353732327376378,
 1.1349496420726002, 1.1111113947168556,
 0.9059874042972714, 0.6116078078746533,
 0.29539752170999634, 0.0959542006711501,
 -0.011650792030826267, -0.012144633073395025,
 -0.011148167569748318, -0.011997606668458151,
 -0.005050685547539485, -0.007998274581954215,
 -0.009472281770823642, -0.0055329541006658815,
 -0.004542891402827449, -0.012541015360921132])
RGBIllum2SpecMagenta_entries = np.array([1.0371892935878366, 1.0587542891035364,
 1.0767271213688903, 1.0762706844110288,
 1.0795289105258212, 1.0743644742950074,
 1.0727028691194342, 1.0732447452056488,
 1.0823760816041414, 1.0840545681409282,
 0.9560756752630666, 0.5519789685506467,
 0.08419109488724758, 8.7940070557041e-05,
 -0.002308640833507125, -0.0011248136628651192,
 -7.729761275498959e-11, -0.00027270769006770834,
 0.014466473094035592, 0.2588311602716948,
 0.5290799982756673, 0.9096662409710516,
 1.0690571327307956, 1.0887326064796272,
 1.0637622289511852, 1.020181291809426,
 1.0262196688979945, 1.078308556061319,
 0.9833384962321887, 1.070724634280262,
 1.0634247770423768, 1.0150875475729566])
RGBIllum2SpecYellow_entries = np.array([0.002775695896581197, 0.003967382099064661,
 -0.0001460693678860675, 0.00036198394557748065,
 -0.00025819258699309733, -5.0133191628082274e-05,
 -0.00024437242866157116, -7.806141994803895e-05,
 0.04969030120754092, 0.48515973574763166,
 1.029572585436059, 1.0333210878457741,
 1.0368102644026933, 1.0364884018886333,
 1.0365427939411784, 1.036859540285454,
 1.0365645405660555, 1.0363938240707142,
 1.0367205578770746, 1.036523932944605,
 1.0361531226427443, 1.0348785007827348,
 1.0042729660717318, 0.8421848643235428,
 0.7375939489480157, 0.6585315450029464,
 0.6053168244406628, 0.5954979413242074,
 0.5941926127844314, 0.5651768232663427,
 0.5606118601496856, 0.5822861038101872])
RGBIllum2SpecRed_entries = np.array([0.05471118715729184, 0.0556090664983034,
 0.060755873790918236, 0.05623294861596237,
 0.04616994053570868, 0.038012808167818095,
 0.02442422575667034, 0.003898358058159218,
 -0.0005608225217273444, 0.0009649387125519465,
 0.0003734119805151037, -0.000433673890931352,
 -9.353396225689203e-05, -0.00012354967412842033,
 -0.0001452454808168746, -0.0002004769191554373,
 -0.0004993858769469367, 0.027255083540032476,
 0.1606740590629706, 0.35069788873150953,
 0.5735746553841896, 0.7639209189071895,
 0.8914446674038152, 0.9639460990957489,
 0.9887946427601628, 0.998974499662272,
 0.9860514040356416, 0.995325028053452,
 0.9743347837730537, 0.9913436461687141,
 0.9886628777217475, 0.9971385608973553])
RGBIllum2SpecGreen_entries = np.array([0.02516838875551463, 0.03942743816942372,
 0.006205957159642579, 0.007112085980742955,
 0.0002176004464913943, 7.327183998429021e-12,
 -0.0216230662171817, 0.015670209409407512,
 0.002801960318863622, 0.32494773799897647,
 1.0164917292316602, 1.0329476657890369,
 1.032158696299155, 1.0358667411948619,
 1.015123547683494, 1.0338076690093119,
 1.0371372378155013, 1.0361377027692558,
 1.022982243255721, 0.9691032733565232,
 -0.005178592389987857, 0.001113126197106143,
 0.006667550303301177, 0.0007402431568600196,
 0.021591567633473925, 0.005148162005621723,
 0.0014561928645728216, 0.00016414511045291513,
 -0.006463076496845329, 0.010250854718507939,
 0.042387394733956134, 0.02125271692686162])
RGBIllum2SpecBlue_entries = np.array([1.0570490759328752, 1.05384669128513,
 1.055049425814067, 1.0530407754701832,
 1.0579930596460185, 1.057843949481237,
 1.0583132387180239, 1.0579712943137616,
 1.0561884233578465, 1.057139928542649,
 1.0425795187752152, 0.326030843740561,
 -0.0019255628442412243, -0.0012959221137046478,
 -0.0014357356276938696, -0.0012963697250337886,
 -0.00192270811623739, 0.0012621152526221778,
 -0.0016095249003578276, -0.0013029983817879568,
 -0.0017666600873954916, -0.001232528114028005,
 0.010316809673254932, 0.03128451264835436,
 0.08877387988174648, 0.1387362174023654,
 0.15535067531939065, 0.1487847717823703,
 0.16624255403475907, 0.16997613960634927,
 0.15769743995852967, 0.19069090525482305])
rgb2spec_entries = {'wlr':RGB2Spec_wavelengths, 
 'rfl':{'white':RGBRefl2SpecWhite_entries, 
  'cyan':RGBRefl2SpecCyan_entries, 
  'magenta':RGBRefl2SpecMagenta_entries, 
  'yellow':RGBRefl2SpecYellow_entries, 
  'blue':RGBRefl2SpecBlue_entries, 
  'green':RGBRefl2SpecGreen_entries, 
  'red':RGBRefl2SpecRed_entries, 
  'scalefactor':0.94}, 
 'spd':{'white':RGBIllum2SpecWhite_entries, 
  'cyan':RGBIllum2SpecCyan_entries, 
  'magenta':RGBIllum2SpecMagenta_entries, 
  'yellow':RGBIllum2SpecYellow_entries, 
  'blue':RGBIllum2SpecBlue_entries, 
  'green':RGBIllum2SpecGreen_entries, 
  'red':RGBIllum2SpecRed_entries, 
  'scalefactor':0.86445}}

def _addwlr(x):
    return np.vstack((rgb2spec_entries['wlr'], x))


def _convert_to_wlr(entries=rgb2spec_entries, wlr=_WL3):
    wlr = getwlr(wlr)
    for entry in entries:
        if entry != 'wlr':
            for k, v in entries[entry].items():
                if k != 'scalefactor':
                    entries[entry][k] = cie_interp((_addwlr(entries[entry][k])), wlr, kind=entry)[1]

    entries['wlr'] = wlr
    return entries


rgb2spec_entries = _convert_to_wlr()
_BASESPEC_SMITS = copy.deepcopy(rgb2spec_entries)

def _fromLinearRGB--- This code section failed: ---

 L. 319         0  LOAD_FAST                'rgb'
                2  UNPACK_SEQUENCE_3     3 
                4  STORE_FAST               'r'
                6  STORE_FAST               'g'
                8  STORE_FAST               'b'

 L. 320        10  LOAD_GLOBAL              np
               12  LOAD_METHOD              zeros
               14  LOAD_FAST                'rgb2spec'
               16  LOAD_STR                 'wlr'
               18  BINARY_SUBSCR    
               20  LOAD_ATTR                shape
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  BUILD_TUPLE_1         1 
               28  CALL_METHOD_1         1  '1 positional argument'
               30  STORE_FAST               'result'

 L. 322        32  LOAD_FAST                'r'
               34  LOAD_FAST                'g'
               36  COMPARE_OP               <=
               38  LOAD_FAST                'r'
               40  LOAD_FAST                'b'
               42  COMPARE_OP               <=
               44  BINARY_AND       
               46  POP_JUMP_IF_FALSE   178  'to 178'

 L. 324        48  LOAD_FAST                'result'
               50  LOAD_FAST                'r'
               52  LOAD_FAST                'rgb2spec'
               54  LOAD_FAST                'intent'
               56  BINARY_SUBSCR    
               58  LOAD_STR                 'white'
               60  BINARY_SUBSCR    
               62  BINARY_MULTIPLY  
               64  INPLACE_ADD      
               66  STORE_FAST               'result'

 L. 325        68  LOAD_FAST                'g'
               70  LOAD_FAST                'b'
               72  COMPARE_OP               <=
               74  POP_JUMP_IF_FALSE   126  'to 126'

 L. 326        76  LOAD_FAST                'result'
               78  LOAD_FAST                'g'
               80  LOAD_FAST                'r'
               82  BINARY_SUBTRACT  
               84  LOAD_FAST                'rgb2spec'
               86  LOAD_FAST                'intent'
               88  BINARY_SUBSCR    
               90  LOAD_STR                 'cyan'
               92  BINARY_SUBSCR    
               94  BINARY_MULTIPLY  
               96  INPLACE_ADD      
               98  STORE_FAST               'result'

 L. 327       100  LOAD_FAST                'result'
              102  LOAD_FAST                'b'
              104  LOAD_FAST                'g'
              106  BINARY_SUBTRACT  
              108  LOAD_FAST                'rgb2spec'
              110  LOAD_FAST                'intent'
              112  BINARY_SUBSCR    
              114  LOAD_STR                 'blue'
              116  BINARY_SUBSCR    
              118  BINARY_MULTIPLY  
              120  INPLACE_ADD      
              122  STORE_FAST               'result'
              124  JUMP_FORWARD        454  'to 454'
            126_0  COME_FROM            74  '74'

 L. 329       126  LOAD_FAST                'result'
              128  LOAD_FAST                'b'
              130  LOAD_FAST                'r'
              132  BINARY_SUBTRACT  
              134  LOAD_FAST                'rgb2spec'
              136  LOAD_FAST                'intent'
              138  BINARY_SUBSCR    
              140  LOAD_STR                 'cyan'
              142  BINARY_SUBSCR    
              144  BINARY_MULTIPLY  
              146  INPLACE_ADD      
              148  STORE_FAST               'result'

 L. 330       150  LOAD_FAST                'result'
              152  LOAD_FAST                'g'
              154  LOAD_FAST                'b'
              156  BINARY_SUBTRACT  
              158  LOAD_FAST                'rgb2spec'
              160  LOAD_FAST                'intent'
              162  BINARY_SUBSCR    
              164  LOAD_STR                 'green'
              166  BINARY_SUBSCR    
              168  BINARY_MULTIPLY  
              170  INPLACE_ADD      
              172  STORE_FAST               'result'
          174_176  JUMP_FORWARD        454  'to 454'
            178_0  COME_FROM            46  '46'

 L. 332       178  LOAD_FAST                'g'
              180  LOAD_FAST                'r'
              182  COMPARE_OP               <=
              184  LOAD_FAST                'g'
              186  LOAD_FAST                'b'
              188  COMPARE_OP               <=
              190  BINARY_AND       
          192_194  POP_JUMP_IF_FALSE   326  'to 326'

 L. 334       196  LOAD_FAST                'result'
              198  LOAD_FAST                'g'
              200  LOAD_FAST                'rgb2spec'
              202  LOAD_FAST                'intent'
              204  BINARY_SUBSCR    
              206  LOAD_STR                 'white'
              208  BINARY_SUBSCR    
              210  BINARY_MULTIPLY  
              212  INPLACE_ADD      
              214  STORE_FAST               'result'

 L. 335       216  LOAD_FAST                'r'
              218  LOAD_FAST                'b'
              220  COMPARE_OP               <=
          222_224  POP_JUMP_IF_FALSE   276  'to 276'

 L. 336       226  LOAD_FAST                'result'
              228  LOAD_FAST                'r'
              230  LOAD_FAST                'g'
              232  BINARY_SUBTRACT  
              234  LOAD_FAST                'rgb2spec'
              236  LOAD_FAST                'intent'
              238  BINARY_SUBSCR    
              240  LOAD_STR                 'magenta'
              242  BINARY_SUBSCR    
              244  BINARY_MULTIPLY  
              246  INPLACE_ADD      
              248  STORE_FAST               'result'

 L. 337       250  LOAD_FAST                'result'
              252  LOAD_FAST                'b'
              254  LOAD_FAST                'r'
              256  BINARY_SUBTRACT  
              258  LOAD_FAST                'rgb2spec'
              260  LOAD_FAST                'intent'
              262  BINARY_SUBSCR    
              264  LOAD_STR                 'blue'
              266  BINARY_SUBSCR    
              268  BINARY_MULTIPLY  
              270  INPLACE_ADD      
              272  STORE_FAST               'result'
              274  JUMP_FORWARD        324  'to 324'
            276_0  COME_FROM           222  '222'

 L. 339       276  LOAD_FAST                'result'
              278  LOAD_FAST                'b'
              280  LOAD_FAST                'g'
              282  BINARY_SUBTRACT  
              284  LOAD_FAST                'rgb2spec'
              286  LOAD_FAST                'intent'
              288  BINARY_SUBSCR    
              290  LOAD_STR                 'magenta'
              292  BINARY_SUBSCR    
              294  BINARY_MULTIPLY  
              296  INPLACE_ADD      
              298  STORE_FAST               'result'

 L. 340       300  LOAD_FAST                'result'
              302  LOAD_FAST                'r'
              304  LOAD_FAST                'b'
              306  BINARY_SUBTRACT  
              308  LOAD_FAST                'rgb2spec'
              310  LOAD_FAST                'intent'
              312  BINARY_SUBSCR    
              314  LOAD_STR                 'red'
              316  BINARY_SUBSCR    
              318  BINARY_MULTIPLY  
              320  INPLACE_ADD      
              322  STORE_FAST               'result'
            324_0  COME_FROM           274  '274'
              324  JUMP_FORWARD        454  'to 454'
            326_0  COME_FROM           192  '192'

 L. 344       326  LOAD_FAST                'result'
              328  LOAD_FAST                'b'
              330  LOAD_FAST                'rgb2spec'
              332  LOAD_FAST                'intent'
              334  BINARY_SUBSCR    
              336  LOAD_STR                 'white'
              338  BINARY_SUBSCR    
              340  BINARY_MULTIPLY  
              342  INPLACE_ADD      
              344  STORE_FAST               'result'

 L. 345       346  LOAD_FAST                'r'
              348  LOAD_FAST                'g'
              350  COMPARE_OP               <=
          352_354  POP_JUMP_IF_FALSE   406  'to 406'

 L. 346       356  LOAD_FAST                'result'
              358  LOAD_FAST                'r'
              360  LOAD_FAST                'b'
              362  BINARY_SUBTRACT  
              364  LOAD_FAST                'rgb2spec'
              366  LOAD_FAST                'intent'
              368  BINARY_SUBSCR    
              370  LOAD_STR                 'yellow'
              372  BINARY_SUBSCR    
              374  BINARY_MULTIPLY  
              376  INPLACE_ADD      
              378  STORE_FAST               'result'

 L. 347       380  LOAD_FAST                'result'
              382  LOAD_FAST                'g'
              384  LOAD_FAST                'r'
              386  BINARY_SUBTRACT  
              388  LOAD_FAST                'rgb2spec'
              390  LOAD_FAST                'intent'
              392  BINARY_SUBSCR    
              394  LOAD_STR                 'green'
              396  BINARY_SUBSCR    
              398  BINARY_MULTIPLY  
              400  INPLACE_ADD      
            402_0  COME_FROM           124  '124'
              402  STORE_FAST               'result'
              404  JUMP_FORWARD        454  'to 454'
            406_0  COME_FROM           352  '352'

 L. 349       406  LOAD_FAST                'result'
              408  LOAD_FAST                'g'
              410  LOAD_FAST                'b'
              412  BINARY_SUBTRACT  
              414  LOAD_FAST                'rgb2spec'
              416  LOAD_FAST                'intent'
              418  BINARY_SUBSCR    
              420  LOAD_STR                 'yellow'
              422  BINARY_SUBSCR    
              424  BINARY_MULTIPLY  
              426  INPLACE_ADD      
              428  STORE_FAST               'result'

 L. 350       430  LOAD_FAST                'result'
              432  LOAD_FAST                'r'
              434  LOAD_FAST                'g'
              436  BINARY_SUBTRACT  
              438  LOAD_FAST                'rgb2spec'
              440  LOAD_FAST                'intent'
              442  BINARY_SUBSCR    
              444  LOAD_STR                 'red'
              446  BINARY_SUBSCR    
              448  BINARY_MULTIPLY  
              450  INPLACE_ADD      
              452  STORE_FAST               'result'
            454_0  COME_FROM           404  '404'
            454_1  COME_FROM           324  '324'
            454_2  COME_FROM           174  '174'

 L. 351       454  LOAD_FAST                'result'
              456  LOAD_FAST                'rgb2spec'
              458  LOAD_FAST                'intent'
              460  BINARY_SUBSCR    
              462  LOAD_STR                 'scalefactor'
              464  BINARY_SUBSCR    
              466  INPLACE_MULTIPLY 
              468  STORE_FAST               'result'

 L. 353       470  LOAD_GLOBAL              np
              472  LOAD_METHOD              clip
              474  LOAD_FAST                'result'
              476  LOAD_CONST               0
              478  LOAD_CONST               None
              480  CALL_METHOD_3         3  '3 positional arguments'
              482  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 402_0


def rgb_to_spec_smits(rgb, intent='rfl', bitdepth=8, wlr=_WL3, rgb2spec=None):
    """
    Convert an array of RGB values to a spectrum using a Smits like conversion as implemented in Mitsuba.
    
    Args:
        :rgb: 
            | ndarray of list of rgb values
        :intent:
            | 'rfl' (or 'spd'), optional
            | type of requested spectrum conversion .
        :bitdepth:
            | 8, optional
            | bit depth of rgb values
        :wlr: 
            | _WL3, optional
            | desired wavelength (nm) range of spectrum.
        :rgb2spec:
            | None, optional
            | Dict with base spectra for white, cyan, magenta, yellow, blue, green and red for each intent.
            | If None: use _BASESPEC_SMITS.
        
    Returns:
        :spec: 
            | ndarray with spectrum or spectra (one for each rgb value, first row are the wavelengths)
    """
    if isinstance(rgb, list):
        rgb = np.atleast_2d(rgb)
    else:
        if rgb.max() > 1:
            rgb = rgb / (2 ** bitdepth - 1)
        if rgb2spec is None:
            rgb2spec = _BASESPEC_SMITS
        rgb2spec = np.array_equal(rgb2spec['wlr'], getwlr(wlr)) or _convert_to_wlr(entries=(copy.deepcopy(rgb2spec)), wlr=wlr)
    spec = np.zeros((rgb.shape[0], rgb2spec['wlr'].shape[0]))
    for i in range(rgb.shape[0]):
        spec[i, :] = _fromLinearRGB((rgb[i, :]), intent=intent, rgb2spec=rgb2spec, wlr=wlr)

    return np.vstack((rgb2spec['wlr'], spec))


if __name__ == '__main__':
    import luxpy as lx
    import matplotlib.pyplot as plt
    rfl = rgb_to_spec_smits([[100, 100, 100], [100, 150, 200]], wlr=[360, 830, 1])
    plt.figure()
    lx.SPD(rfl).plot()