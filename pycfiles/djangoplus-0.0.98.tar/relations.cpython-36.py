# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/utils/relations.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 13527 bytes
from djangoplus.utils import permissions
from djangoplus.ui.components.panel import ModelPanel
from djangoplus.ui.components.paginator import Paginator
from djangoplus.utils.metadata import get_fieldsets, get_metadata
from djangoplus.ui.components.forms import ModelForm, ValidationError

class Relation(object):

    def __init__--- This code section failed: ---

 L.  11         0  LOAD_FAST                'instance'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               instance

 L.  12         6  LOAD_GLOBAL              type
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                instance
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               model

 L.  13        18  LOAD_FAST                'relation_name'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               relation_name

 L.  14        24  LOAD_CONST               None
               26  LOAD_FAST                'self'
               28  STORE_ATTR               relation_verbose_name

 L.  15        30  LOAD_CONST               None
               32  LOAD_FAST                'self'
               34  STORE_ATTR               relation_model

 L.  16        36  LOAD_CONST               None
               38  LOAD_FAST                'self'
               40  STORE_ATTR               relation_value

 L.  17        42  LOAD_CONST               None
               44  LOAD_FAST                'self'
               46  STORE_ATTR               relation_type

 L.  18        48  LOAD_CONST               None
               50  LOAD_FAST                'self'
               52  STORE_ATTR               hidden_field_name

 L.  20        54  LOAD_GLOBAL              get_metadata
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                model
               60  LOAD_STR                 'app_label'
               62  CALL_FUNCTION_2       2  '2 positional arguments'
               64  STORE_FAST               'app_label'

 L.  21        66  LOAD_FAST                'self'
               68  LOAD_ATTR                model
               70  LOAD_ATTR                __name__
               72  LOAD_ATTR                lower
               74  CALL_FUNCTION_0       0  '0 positional arguments'
               76  STORE_FAST               'model_name'

 L.  23        78  LOAD_CONST               None
               80  LOAD_FAST                'self'
               82  STORE_ATTR               add_label

 L.  24        84  LOAD_CONST               None
               86  LOAD_FAST                'self'
               88  STORE_ATTR               can_add

 L.  25        90  LOAD_CONST               None
               92  LOAD_FAST                'self'
               94  STORE_ATTR               add_url

 L.  26        96  LOAD_CONST               None
               98  LOAD_FAST                'self'
              100  STORE_ATTR               edit_url

 L.  27       102  LOAD_CONST               None
              104  LOAD_FAST                'self'
              106  STORE_ATTR               view_url

 L.  28       108  LOAD_CONST               None
              110  LOAD_FAST                'self'
              112  STORE_ATTR               delete_url

 L.  30       114  LOAD_CONST               False
              116  LOAD_FAST                'self'
              118  STORE_ATTR               is_one_to_one

 L.  31       120  LOAD_CONST               False
              122  LOAD_FAST                'self'
              124  STORE_ATTR               is_many_to_one

 L.  32       126  LOAD_CONST               False
              128  LOAD_FAST                'self'
              130  STORE_ATTR               is_one_to_many

 L.  33       132  LOAD_CONST               False
              134  LOAD_FAST                'self'
              136  STORE_ATTR               is_one_to_many_reverse

 L.  34       138  LOAD_CONST               False
              140  LOAD_FAST                'self'
              142  STORE_ATTR               is_many_to_many

 L.  36       144  LOAD_GLOBAL              getattr
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                model
              150  LOAD_FAST                'relation_name'
              152  CALL_FUNCTION_2       2  '2 positional arguments'
              154  STORE_FAST               'attr'

 L.  37       156  LOAD_FAST                'attr'
              158  LOAD_ATTR                __class__
              160  LOAD_ATTR                __name__
              162  STORE_FAST               'descriptor_name'

 L.  39       164  LOAD_GLOBAL              hasattr
              166  LOAD_FAST                'attr'
              168  LOAD_STR                 'related'
              170  CALL_FUNCTION_2       2  '2 positional arguments'
              172  POP_JUMP_IF_FALSE   296  'to 296'

 L.  40       176  LOAD_FAST                'descriptor_name'
              178  LOAD_STR                 'ReverseOneToOneDescriptor'
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE  1264  'to 1264'

 L.  41       186  LOAD_CONST               True
              188  LOAD_FAST                'self'
              190  STORE_ATTR               is_one_to_one

 L.  42       192  LOAD_STR                 'OneToOne'
              194  LOAD_FAST                'self'
              196  STORE_ATTR               relation_type

 L.  43       198  LOAD_FAST                'attr'
              200  LOAD_ATTR                related
              202  LOAD_ATTR                remote_field
              204  LOAD_ATTR                model
              206  LOAD_FAST                'self'
              208  STORE_ATTR               relation_model

 L.  44       210  LOAD_GLOBAL              getattr
              212  LOAD_FAST                'attr'
              214  LOAD_ATTR                related
              216  LOAD_ATTR                target_field
              218  LOAD_ATTR                model
              220  LOAD_STR                 '_meta'
              222  CALL_FUNCTION_2       2  '2 positional arguments'
              224  LOAD_ATTR                verbose_name
              226  LOAD_FAST                'self'
              228  STORE_ATTR               relation_verbose_name

 L.  46       230  LOAD_GLOBAL              getattr
              232  LOAD_FAST                'instance'
              234  LOAD_FAST                'relation_name'
              236  CALL_FUNCTION_2       2  '2 positional arguments'
              238  LOAD_FAST                'self'
              240  STORE_ATTR               relation_value

 L.  47       242  LOAD_GLOBAL              get_metadata
              244  LOAD_FAST                'self'
              246  LOAD_ATTR                model
              248  LOAD_STR                 'app_label'
              250  CALL_FUNCTION_2       2  '2 positional arguments'
              252  STORE_FAST               'relation_app_label'

 L.  48       254  LOAD_FAST                'self'
              256  LOAD_ATTR                relation_model
              258  LOAD_ATTR                __name__
              260  LOAD_ATTR                lower
              262  CALL_FUNCTION_0       0  '0 positional arguments'
              264  STORE_FAST               'relation_model_name'

 L.  50       266  LOAD_CONST               None
              268  LOAD_FAST                'self'
              270  STORE_ATTR               add_url

 L.  51       272  LOAD_STR                 '/view/{}/{}/{}/'
              274  LOAD_ATTR                format
              276  LOAD_FAST                'relation_app_label'
              278  LOAD_FAST                'relation_model_name'
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                relation_value
              284  LOAD_ATTR                pk
              286  CALL_FUNCTION_3       3  '3 positional arguments'
              288  LOAD_FAST                'self'
              290  STORE_ATTR               view_url
              292  JUMP_FORWARD       1264  'to 1264'
              296  ELSE                     '1264'

 L.  53       296  LOAD_GLOBAL              hasattr
              298  LOAD_FAST                'attr'
              300  LOAD_STR                 'field'
              302  CALL_FUNCTION_2       2  '2 positional arguments'
              304  POP_JUMP_IF_FALSE  1126  'to 1126'

 L.  55       308  LOAD_FAST                'attr'
              310  LOAD_ATTR                field
              312  LOAD_ATTR                __class__
              314  LOAD_ATTR                __name__
              316  STORE_FAST               'field_name'

 L.  57       318  LOAD_FAST                'descriptor_name'
              320  LOAD_STR                 'ForwardOneToOneDescriptor'
              322  COMPARE_OP               ==
              324  POP_JUMP_IF_FALSE   500  'to 500'

 L.  58       328  LOAD_CONST               True
              330  LOAD_FAST                'self'
              332  STORE_ATTR               is_one_to_one

 L.  59       334  LOAD_STR                 'OneToOne'
              336  LOAD_FAST                'self'
              338  STORE_ATTR               relation_type

 L.  60       340  LOAD_FAST                'attr'
              342  LOAD_ATTR                field
              344  LOAD_ATTR                remote_field
              346  LOAD_ATTR                model
              348  LOAD_FAST                'self'
              350  STORE_ATTR               relation_model

 L.  61       352  LOAD_FAST                'attr'
              354  LOAD_ATTR                field
              356  LOAD_ATTR                verbose_name
              358  LOAD_FAST                'self'
              360  STORE_ATTR               relation_verbose_name

 L.  63       362  LOAD_GLOBAL              getattr
              364  LOAD_FAST                'instance'
              366  LOAD_FAST                'relation_name'
              368  CALL_FUNCTION_2       2  '2 positional arguments'
              370  LOAD_FAST                'self'
              372  STORE_ATTR               relation_value

 L.  64       374  LOAD_GLOBAL              get_metadata
              376  LOAD_FAST                'self'
              378  LOAD_ATTR                relation_model
              380  LOAD_STR                 'app_label'
              382  CALL_FUNCTION_2       2  '2 positional arguments'
              384  STORE_FAST               'relation_app_label'

 L.  65       386  LOAD_FAST                'self'
              388  LOAD_ATTR                relation_model
              390  LOAD_ATTR                __name__
              392  LOAD_ATTR                lower
              394  CALL_FUNCTION_0       0  '0 positional arguments'
              396  STORE_FAST               'relation_model_name'

 L.  67       398  LOAD_STR                 '/add/{}/{}/{}/{}/'
              400  LOAD_ATTR                format
              402  LOAD_FAST                'app_label'
              404  LOAD_FAST                'model_name'
              406  LOAD_FAST                'self'
              408  LOAD_ATTR                instance
              410  LOAD_ATTR                pk
              412  LOAD_FAST                'relation_name'
              414  CALL_FUNCTION_4       4  '4 positional arguments'
              416  LOAD_FAST                'self'
              418  STORE_ATTR               add_url

 L.  68       420  LOAD_FAST                'self'
              422  LOAD_ATTR                relation_value
              424  POP_JUMP_IF_FALSE  1124  'to 1124'

 L.  69       428  LOAD_STR                 '/add/{}/{}/{}/{}/{}/'
              430  LOAD_ATTR                format
              432  LOAD_FAST                'app_label'
              434  LOAD_FAST                'model_name'
              436  LOAD_FAST                'self'
              438  LOAD_ATTR                instance
              440  LOAD_ATTR                pk
              442  LOAD_FAST                'relation_name'
              444  LOAD_FAST                'self'
              446  LOAD_ATTR                relation_value
              448  LOAD_ATTR                pk
              450  CALL_FUNCTION_5       5  '5 positional arguments'
              452  LOAD_FAST                'self'
              454  STORE_ATTR               add_url

 L.  70       456  LOAD_STR                 '/view/{}/{}/{}/'
              458  LOAD_ATTR                format
              460  LOAD_FAST                'relation_app_label'
              462  LOAD_FAST                'relation_model_name'
              464  LOAD_FAST                'self'
              466  LOAD_ATTR                relation_value
              468  LOAD_ATTR                pk
              470  CALL_FUNCTION_3       3  '3 positional arguments'
              472  LOAD_FAST                'self'
              474  STORE_ATTR               view_url

 L.  71       476  LOAD_STR                 '/delete/{}/{}/{}/'
              478  LOAD_ATTR                format
              480  LOAD_FAST                'relation_app_label'
              482  LOAD_FAST                'relation_model_name'
              484  LOAD_FAST                'self'
              486  LOAD_ATTR                relation_value
              488  LOAD_ATTR                pk
              490  CALL_FUNCTION_3       3  '3 positional arguments'
              492  LOAD_FAST                'self'
              494  STORE_ATTR               delete_url
              496  JUMP_ABSOLUTE      1264  'to 1264'
              500  ELSE                     '1124'

 L.  73       500  LOAD_FAST                'descriptor_name'
              502  LOAD_STR                 'ForwardManyToOneDescriptor'
              504  COMPARE_OP               ==
              506  POP_JUMP_IF_FALSE   612  'to 612'

 L.  74       510  LOAD_CONST               True
              512  LOAD_FAST                'self'
              514  STORE_ATTR               is_many_to_one

 L.  75       516  LOAD_STR                 'ManyToOne'
              518  LOAD_FAST                'self'
              520  STORE_ATTR               relation_type

 L.  76       522  LOAD_FAST                'attr'
              524  LOAD_ATTR                field
              526  LOAD_ATTR                remote_field
              528  LOAD_ATTR                model
              530  LOAD_FAST                'self'
              532  STORE_ATTR               relation_model

 L.  77       534  LOAD_FAST                'attr'
              536  LOAD_ATTR                field
              538  LOAD_ATTR                verbose_name
              540  LOAD_FAST                'self'
              542  STORE_ATTR               relation_verbose_name

 L.  79       544  LOAD_GLOBAL              getattr
              546  LOAD_FAST                'instance'
              548  LOAD_FAST                'relation_name'
              550  CALL_FUNCTION_2       2  '2 positional arguments'
              552  LOAD_FAST                'self'
              554  STORE_ATTR               relation_value

 L.  80       556  LOAD_GLOBAL              get_metadata
              558  LOAD_FAST                'self'
              560  LOAD_ATTR                relation_model
              562  LOAD_STR                 'app_label'
              564  CALL_FUNCTION_2       2  '2 positional arguments'
              566  STORE_FAST               'relation_app_label'

 L.  81       568  LOAD_FAST                'self'
              570  LOAD_ATTR                relation_model
              572  LOAD_ATTR                __name__
              574  LOAD_ATTR                lower
              576  CALL_FUNCTION_0       0  '0 positional arguments'
              578  STORE_FAST               'relation_model_name'

 L.  82       580  LOAD_FAST                'self'
              582  LOAD_ATTR                relation_value
              584  POP_JUMP_IF_FALSE  1124  'to 1124'

 L.  83       588  LOAD_STR                 '/view/{}/{}/{}/'
              590  LOAD_ATTR                format
              592  LOAD_FAST                'relation_app_label'
              594  LOAD_FAST                'relation_model_name'
              596  LOAD_FAST                'self'
              598  LOAD_ATTR                relation_value
              600  LOAD_ATTR                pk
              602  CALL_FUNCTION_3       3  '3 positional arguments'
              604  LOAD_FAST                'self'
              606  STORE_ATTR               view_url
              608  JUMP_ABSOLUTE      1264  'to 1264'
              612  ELSE                     '1124'

 L.  85       612  LOAD_FAST                'descriptor_name'
              614  LOAD_STR                 'ManyToManyDescriptor'
              616  COMPARE_OP               ==
              618  POP_JUMP_IF_FALSE   778  'to 778'
              622  LOAD_FAST                'field_name'
              624  LOAD_STR                 'OneToManyField'
              626  COMPARE_OP               ==
              628  POP_JUMP_IF_FALSE   778  'to 778'

 L.  86       632  LOAD_CONST               True
              634  LOAD_FAST                'self'
              636  STORE_ATTR               is_one_to_many

 L.  87       638  LOAD_STR                 'OneToMany'
              640  LOAD_FAST                'self'
              642  STORE_ATTR               relation_type

 L.  88       644  LOAD_FAST                'attr'
              646  LOAD_ATTR                field
              648  LOAD_ATTR                remote_field
              650  LOAD_ATTR                model
              652  LOAD_FAST                'self'
              654  STORE_ATTR               relation_model

 L.  89       656  LOAD_FAST                'attr'
              658  LOAD_ATTR                field
              660  LOAD_ATTR                verbose_name
              662  LOAD_FAST                'self'
              664  STORE_ATTR               relation_verbose_name

 L.  90       666  LOAD_FAST                'attr'
              668  LOAD_ATTR                field
              670  LOAD_ATTR                add_label
              672  LOAD_FAST                'self'
              674  STORE_ATTR               add_label

 L.  92       676  LOAD_GLOBAL              getattr
              678  LOAD_FAST                'instance'
              680  LOAD_FAST                'relation_name'
              682  CALL_FUNCTION_2       2  '2 positional arguments'
              684  LOAD_ATTR                all
              686  CALL_FUNCTION_0       0  '0 positional arguments'
              688  LOAD_FAST                'self'
              690  STORE_ATTR               relation_value

 L.  93       692  LOAD_GLOBAL              get_metadata
              694  LOAD_FAST                'self'
              696  LOAD_ATTR                relation_model
              698  LOAD_STR                 'app_label'
              700  CALL_FUNCTION_2       2  '2 positional arguments'
              702  STORE_FAST               'relation_app_label'

 L.  94       704  LOAD_FAST                'self'
              706  LOAD_ATTR                relation_model
              708  LOAD_ATTR                __name__
              710  LOAD_ATTR                lower
              712  CALL_FUNCTION_0       0  '0 positional arguments'
              714  STORE_FAST               'relation_model_name'

 L.  96       716  LOAD_STR                 '/view/{}/{}/{{}}/'
              718  LOAD_ATTR                format
              720  LOAD_FAST                'relation_app_label'
              722  LOAD_FAST                'relation_model_name'
              724  CALL_FUNCTION_2       2  '2 positional arguments'
              726  LOAD_FAST                'self'
              728  STORE_ATTR               view_url

 L.  97       730  LOAD_STR                 '/add/{}/{}/{}/{}/'
              732  LOAD_ATTR                format
              734  LOAD_FAST                'app_label'
              736  LOAD_FAST                'model_name'
              738  LOAD_FAST                'self'
              740  LOAD_ATTR                instance
              742  LOAD_ATTR                pk
              744  LOAD_FAST                'relation_name'
              746  CALL_FUNCTION_4       4  '4 positional arguments'
              748  LOAD_FAST                'self'
              750  STORE_ATTR               add_url

 L.  98       752  LOAD_STR                 '/delete/{}/{}/{}/{}/{{}}/'
              754  LOAD_ATTR                format
              756  LOAD_FAST                'app_label'
              758  LOAD_FAST                'model_name'
              760  LOAD_FAST                'self'
              762  LOAD_ATTR                instance
              764  LOAD_ATTR                pk
              766  LOAD_FAST                'relation_name'
              768  CALL_FUNCTION_4       4  '4 positional arguments'
              770  LOAD_FAST                'self'
              772  STORE_ATTR               delete_url
              774  JUMP_ABSOLUTE      1264  'to 1264'
            778_0  COME_FROM           618  '618'

 L. 100       778  LOAD_FAST                'descriptor_name'
              780  LOAD_STR                 'ReverseManyToOneDescriptor'
              782  COMPARE_OP               ==
              784  POP_JUMP_IF_FALSE   954  'to 954'

 L. 101       788  LOAD_CONST               True
              790  LOAD_FAST                'self'
              792  STORE_ATTR               is_one_to_many_reverse

 L. 102       794  LOAD_STR                 'OneToManyReverse'
              796  LOAD_FAST                'self'
              798  STORE_ATTR               relation_type

 L. 103       800  LOAD_FAST                'attr'
              802  LOAD_ATTR                field
              804  LOAD_ATTR                model
              806  LOAD_FAST                'self'
              808  STORE_ATTR               relation_model

 L. 104       810  LOAD_GLOBAL              getattr
              812  LOAD_FAST                'attr'
              814  LOAD_ATTR                field
              816  LOAD_ATTR                model
              818  LOAD_STR                 '_meta'
              820  CALL_FUNCTION_2       2  '2 positional arguments'
              822  LOAD_ATTR                verbose_name_plural
              824  LOAD_FAST                'self'
              826  STORE_ATTR               relation_verbose_name

 L. 106       828  LOAD_FAST                'attr'
              830  LOAD_ATTR                rel
              832  LOAD_ATTR                field
              834  LOAD_ATTR                name
              836  LOAD_FAST                'self'
              838  STORE_ATTR               hidden_field_name

 L. 107       840  LOAD_GLOBAL              getattr
              842  LOAD_FAST                'instance'
              844  LOAD_FAST                'relation_name'
              846  CALL_FUNCTION_2       2  '2 positional arguments'
              848  LOAD_ATTR                all
              850  CALL_FUNCTION_0       0  '0 positional arguments'
              852  LOAD_FAST                'self'
              854  STORE_ATTR               relation_value

 L. 108       856  LOAD_GLOBAL              get_metadata
              858  LOAD_FAST                'self'
              860  LOAD_ATTR                relation_model
              862  LOAD_STR                 'app_label'
              864  CALL_FUNCTION_2       2  '2 positional arguments'
              866  STORE_FAST               'relation_app_label'

 L. 109       868  LOAD_FAST                'self'
              870  LOAD_ATTR                relation_model
              872  LOAD_ATTR                __name__
              874  LOAD_ATTR                lower
              876  CALL_FUNCTION_0       0  '0 positional arguments'
              878  STORE_FAST               'relation_model_name'

 L. 111       880  LOAD_STR                 '/add/{}/{}/{}/{}/'
              882  LOAD_ATTR                format
              884  LOAD_FAST                'app_label'
              886  LOAD_FAST                'model_name'
              888  LOAD_FAST                'self'
              890  LOAD_ATTR                instance
              892  LOAD_ATTR                pk
              894  LOAD_FAST                'relation_name'
              896  CALL_FUNCTION_4       4  '4 positional arguments'
              898  LOAD_FAST                'self'
              900  STORE_ATTR               add_url

 L. 112       902  LOAD_STR                 '/add/{}/{}/{}/{}/{{}}/'
              904  LOAD_ATTR                format
              906  LOAD_FAST                'app_label'
              908  LOAD_FAST                'model_name'
              910  LOAD_FAST                'self'
              912  LOAD_ATTR                instance
              914  LOAD_ATTR                pk
              916  LOAD_FAST                'relation_name'
              918  CALL_FUNCTION_4       4  '4 positional arguments'
              920  LOAD_FAST                'self'
              922  STORE_ATTR               edit_url

 L. 113       924  LOAD_STR                 '/view/{}/{}/{{}}/'
              926  LOAD_ATTR                format
              928  LOAD_FAST                'relation_app_label'
              930  LOAD_FAST                'relation_model_name'
              932  CALL_FUNCTION_2       2  '2 positional arguments'
              934  LOAD_FAST                'self'
              936  STORE_ATTR               view_url

 L. 114       938  LOAD_STR                 '/delete/{}/{}/{{}}/'
              940  LOAD_ATTR                format
              942  LOAD_FAST                'relation_app_label'
              944  LOAD_FAST                'relation_model_name'
              946  CALL_FUNCTION_2       2  '2 positional arguments'
              948  LOAD_FAST                'self'
              950  STORE_ATTR               delete_url
              952  JUMP_FORWARD       1124  'to 1124'
              954  ELSE                     '1124'

 L. 116       954  LOAD_FAST                'descriptor_name'
              956  LOAD_STR                 'ManyToManyDescriptor'
              958  COMPARE_OP               ==
              960  POP_JUMP_IF_FALSE  1118  'to 1118'

 L. 117       964  LOAD_CONST               True
              966  LOAD_FAST                'self'
              968  STORE_ATTR               is_many_to_many

 L. 118       970  LOAD_STR                 'ManyToMany'
              972  LOAD_FAST                'self'
              974  STORE_ATTR               relation_type

 L. 119       976  LOAD_FAST                'attr'
              978  LOAD_ATTR                field
              980  LOAD_ATTR                remote_field
              982  LOAD_ATTR                model
              984  LOAD_FAST                'self'
              986  STORE_ATTR               relation_model

 L. 120       988  LOAD_FAST                'attr'
              990  LOAD_ATTR                field
              992  LOAD_ATTR                verbose_name
              994  LOAD_FAST                'self'
              996  STORE_ATTR               relation_verbose_name

 L. 121       998  LOAD_FAST                'attr'
             1000  LOAD_ATTR                field
             1002  LOAD_ATTR                add_label
             1004  LOAD_FAST                'self'
             1006  STORE_ATTR               add_label

 L. 122      1008  LOAD_FAST                'attr'
             1010  LOAD_ATTR                field
             1012  LOAD_ATTR                can_add
             1014  LOAD_FAST                'self'
             1016  STORE_ATTR               can_add

 L. 124      1018  LOAD_GLOBAL              getattr
             1020  LOAD_FAST                'instance'
             1022  LOAD_FAST                'relation_name'
             1024  CALL_FUNCTION_2       2  '2 positional arguments'
             1026  LOAD_ATTR                all
             1028  CALL_FUNCTION_0       0  '0 positional arguments'
             1030  LOAD_FAST                'self'
             1032  STORE_ATTR               relation_value

 L. 125      1034  LOAD_GLOBAL              get_metadata
             1036  LOAD_FAST                'self'
             1038  LOAD_ATTR                relation_model
             1040  LOAD_STR                 'app_label'
             1042  CALL_FUNCTION_2       2  '2 positional arguments'
             1044  STORE_FAST               'relation_app_label'

 L. 126      1046  LOAD_FAST                'self'
             1048  LOAD_ATTR                relation_model
             1050  LOAD_ATTR                __name__
             1052  LOAD_ATTR                lower
             1054  CALL_FUNCTION_0       0  '0 positional arguments'
             1056  STORE_FAST               'relation_model_name'

 L. 128      1058  LOAD_STR                 '/view/{}/{}/{{}}/'
             1060  LOAD_ATTR                format
             1062  LOAD_FAST                'relation_app_label'
             1064  LOAD_FAST                'relation_model_name'
             1066  CALL_FUNCTION_2       2  '2 positional arguments'
             1068  LOAD_FAST                'self'
             1070  STORE_ATTR               view_url

 L. 129      1072  LOAD_STR                 '/add/{}/{}/{}/{}/'
             1074  LOAD_ATTR                format
             1076  LOAD_FAST                'app_label'
             1078  LOAD_FAST                'model_name'
             1080  LOAD_FAST                'self'
             1082  LOAD_ATTR                instance
             1084  LOAD_ATTR                pk
             1086  LOAD_FAST                'relation_name'
             1088  CALL_FUNCTION_4       4  '4 positional arguments'
             1090  LOAD_FAST                'self'
             1092  STORE_ATTR               add_url

 L. 130      1094  LOAD_STR                 '/delete/{}/{}/{}/{}/{{}}/'
             1096  LOAD_ATTR                format
             1098  LOAD_FAST                'app_label'
             1100  LOAD_FAST                'model_name'
             1102  LOAD_FAST                'self'
             1104  LOAD_ATTR                instance
             1106  LOAD_ATTR                pk
             1108  LOAD_FAST                'relation_name'
             1110  CALL_FUNCTION_4       4  '4 positional arguments'
             1112  LOAD_FAST                'self'
             1114  STORE_ATTR               delete_url
             1116  JUMP_FORWARD       1124  'to 1124'
             1118  ELSE                     '1124'

 L. 132      1118  LOAD_GLOBAL              Exception
             1120  CALL_FUNCTION_0       0  '0 positional arguments'
             1122  RAISE_VARARGS_1       1  'exception'
           1124_0  COME_FROM          1116  '1116'
           1124_1  COME_FROM           952  '952'
           1124_2  COME_FROM           584  '584'
           1124_3  COME_FROM           424  '424'
             1124  JUMP_FORWARD       1264  'to 1264'
             1126  ELSE                     '1264'

 L. 133      1126  LOAD_GLOBAL              hasattr
             1128  LOAD_FAST                'attr'
             1130  LOAD_STR                 '_metadata'
             1132  CALL_FUNCTION_2       2  '2 positional arguments'
             1134  POP_JUMP_IF_FALSE  1258  'to 1258'

 L. 134      1138  LOAD_GLOBAL              getattr
             1140  LOAD_FAST                'self'
             1142  LOAD_ATTR                instance
             1144  LOAD_FAST                'self'
             1146  LOAD_ATTR                relation_name
             1148  CALL_FUNCTION_2       2  '2 positional arguments'
             1150  CALL_FUNCTION_0       0  '0 positional arguments'
             1152  LOAD_FAST                'self'
             1154  STORE_ATTR               relation_value

 L. 135      1156  LOAD_GLOBAL              hasattr
             1158  LOAD_FAST                'self'
             1160  LOAD_ATTR                relation_value
             1162  LOAD_STR                 'model'
             1164  CALL_FUNCTION_2       2  '2 positional arguments'
             1166  POP_JUMP_IF_FALSE  1182  'to 1182'

 L. 136      1170  LOAD_FAST                'self'
             1172  LOAD_ATTR                relation_value
             1174  LOAD_ATTR                model
             1176  LOAD_FAST                'self'
             1178  STORE_ATTR               relation_model
             1180  JUMP_FORWARD       1194  'to 1194'
             1182  ELSE                     '1194'

 L. 138      1182  LOAD_GLOBAL              type
             1184  LOAD_FAST                'self'
             1186  LOAD_ATTR                relation_value
             1188  CALL_FUNCTION_1       1  '1 positional argument'
             1190  LOAD_FAST                'self'
             1192  STORE_ATTR               relation_model
           1194_0  COME_FROM          1180  '1180'

 L. 139      1194  LOAD_GLOBAL              getattr
             1196  LOAD_FAST                'attr'
             1198  LOAD_STR                 '_metadata'
             1200  CALL_FUNCTION_2       2  '2 positional arguments'
             1202  LOAD_STR                 '{}:verbose_name'
             1204  LOAD_ATTR                format
             1206  LOAD_FAST                'self'
             1208  LOAD_ATTR                relation_name
             1210  CALL_FUNCTION_1       1  '1 positional argument'
             1212  BINARY_SUBSCR    
             1214  LOAD_FAST                'self'
             1216  STORE_ATTR               relation_verbose_name

 L. 141      1218  LOAD_GLOBAL              get_metadata
             1220  LOAD_FAST                'self'
             1222  LOAD_ATTR                relation_model
             1224  LOAD_STR                 'app_label'
             1226  CALL_FUNCTION_2       2  '2 positional arguments'
             1228  STORE_FAST               'relation_app_label'

 L. 142      1230  LOAD_FAST                'self'
             1232  LOAD_ATTR                relation_model
             1234  LOAD_ATTR                __name__
             1236  LOAD_ATTR                lower
             1238  CALL_FUNCTION_0       0  '0 positional arguments'
             1240  STORE_FAST               'relation_model_name'

 L. 143      1242  LOAD_STR                 '/view/{}/{}/{{}}/'
             1244  LOAD_ATTR                format
             1246  LOAD_FAST                'relation_app_label'
             1248  LOAD_FAST                'relation_model_name'
             1250  CALL_FUNCTION_2       2  '2 positional arguments'
             1252  LOAD_FAST                'self'
             1254  STORE_ATTR               view_url
             1256  JUMP_FORWARD       1264  'to 1264'
             1258  ELSE                     '1264'

 L. 145      1258  LOAD_GLOBAL              Exception
             1260  CALL_FUNCTION_0       0  '0 positional arguments'
             1262  RAISE_VARARGS_1       1  'exception'
           1264_0  COME_FROM          1256  '1256'
           1264_1  COME_FROM          1124  '1124'
           1264_2  COME_FROM           292  '292'
           1264_3  COME_FROM           182  '182'

Parse error at or near `COME_FROM' instruction at offset 1264_2

    def get_component(self, request, as_pdf=False):
        verbose_name = getattr(self.relation_model, '_meta').verbose_name
        if self.is_one_to_one or self.is_many_to_one:
            panel_fieldsets = getattr(self.relation_model, 'fieldsets', None)
            if panel_fieldsets:
                panel_fieldsets = (
                 (
                  self.relation_verbose_name, panel_fieldsets[0][1]),)
            else:
                panel_fieldsets = get_fieldsets(self.relation_model, self.relation_verbose_name)
            component = ModelPanel(request, (self.relation_value or self.relation_model), fieldsets=panel_fieldsets, complete=False)
            if self.view_url:
                if permissions.has_view_permission(request, self.relation_model):
                    label = 'Detalhar {}'.formatverbose_name
                    component.drop_down.add_action(label, (self.view_url), 'ajax', 'fa-eye', category=label)
            if self.add_url:
                if permissions.has_edit_permission(request, self.model):
                    label = 'Atualizar {}'.formatverbose_name
                    component.drop_down.add_action(label, (self.add_url), 'popup', 'fa-edit', category=label)
            if self.delete_url and permissions.has_edit_permission(request, self.model):
                label = 'Excluir {}'.formatverbose_name
                component.drop_down.add_action(label, (self.delete_url), 'popup', 'fa-close', category=label)
        else:
            inlines = []
            fieldsets = getattr(self.model, 'fieldsets', ())
            title = self.relation_verbose_name
            for fieldset in fieldsets:
                fieldset_relations = fieldset[1].get('relations', ())
                fieldset_inlines = fieldset[1].get('inlines', ())
                fieldset_fields = fieldset[1].get('fields', ())
                for inline in fieldset_inlines:
                    inlines.appendinline

                if (self.relation_name in fieldset_relations or self.relation_name in fieldset_inlines or self.relation_name in fieldset_fields) and lenfieldset_relations + lenfieldset_inlines + lenfieldset_fields == 1:
                    title = fieldset[0].split'::'[(-1)]

            if self.is_one_to_many or self.is_many_to_many:
                if self.can_add:
                    has_add_permission = permissions.check_group_or_permission(request, self.can_add)
                else:
                    has_add_permission = permissions.has_add_permission(request, self.model)
            else:
                has_add_permission = permissions.has_add_permission(request, self.relation_model)
            component = Paginator(request, (self.relation_value.allrequest.user), title, relation=self, list_subsets=[], readonly=(not has_add_permission))
            component.add_actions
            instance = self.relation_model
            if self.hidden_field_name:
                setattr(instance, self.hidden_field_name, self.instance)
            can_add = not hasattr(instance, 'can_add') or instance.can_add
        if self.add_url:
            if has_add_permission:
                if can_add:
                    if self.relation_name in inlines:
                        form_name = get_metadata(self.relation_model, 'add_form')
                        if form_name:
                            fromlist = get_metadata(self.relation_model, 'app_label')
                            forms_module = __import__(('{}.forms'.formatfromlist), fromlist=(listmap(str, [fromlist])))
                            Form = getattr(forms_module, form_name)
                        else:

                            class Form(ModelForm):

                                class Meta:
                                    model = self.relation_model
                                    fields = get_metadata(self.relation_model, 'form_fields', '__all__')
                                    exclude = get_metadata(self.relation_model, 'exclude_fields', ())
                                    submit_label = 'Adicionar'
                                    title = 'Adicionar {}'.formatget_metadata(self.relation_model, 'verbose_name')

                        form = Form(request, instance=instance, inline=True)
                        if self.hidden_field_name in form.fields:
                            del form.fields[self.hidden_field_name]
                        component.form = form
                        if form.is_valid:
                            try:
                                form.save
                                component.message = 'Ação realizada com sucesso'
                            except ValidationError as e:
                                form.add_error(None, stre.message)

                    else:
                        add_label = self.add_label or get_metadata(self.relation_model, 'add_label')
                        label = add_label or 'Adicionar {}'.formatverbose_name
                        component.add_actionlabelself.add_url'popup''fa-plus'
        component.as_pdf = as_pdf
        return component

    def debug(self):
        url = 'http://localhost:8000'
        print('Instance:', self.instance)
        print('Model:', self.model)
        print('Relation Name:', self.relation_name)
        print('Relation Verbose Name:', self.relation_verbose_name)
        print('Relation Model:', self.relation_model)
        print('Relation Value:', self.relation_value)
        print('Relation Type:', self.relation_type)
        if self.add_url:
            print('Add URL', '{}{}'.format(url, self.add_url))
        if self.edit_url:
            print('Edit URL', '{}{}'.format(url, self.edit_url))
        if self.view_url:
            print('View URL', '{}{}'.format(url, self.view_url))
        if self.delete_url:
            print('Delete URL', '{}{}'.format(url, self.delete_url))
        print'\n\n\n\n'