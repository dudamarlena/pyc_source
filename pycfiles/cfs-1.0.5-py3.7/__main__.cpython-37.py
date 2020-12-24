# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/cf/__main__.py
# Compiled at: 2019-07-09 05:11:54
# Size of source mod 2**32: 5758 bytes
import sys, argparse, requests, json
from cf.user_info import *
from cf.user_rating import *
from cf.contest_list import *
from cf.problems import *
from cf.blog import *
from cf.ratingchange import *
from cf.bloguser import *
from cf.userstatus import *
from cf.conteststatus import *
from cf.compare import *
from yaspin import yaspin
from yaspin.spinners import Spinners

def get_req(url):
    with yaspin((Spinners.arc), text='Loading', color='magenta', side='right', reversal=True) as (sp):
        res = requests.get(url)
    comm = json.loads(res.text)
    if comm['status'] != 'OK':
        print(comm['comment'])
        sys.exit(1)
    return res


def get_parser():
    parser = argparse.ArgumentParser(description='Codeforces CLI')
    parser.add_argument('-u', '--user', metavar='<HANDLE>', help='Display user details.')
    parser.add_argument('-g', '--graph', metavar='<HANDLE>', help='Display rating chart of user.')
    parser.add_argument('-c', '--contest', metavar='<CONTEST ID>', type=int, help='Details of contest.')
    parser.add_argument('--gym', action='store_true', help='Optional argument to list gym contests. Use with -c.')
    parser.add_argument('-p', '--problem', action='store_true', help='Retrieve all problems.')
    parser.add_argument('--tag', metavar='<TAG>', help='Tag of problems to retrieve.')
    parser.add_argument('-b', '--blog', metavar='<BLOG ID>', help='View the blog entry specified by id.')
    parser.add_argument('-rc', '--ratingchange', metavar='<CONTEST ID>', help='Get Rating change of contest id.')
    parser.add_argument('--handle', metavar='<HANDLE>', help='Specify handle.')
    parser.add_argument('-bu', '--bloguser', metavar='<HANDLE>', help='Get blog entries of user.')
    parser.add_argument('-us', '--userstatus', metavar='<HANDLE>', help='Get submissions of specified user.')
    parser.add_argument('--fr', metavar='<FROM>', help='1-based index of the first submission to return.')
    parser.add_argument('--count', metavar='<COUNT>', help='Number of returned submissions.')
    parser.add_argument('-cs', '--cstatus', metavar='<CONTEST ID>', help='Get contest submissions.')
    parser.add_argument('--compare', nargs=2, metavar='<USER1 USER2>', help='Compare two users.')
    return parser


def main--- This code section failed: ---

 L.  51         0  LOAD_FAST                'argv'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  52         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                argv
               12  STORE_FAST               'argv'
             14_0  COME_FROM             6  '6'

 L.  55        14  LOAD_GLOBAL              get_parser
               16  CALL_FUNCTION_0       0  '0 positional arguments'
               18  STORE_FAST               'parser'

 L.  56        20  LOAD_FAST                'parser'
               22  LOAD_METHOD              parse_args
               24  LOAD_FAST                'argv'
               26  LOAD_CONST               1
               28  LOAD_CONST               None
               30  BUILD_SLICE_2         2 
               32  BINARY_SUBSCR    
               34  CALL_METHOD_1         1  '1 positional argument'
               36  STORE_FAST               'args'

 L.  58        38  LOAD_FAST                'args'
               40  LOAD_ATTR                user
               42  STORE_FAST               'user'

 L.  59        44  LOAD_FAST                'args'
               46  LOAD_ATTR                graph
               48  STORE_FAST               'graph'

 L.  60        50  LOAD_FAST                'args'
               52  LOAD_ATTR                contest
               54  STORE_FAST               'contest'

 L.  61        56  LOAD_FAST                'args'
               58  LOAD_ATTR                gym
               60  STORE_FAST               'gym'

 L.  62        62  LOAD_FAST                'args'
               64  LOAD_ATTR                problem
               66  STORE_FAST               'problem'

 L.  63        68  LOAD_FAST                'args'
               70  LOAD_ATTR                tag
               72  STORE_FAST               'tag'

 L.  64        74  LOAD_FAST                'args'
               76  LOAD_ATTR                blog
               78  STORE_FAST               'blogid'

 L.  65        80  LOAD_FAST                'args'
               82  LOAD_ATTR                ratingchange
               84  STORE_FAST               'cid'

 L.  66        86  LOAD_FAST                'args'
               88  LOAD_ATTR                handle
               90  STORE_FAST               'handle'

 L.  67        92  LOAD_FAST                'args'
               94  LOAD_ATTR                bloguser
               96  STORE_FAST               'bloguser_'

 L.  68        98  LOAD_FAST                'args'
              100  LOAD_ATTR                userstatus
              102  STORE_FAST               'user_status'

 L.  69       104  LOAD_FAST                'args'
              106  LOAD_ATTR                fr
              108  STORE_FAST               'from_'

 L.  70       110  LOAD_FAST                'args'
              112  LOAD_ATTR                count
              114  STORE_FAST               'count'

 L.  71       116  LOAD_FAST                'args'
              118  LOAD_ATTR                cstatus
              120  STORE_FAST               'cstatus'

 L.  72       122  LOAD_FAST                'args'
              124  LOAD_ATTR                compare
              126  STORE_FAST               'comp'

 L.  74       128  LOAD_FAST                'user'
              130  POP_JUMP_IF_FALSE   166  'to 166'

 L.  75       132  LOAD_GLOBAL              get_req
              134  LOAD_STR                 'http://codeforces.com/api/user.info?handles={0}'
              136  LOAD_METHOD              format
              138  LOAD_FAST                'user'
              140  CALL_METHOD_1         1  '1 positional argument'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  STORE_FAST               'res'

 L.  76       146  LOAD_GLOBAL              user_info
              148  LOAD_GLOBAL              json
              150  LOAD_METHOD              loads
              152  LOAD_FAST                'res'
              154  LOAD_ATTR                text
              156  CALL_METHOD_1         1  '1 positional argument'
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  POP_TOP          
          162_164  JUMP_FORWARD        756  'to 756'
            166_0  COME_FROM           130  '130'

 L.  77       166  LOAD_FAST                'graph'
              168  POP_JUMP_IF_FALSE   204  'to 204'

 L.  78       170  LOAD_GLOBAL              get_req
              172  LOAD_STR                 'http://codeforces.com/api/user.rating?handle={0}'
              174  LOAD_METHOD              format
              176  LOAD_FAST                'graph'
              178  CALL_METHOD_1         1  '1 positional argument'
              180  CALL_FUNCTION_1       1  '1 positional argument'
              182  STORE_FAST               'res'

 L.  79       184  LOAD_GLOBAL              user_rating
              186  LOAD_GLOBAL              json
              188  LOAD_METHOD              loads
              190  LOAD_FAST                'res'
              192  LOAD_ATTR                text
              194  CALL_METHOD_1         1  '1 positional argument'
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  POP_TOP          
          200_202  JUMP_FORWARD        756  'to 756'
            204_0  COME_FROM           168  '168'

 L.  80       204  LOAD_FAST                'contest'
              206  POP_JUMP_IF_FALSE   252  'to 252'

 L.  81       208  LOAD_FAST                'gym'
              210  POP_JUMP_IF_FALSE   222  'to 222'

 L.  82       212  LOAD_GLOBAL              get_req
              214  LOAD_STR                 'http://codeforces.com/api/contest.list?gym=true'
              216  CALL_FUNCTION_1       1  '1 positional argument'
              218  STORE_FAST               'res'
              220  JUMP_FORWARD        230  'to 230'
            222_0  COME_FROM           210  '210'

 L.  84       222  LOAD_GLOBAL              get_req
              224  LOAD_STR                 'http://codeforces.com/api/contest.list'
              226  CALL_FUNCTION_1       1  '1 positional argument'
              228  STORE_FAST               'res'
            230_0  COME_FROM           220  '220'

 L.  85       230  LOAD_GLOBAL              contest_list
              232  LOAD_GLOBAL              json
              234  LOAD_METHOD              loads
              236  LOAD_FAST                'res'
              238  LOAD_ATTR                text
              240  CALL_METHOD_1         1  '1 positional argument'
              242  LOAD_FAST                'contest'
              244  CALL_FUNCTION_2       2  '2 positional arguments'
              246  POP_TOP          
          248_250  JUMP_FORWARD        756  'to 756'
            252_0  COME_FROM           206  '206'

 L.  86       252  LOAD_FAST                'problem'
          254_256  POP_JUMP_IF_FALSE   308  'to 308'

 L.  87       258  LOAD_FAST                'tag'
          260_262  POP_JUMP_IF_FALSE   280  'to 280'

 L.  88       264  LOAD_GLOBAL              get_req
              266  LOAD_STR                 'https://codeforces.com/api/problemset.problems?tags={}'
              268  LOAD_METHOD              format
              270  LOAD_FAST                'tag'
              272  CALL_METHOD_1         1  '1 positional argument'
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  STORE_FAST               'res'
              278  JUMP_FORWARD        288  'to 288'
            280_0  COME_FROM           260  '260'

 L.  90       280  LOAD_GLOBAL              get_req
              282  LOAD_STR                 'https://codeforces.com/api/problemset.problems'
              284  CALL_FUNCTION_1       1  '1 positional argument'
              286  STORE_FAST               'res'
            288_0  COME_FROM           278  '278'

 L.  91       288  LOAD_GLOBAL              p_main
              290  LOAD_GLOBAL              json
              292  LOAD_METHOD              loads
              294  LOAD_FAST                'res'
              296  LOAD_ATTR                text
              298  CALL_METHOD_1         1  '1 positional argument'
              300  CALL_FUNCTION_1       1  '1 positional argument'
              302  POP_TOP          
          304_306  JUMP_FORWARD        756  'to 756'
            308_0  COME_FROM           254  '254'

 L.  92       308  LOAD_FAST                'blogid'
          310_312  POP_JUMP_IF_FALSE   372  'to 372'

 L.  93       314  LOAD_GLOBAL              get_req
              316  LOAD_STR                 'https://codeforces.com/api/blogEntry.view?blogEntryId={}'
              318  LOAD_METHOD              format
              320  LOAD_FAST                'blogid'
              322  CALL_METHOD_1         1  '1 positional argument'
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               'res'

 L.  94       328  LOAD_GLOBAL              get_req
              330  LOAD_STR                 'https://codeforces.com/api/blogEntry.comments?blogEntryId={}'
              332  LOAD_METHOD              format
              334  LOAD_FAST                'blogid'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  CALL_FUNCTION_1       1  '1 positional argument'
              340  STORE_FAST               'comm'

 L.  95       342  LOAD_GLOBAL              blog
              344  LOAD_GLOBAL              json
              346  LOAD_METHOD              loads
              348  LOAD_FAST                'res'
              350  LOAD_ATTR                text
              352  CALL_METHOD_1         1  '1 positional argument'
              354  LOAD_GLOBAL              json
              356  LOAD_METHOD              loads
              358  LOAD_FAST                'comm'
              360  LOAD_ATTR                text
              362  CALL_METHOD_1         1  '1 positional argument'
              364  CALL_FUNCTION_2       2  '2 positional arguments'
              366  POP_TOP          
          368_370  JUMP_FORWARD        756  'to 756'
            372_0  COME_FROM           310  '310'

 L.  96       372  LOAD_FAST                'cid'
          374_376  POP_JUMP_IF_FALSE   438  'to 438'

 L.  97       378  LOAD_GLOBAL              get_req
              380  LOAD_STR                 'https://codeforces.com/api/contest.ratingChanges?contestId={}'
              382  LOAD_METHOD              format
              384  LOAD_FAST                'cid'
              386  CALL_METHOD_1         1  '1 positional argument'
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  STORE_FAST               'res'

 L.  98       392  LOAD_FAST                'handle'
          394_396  POP_JUMP_IF_FALSE   418  'to 418'

 L.  99       398  LOAD_GLOBAL              rath
              400  LOAD_GLOBAL              json
              402  LOAD_METHOD              loads
              404  LOAD_FAST                'res'
              406  LOAD_ATTR                text
              408  CALL_METHOD_1         1  '1 positional argument'
              410  LOAD_FAST                'handle'
              412  CALL_FUNCTION_2       2  '2 positional arguments'
              414  POP_TOP          
              416  JUMP_FORWARD        756  'to 756'
            418_0  COME_FROM           394  '394'

 L. 101       418  LOAD_GLOBAL              ratc
              420  LOAD_GLOBAL              json
              422  LOAD_METHOD              loads
              424  LOAD_FAST                'res'
              426  LOAD_ATTR                text
              428  CALL_METHOD_1         1  '1 positional argument'
              430  CALL_FUNCTION_1       1  '1 positional argument'
              432  POP_TOP          
          434_436  JUMP_FORWARD        756  'to 756'
            438_0  COME_FROM           374  '374'

 L. 102       438  LOAD_FAST                'bloguser_'
          440_442  POP_JUMP_IF_FALSE   478  'to 478'

 L. 103       444  LOAD_GLOBAL              get_req
              446  LOAD_STR                 'https://codeforces.com/api/user.blogEntries?handle={}'
              448  LOAD_METHOD              format
              450  LOAD_FAST                'bloguser_'
              452  CALL_METHOD_1         1  '1 positional argument'
              454  CALL_FUNCTION_1       1  '1 positional argument'
              456  STORE_FAST               'res'

 L. 104       458  LOAD_GLOBAL              bloguser
              460  LOAD_GLOBAL              json
              462  LOAD_METHOD              loads
              464  LOAD_FAST                'res'
              466  LOAD_ATTR                text
              468  CALL_METHOD_1         1  '1 positional argument'
              470  CALL_FUNCTION_1       1  '1 positional argument'
              472  POP_TOP          
          474_476  JUMP_FORWARD        756  'to 756'
            478_0  COME_FROM           440  '440'

 L. 105       478  LOAD_FAST                'user_status'
          480_482  POP_JUMP_IF_FALSE   568  'to 568'

 L. 106       484  LOAD_FAST                'from_'
          486_488  POP_JUMP_IF_TRUE    512  'to 512'
              490  LOAD_FAST                'count'
          492_494  POP_JUMP_IF_TRUE    512  'to 512'

 L. 107       496  LOAD_GLOBAL              get_req
              498  LOAD_STR                 'https://codeforces.com/api/user.status?handle={}'
              500  LOAD_METHOD              format
              502  LOAD_FAST                'user_status'
              504  CALL_METHOD_1         1  '1 positional argument'
              506  CALL_FUNCTION_1       1  '1 positional argument'
              508  STORE_FAST               'res'
              510  JUMP_FORWARD        550  'to 550'
            512_0  COME_FROM           492  '492'
            512_1  COME_FROM           486  '486'

 L. 109       512  LOAD_FAST                'from_'
          514_516  POP_JUMP_IF_TRUE    522  'to 522'

 L. 110       518  LOAD_CONST               1
              520  STORE_FAST               'from_'
            522_0  COME_FROM           514  '514'

 L. 111       522  LOAD_FAST                'count'
          524_526  POP_JUMP_IF_TRUE    532  'to 532'

 L. 112       528  LOAD_CONST               10
              530  STORE_FAST               'count'
            532_0  COME_FROM           524  '524'

 L. 113       532  LOAD_GLOBAL              get_req
              534  LOAD_STR                 'https://codeforces.com/api/user.status?handle={}&from={}&count={}'
              536  LOAD_METHOD              format
              538  LOAD_FAST                'user_status'
              540  LOAD_FAST                'from_'
              542  LOAD_FAST                'count'
              544  CALL_METHOD_3         3  '3 positional arguments'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  STORE_FAST               'res'
            550_0  COME_FROM           510  '510'

 L. 114       550  LOAD_GLOBAL              userstatus
              552  LOAD_GLOBAL              json
              554  LOAD_METHOD              loads
              556  LOAD_FAST                'res'
              558  LOAD_ATTR                text
              560  CALL_METHOD_1         1  '1 positional argument'
              562  CALL_FUNCTION_1       1  '1 positional argument'
              564  POP_TOP          
              566  JUMP_FORWARD        756  'to 756'
            568_0  COME_FROM           480  '480'

 L. 115       568  LOAD_FAST                'cstatus'
          570_572  POP_JUMP_IF_FALSE   710  'to 710'

 L. 116       574  LOAD_FAST                'from_'
          576_578  POP_JUMP_IF_TRUE    626  'to 626'
              580  LOAD_FAST                'count'
          582_584  POP_JUMP_IF_TRUE    626  'to 626'

 L. 117       586  LOAD_FAST                'handle'
          588_590  POP_JUMP_IF_FALSE   610  'to 610'

 L. 118       592  LOAD_GLOBAL              get_req
              594  LOAD_STR                 'https://codeforces.com/api/contest.status?contestId={}&handle={}'
              596  LOAD_METHOD              format
              598  LOAD_FAST                'cstatus'
              600  LOAD_FAST                'handle'
              602  CALL_METHOD_2         2  '2 positional arguments'
              604  CALL_FUNCTION_1       1  '1 positional argument'
              606  STORE_FAST               'res'
              608  JUMP_FORWARD        624  'to 624'
            610_0  COME_FROM           588  '588'

 L. 120       610  LOAD_GLOBAL              get_req
              612  LOAD_STR                 'https://codeforces.com/api/contest.status?contestId={}'
              614  LOAD_METHOD              format
              616  LOAD_FAST                'cstatus'
              618  CALL_METHOD_1         1  '1 positional argument'
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  STORE_FAST               'res'
            624_0  COME_FROM           608  '608'
              624  JUMP_FORWARD        692  'to 692'
            626_0  COME_FROM           582  '582'
            626_1  COME_FROM           576  '576'

 L. 122       626  LOAD_FAST                'from_'
          628_630  POP_JUMP_IF_TRUE    636  'to 636'

 L. 123       632  LOAD_CONST               1
              634  STORE_FAST               'from_'
            636_0  COME_FROM           628  '628'

 L. 124       636  LOAD_FAST                'count'
          638_640  POP_JUMP_IF_TRUE    646  'to 646'

 L. 125       642  LOAD_CONST               10
              644  STORE_FAST               'count'
            646_0  COME_FROM           638  '638'

 L. 126       646  LOAD_FAST                'handle'
          648_650  POP_JUMP_IF_FALSE   674  'to 674'

 L. 127       652  LOAD_GLOBAL              get_req
              654  LOAD_STR                 'https://codeforces.com/api/contest.status?contestId={}&handle={}&from={}&count={}'
              656  LOAD_METHOD              format
              658  LOAD_FAST                'cstatus'
              660  LOAD_FAST                'handle'
              662  LOAD_FAST                'from_'
              664  LOAD_FAST                'count'
              666  CALL_METHOD_4         4  '4 positional arguments'
              668  CALL_FUNCTION_1       1  '1 positional argument'
              670  STORE_FAST               'res'
              672  JUMP_FORWARD        692  'to 692'
            674_0  COME_FROM           648  '648'

 L. 129       674  LOAD_GLOBAL              get_req
              676  LOAD_STR                 'https://codeforces.com/api/contest.status?contestId={}&from={}&count={}'
              678  LOAD_METHOD              format
              680  LOAD_FAST                'cstatus'
              682  LOAD_FAST                'from_'
              684  LOAD_FAST                'count'
              686  CALL_METHOD_3         3  '3 positional arguments'
              688  CALL_FUNCTION_1       1  '1 positional argument'
              690  STORE_FAST               'res'
            692_0  COME_FROM           672  '672'
            692_1  COME_FROM           624  '624'

 L. 130       692  LOAD_GLOBAL              conteststatus
              694  LOAD_GLOBAL              json
              696  LOAD_METHOD              loads
              698  LOAD_FAST                'res'
              700  LOAD_ATTR                text
              702  CALL_METHOD_1         1  '1 positional argument'
              704  CALL_FUNCTION_1       1  '1 positional argument'
              706  POP_TOP          
              708  JUMP_FORWARD        756  'to 756'
            710_0  COME_FROM           570  '570'

 L. 131       710  LOAD_FAST                'comp'
          712_714  POP_JUMP_IF_FALSE   756  'to 756'

 L. 132       716  LOAD_GLOBAL              get_req
              718  LOAD_STR                 'http://codeforces.com/api/user.info?handles={};{}'
              720  LOAD_METHOD              format
              722  LOAD_FAST                'comp'
              724  LOAD_CONST               0
              726  BINARY_SUBSCR    
              728  LOAD_FAST                'comp'
              730  LOAD_CONST               1
              732  BINARY_SUBSCR    
              734  CALL_METHOD_2         2  '2 positional arguments'
            736_0  COME_FROM           416  '416'
              736  CALL_FUNCTION_1       1  '1 positional argument'
              738  STORE_FAST               'res'

 L. 133       740  LOAD_GLOBAL              compare
              742  LOAD_GLOBAL              json
              744  LOAD_METHOD              loads
              746  LOAD_FAST                'res'
              748  LOAD_ATTR                text
              750  CALL_METHOD_1         1  '1 positional argument'
              752  CALL_FUNCTION_1       1  '1 positional argument'
              754  POP_TOP          
            756_0  COME_FROM           712  '712'
            756_1  COME_FROM           708  '708'
            756_2  COME_FROM           566  '566'
            756_3  COME_FROM           474  '474'
            756_4  COME_FROM           434  '434'
            756_5  COME_FROM           368  '368'
            756_6  COME_FROM           304  '304'
            756_7  COME_FROM           248  '248'
            756_8  COME_FROM           200  '200'
            756_9  COME_FROM           162  '162'

Parse error at or near `COME_FROM' instruction at offset 736_0


if __name__ == '__main__':
    sys.exit(main(sys.argv))