# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bart/mybot/mods/stats.py
# Compiled at: 2020-05-13 07:28:47
# Size of source mod 2**32: 20640 bytes
import bot, datetime, lo, lo.clk, lo.tms, random, time
k = bot.get_kernel()

def init(kernel):
    for name in wanted.keys():
        obj = wanted.get(name, None)
        if obj:
            e = lo.hdl.Event()
            e.txt = ''
            e.rest = name

    for key in obj.keys():
        if lo.cfg.options and key not in lo.cfg.options:
            pass
        else:
            val = obj.get(key, None)
            if val:
                sec = seconds(val)
                repeater = lo.clk.Repeater(sec, stat, e, name=('stats.%s' % key))
                repeater.start()


year_formats = [
 '%b %H:%M',
 '%b %H:%M:%S',
 '%a %H:%M %Y',
 '%a %H:%M',
 '%a %H:%M:%S',
 '%Y-%m-%d',
 '%d-%m-%Y',
 '%d-%m',
 '%m-%d',
 '%Y-%m-%d %H:%M:%S',
 '%d-%m-%Y %H:%M:%S',
 '%d-%m %H:%M:%S',
 '%m-%d %H:%M:%S',
 '%Y-%m-%d %H:%M',
 '%d-%m-%Y %H:%M',
 '%d-%m %H:%M',
 '%m-%d %H:%M',
 '%H:%M:%S',
 '%H:%M']

class ENOSTATS(Exception):
    pass


def day():
    return str(datetime.datetime.today()).split()[0]


def get_time--- This code section failed: ---

 L.  62         0  LOAD_GLOBAL              year_formats
                2  GET_ITER         
                4  FOR_ITER             60  'to 60'
                6  STORE_FAST               'f'

 L.  63         8  SETUP_FINALLY        38  'to 38'

 L.  64        10  LOAD_GLOBAL              time
               12  LOAD_METHOD              mktime
               14  LOAD_GLOBAL              time
               16  LOAD_METHOD              strptime
               18  LOAD_FAST                'daystr'
               20  LOAD_FAST                'f'
               22  CALL_METHOD_2         2  ''
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               't'

 L.  65        28  LOAD_FAST                't'
               30  POP_BLOCK        
               32  ROT_TWO          
               34  POP_TOP          
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY     8  '8'

 L.  66        38  DUP_TOP          
               40  LOAD_GLOBAL              Exception
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    56  'to 56'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  67        52  POP_EXCEPT       
               54  JUMP_BACK             4  'to 4'
             56_0  COME_FROM            44  '44'
               56  END_FINALLY      
               58  JUMP_BACK             4  'to 4'

Parse error at or near `ROT_TWO' instruction at offset 32


def today():
    return datetime.datetime.today().timestamp()


def to_day--- This code section failed: ---

 L.  73         0  LOAD_STR                 ''
                2  STORE_FAST               'line'

 L.  74         4  LOAD_GLOBAL              str
                6  LOAD_FAST                'daystring'
                8  CALL_FUNCTION_1       1  ''
               10  STORE_FAST               'daystr'

 L.  75        12  LOAD_FAST                'daystr'
               14  LOAD_METHOD              split
               16  CALL_METHOD_0         0  ''
               18  GET_ITER         
             20_0  COME_FROM            52  '52'
               20  FOR_ITER             64  'to 64'
               22  STORE_FAST               'word'

 L.  76        24  LOAD_STR                 '-'
               26  LOAD_FAST                'word'
               28  COMPARE_OP               in
               30  POP_JUMP_IF_FALSE    46  'to 46'

 L.  77        32  LOAD_FAST                'line'
               34  LOAD_FAST                'word'
               36  LOAD_STR                 ' '
               38  BINARY_ADD       
               40  INPLACE_ADD      
               42  STORE_FAST               'line'
               44  JUMP_BACK            20  'to 20'
             46_0  COME_FROM            30  '30'

 L.  78        46  LOAD_STR                 ':'
               48  LOAD_FAST                'word'
               50  COMPARE_OP               in
               52  POP_JUMP_IF_FALSE    20  'to 20'

 L.  79        54  LOAD_FAST                'line'
               56  LOAD_FAST                'word'
               58  INPLACE_ADD      
               60  STORE_FAST               'line'
               62  JUMP_BACK            20  'to 20'

 L.  80        64  LOAD_STR                 '-'
               66  LOAD_FAST                'line'
               68  COMPARE_OP               not-in
               70  POP_JUMP_IF_FALSE    86  'to 86'

 L.  81        72  LOAD_GLOBAL              day
               74  CALL_FUNCTION_0       0  ''
               76  LOAD_STR                 ' '
               78  BINARY_ADD       
               80  LOAD_FAST                'line'
               82  BINARY_ADD       
               84  STORE_FAST               'line'
             86_0  COME_FROM            70  '70'

 L.  82        86  SETUP_FINALLY       102  'to 102'

 L.  83        88  LOAD_GLOBAL              get_time
               90  LOAD_FAST                'line'
               92  LOAD_METHOD              strip
               94  CALL_METHOD_0         0  ''
               96  CALL_FUNCTION_1       1  ''
               98  POP_BLOCK        
              100  RETURN_VALUE     
            102_0  COME_FROM_FINALLY    86  '86'

 L.  84       102  DUP_TOP          
              104  LOAD_GLOBAL              ValueError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   120  'to 120'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L.  85       116  POP_EXCEPT       
              118  JUMP_FORWARD        122  'to 122'
            120_0  COME_FROM           108  '108'
              120  END_FINALLY      
            122_0  COME_FROM           118  '118'

Parse error at or near `POP_TOP' instruction at offset 112


startdate = '2018-10-05 00:00:00'
starttime = to_day(startdate)
source = 'https://bitbucket.org/botd/botlib'

def seconds(nr, period='jaar'):
    if not nr:
        return nr
    return nrsec.getperiod / float(nr)


def nr(name):
    for key in wanted.keys():
        obj = wanted.get(key, None)
        for n in obj.keys():
            if n == name:
                return obj.getn

    else:
        raise ENOSTATS(name)


def stats--- This code section failed: ---

 L. 106         0  LOAD_FAST                'event'
                2  LOAD_ATTR                args
                4  STORE_FAST               'args'

 L. 107         6  LOAD_STR                 'Sinds %s\n'
                8  LOAD_GLOBAL              time
               10  LOAD_METHOD              ctime
               12  LOAD_GLOBAL              starttime
               14  CALL_METHOD_1         1  ''
               16  BINARY_MODULO    
               18  STORE_FAST               'txt'

 L. 108        20  LOAD_GLOBAL              time
               22  LOAD_METHOD              time
               24  CALL_METHOD_0         0  ''
               26  LOAD_GLOBAL              starttime
               28  BINARY_SUBTRACT  
               30  STORE_FAST               'delta'

 L. 109        32  LOAD_GLOBAL              wanted
               34  LOAD_METHOD              items
               36  CALL_METHOD_0         0  ''
               38  GET_ITER         
               40  FOR_ITER            290  'to 290'
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'name'
               46  STORE_FAST               'obj'

 L. 110        48  LOAD_FAST                'obj'
               50  LOAD_METHOD              items
               52  CALL_METHOD_0         0  ''
               54  GET_ITER         
               56  FOR_ITER            288  'to 288'
               58  UNPACK_SEQUENCE_2     2 
               60  STORE_FAST               'key'
               62  STORE_FAST               'val'

 L. 111        64  SETUP_FINALLY        82  'to 82'

 L. 112        66  LOAD_GLOBAL              seconds
               68  LOAD_GLOBAL              nr
               70  LOAD_FAST                'key'
               72  CALL_FUNCTION_1       1  ''
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'needed'
               78  POP_BLOCK        
               80  JUMP_FORWARD        108  'to 108'
             82_0  COME_FROM_FINALLY    64  '64'

 L. 113        82  DUP_TOP          
               84  LOAD_GLOBAL              ENOSTATS
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   106  'to 106'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 114        96  POP_EXCEPT       
               98  POP_TOP          
              100  POP_TOP          
              102  LOAD_CONST               None
              104  RETURN_VALUE     
            106_0  COME_FROM            88  '88'
              106  END_FINALLY      
            108_0  COME_FROM            80  '80'

 L. 115       108  LOAD_FAST                'key'
              110  STORE_FAST               'name'

 L. 116       112  LOAD_GLOBAL              int
              114  LOAD_FAST                'delta'
              116  LOAD_FAST                'needed'
              118  BINARY_TRUE_DIVIDE
              120  CALL_FUNCTION_1       1  ''
              122  STORE_FAST               'nrtimes'

 L. 117       124  LOAD_STR                 '%s #%s'
              126  LOAD_FAST                'name'
              128  LOAD_METHOD              upper
              130  CALL_METHOD_0         0  ''
              132  LOAD_FAST                'nrtimes'
              134  BUILD_TUPLE_2         2 
              136  BINARY_MODULO    
              138  STORE_FAST               'txt'

 L. 118       140  LOAD_FAST                'name'
              142  LOAD_GLOBAL              omschrijving
              144  COMPARE_OP               in
              146  POP_JUMP_IF_FALSE   166  'to 166'

 L. 119       148  LOAD_FAST                'txt'
              150  LOAD_STR                 ' (%s)'
              152  LOAD_GLOBAL              omschrijving
              154  LOAD_METHOD              get
              156  LOAD_FAST                'name'
              158  CALL_METHOD_1         1  ''
              160  BINARY_MODULO    
              162  INPLACE_ADD      
              164  STORE_FAST               'txt'
            166_0  COME_FROM           146  '146'

 L. 120       166  LOAD_FAST                'txt'
              168  LOAD_STR                 ' elke %s'
              170  LOAD_GLOBAL              lo
              172  LOAD_ATTR                tms
              174  LOAD_METHOD              elapsed
              176  LOAD_GLOBAL              seconds
              178  LOAD_GLOBAL              nr
              180  LOAD_FAST                'name'
              182  CALL_FUNCTION_1       1  ''
              184  CALL_FUNCTION_1       1  ''
              186  CALL_METHOD_1         1  ''
              188  BINARY_MODULO    
              190  INPLACE_ADD      
              192  STORE_FAST               'txt'

 L. 121       194  LOAD_FAST                'name'
              196  LOAD_GLOBAL              urls
              198  COMPARE_OP               in
              200  POP_JUMP_IF_FALSE   220  'to 220'

 L. 122       202  LOAD_FAST                'txt'
              204  LOAD_STR                 ' - %s'
              206  LOAD_GLOBAL              urls
              208  LOAD_METHOD              get
              210  LOAD_FAST                'name'
              212  CALL_METHOD_1         1  ''
              214  BINARY_MODULO    
              216  INPLACE_ADD      
              218  STORE_FAST               'txt'
            220_0  COME_FROM           200  '200'

 L. 123       220  LOAD_FAST                'name'
              222  LOAD_GLOBAL              tags
              224  COMPARE_OP               in
              226  POP_JUMP_IF_FALSE   248  'to 248'

 L. 124       228  LOAD_FAST                'txt'
              230  LOAD_STR                 ' %s'
              232  LOAD_GLOBAL              tags
              234  LOAD_METHOD              get
              236  LOAD_FAST                'name'
              238  CALL_METHOD_1         1  ''
              240  BINARY_MODULO    
              242  INPLACE_ADD      
              244  STORE_FAST               'txt'
              246  JUMP_FORWARD        274  'to 274'
            248_0  COME_FROM           226  '226'

 L. 126       248  LOAD_FAST                'txt'
              250  LOAD_STR                 ' %s'
              252  LOAD_GLOBAL              random
              254  LOAD_METHOD              choice
              256  LOAD_GLOBAL              list
              258  LOAD_GLOBAL              tags
              260  LOAD_METHOD              values
              262  CALL_METHOD_0         0  ''
              264  CALL_FUNCTION_1       1  ''
              266  CALL_METHOD_1         1  ''
              268  BINARY_MODULO    
              270  INPLACE_ADD      
              272  STORE_FAST               'txt'
            274_0  COME_FROM           246  '246'

 L. 127       274  LOAD_GLOBAL              k
              276  LOAD_ATTR                fleet
              278  LOAD_METHOD              announce
              280  LOAD_FAST                'txt'
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          
              286  JUMP_BACK            56  'to 56'
              288  JUMP_BACK            40  'to 40'

Parse error at or near `POP_TOP' instruction at offset 100


def stat(event, **kwargs):
    name = event.rest or 'suicide'
    if '.' in name:
        name = name.split'.'[(-1)]
    name = name.lower()
    delta = time.time() - starttime
    awake = time.time() - today
    try:
        needed = seconds(nr(name))
    except ENOSTATS:
        return
    else:
        if needed:
            nrtimes = int(delta / needed)
            txt = '%s #%s' % (name.upper(), nrtimes)
            if name in omschrijving:
                txt += ' (%s)' % omschrijving.getname
            else:
                txt += ' elke %s' % lo.tms.elapsedseconds(nr(name))
                if name in urls:
                    txt += ' - %s' % urls.getname
                if name in tags:
                    txt += ' %s' % tags.getname
                else:
                    txt += ' %s' % random.choicelist(tags.values())
            k.fleet.announcetxt


oorzaak = lo.Object()
oorzaak.suicide = 1800
oorzaak.psychosestoornis = 12000
nrsec = lo.Object()
nrsec.dag = 86400.0
nrsec.jaar = 365 * nrsec.dag
nrsec.weekend = 173274.7252747253
nrsec.avond = 57600.0
times = lo.Object()
times.weekend = 173274.7252747253
times.avond = 57600.0
times.dag = 86400.0
times.jaar = 31536000.0
rechter = lo.Object()
rechter.ibs = 8861
rechter.rm = 17746
rechter.vwm = 6657
rechter.mvv = 4431
rechter.vm = 6690
rechter.mev = 65
rechter.zm = 3
suicidejaar = lo.Object()
suicidejaar.y2008 = 1435
suicidejaar.y2009 = 1525
suicidejaar.y2010 = 1600
suicidejaar.y2011 = 1647
suicidejaar.y2012 = 1753
suicidejaar.y2013 = 1857
suicidejaar.y2014 = 1839
suicidejaar.y2015 = 1871
suicidejaar.y2016 = 1894
suicidejaar.y2017 = 1917
ziekenhuis = lo.Object()
ziekenhuis.y2010 = 7800
ziekenhuis.y2011 = 9600
ziekenhuis.y2012 = 9200
ziekenhuis.y2013 = 8300
ziekenhuis.y2014 = 8500
seh = lo.Object()
seh.y2010 = 13700
seh.y2011 = 16000
seh.y2012 = 15800
seh.y2013 = 13300
seh.y2014 = 14000
e33 = lo.Object()
e33.melding = 61000
cijfers = lo.Object()
cijfers.melding = 61000
cijfers.opnames = 24338
cijfers.crisis = 150000
cijfers.oordeel = 150000
cijfers.pogingen = 94000
cijfers.incidenten = 66000
cijfers.poh = 1300000
cijfers.vergiftigingen = 25262
cijfers.overlast = 18000
cijfers.insluiting = 240000
cijfers.aangiftes = 134000
cijfers.suicide = 1871
cijfers.burenoverlast = 12000
cijfers.uitzetting = 5900
cijfers.volwassendoop = 500
cijfers.tumor = 12000
cijfers.detox = 65654
cijfers.acuut = 8000
cijfers.spoedeisendpoging = 14000
cijfers.weguitkliniek = 2539
cijfers.bewindvoering = 295000
cijfers.suicidegedachtes = 410000
cijfers.psychosestoornis = 13076
cijfers.oorzaak = cijfers.psychosestoornis + cijfers.suicide
oordeel = lo.Object()
oordeel.verwijs = cijfers.crisis * 0.85
oordeel.uitstroom = cijfers.crisis * 0.05
oordeel.opname = cijfers.crisis * 0.1
alarm = lo.Object()
alarm.politie = 0.3 * cijfers.crisis
alarm.hap = 0.4 * cijfers.crisis
alarm.keten = 0.3 * cijfers.crisis
suicide = lo.Object()
suicide.suicide = suicidejaar.y2017
pogingen = lo.Object()
pogingen.pogingen = cijfers.pogingen
poging = lo.Object()
poging.ziekenhuis = ziekenhuis.y2014
poging.seh = seh.y2014
drugs = lo.Object()
drugs.speed = 20000
drugs.cocaine = 50000
drugs.alcohol = 400000
drugs.wiet = 500000
medicijnen = lo.Object()
medicijnen.amitriptyline = 189137
medicijnen.paroxetine = 186028
medicijnen.citalopram = 154620
medicijnen.oxazepam = 133608
medicijnen.venlafaxine = 112000
medicijnen.mirtazapine = 110742
medicijnen.quetiapine = 84414
medicijnen.diazepam = 72000
medicijnen.sertraline = 68000
medicijnen.haloperidol = 59825
dbc = lo.Object()
dbc.middelgebondenstoornissen = 33060
dbc.somatoformestoornissen = 21841
dbc.cognitievestoornissen = 25717
dbc.angststoornissen = 54458
dbc.aanpassingsstoornissen = 43079
dbc.depressievestoornissen = 102361
dbc.eetstoornissen = 8688
dbc.restgroepdiagnose = 16996
dbc.ontbrekendeprimairediagnose = 3030
dbc.andereproblemenredenvoorzorg = 49286
dbc.schizofrenieenanderepsychotischestoornissen = 6798
dbc.bipolairestoornissen = 3569
dbc.posttraumatischestressstoornis = 24716
dbc.persoonlijkheidsstoornissen = 36574
dbc.adhd = 25951
dbc.gedrag = 1176
dbc.kindertijdoverig = 1035
dbc.autismespectrum = 9436
halfwaarde = lo.Object()
halfwaarde.zyprexa = 30
halfwaarde.abilify = 75
halfwaarde.haldol = 30
halfwaarde.alprazolam = 11
halfwaarde.orap = 55
halfwaarde.paracetamol = 2.5
halfwaarde.lorazepam = 12
halfwaarde.paroxetine = 21
halfwaarde.citalopram = 35
halfwaarde.oxazepam = 8.2
halfwaarde.quetiapine = 6
halfwaarde.diazepam = 100
halfwaarde.wiet = 7
perdag = lo.Object()
perdag.medicijnen = medicijnen
perdag.drugs = drugs
tags = lo.Object()
tags.keten = '#burgemeester'
tags.politie = '#broodjepindakaas'
tags.hap = '#triagetrien'
tags.verwijs = '#maandagweer'
tags.uitstroom = '#zorgwekkend'
tags.opname = '#meermedicijn'
tags.crisis = '#triade'
tags.suicide = '#wetverplichteggz'
tags.pogingen = '#prettigweekend'
tags.incidenten = '#jammerdan'
tags.acuut = '#geenbedvoorjou'
tags.zorgmijder = '#helaas'
tags.inwoners = '#gebodenvrucht'
tags.crisis = '#medicijnen'
tags.alarm = '#telaat'
tags.oordeel = '#geencrisis'
tags.vergiftigingen = '#overduur'
tags.neurotoxisch = '#overdosis'
tags.schizofrenie = '#gifmedicijn'
tags.angst = '#gifmedicijn'
tags.depressie = '#gifmedicijn'
tags.meds = '#gifmedicijn'
tags.ibs = '#overlast'
tags.rm = '#benadeling'
tags.vwm = '#maatregel'
tags.vm = '#nogeven'
tags.mvv = '#direct!!'
tags.mev = '#kieserzelfvoor'
tags.om = '#ffkijken#'
tags.zm = '#zelfwat?'
omschrijving = lo.Object()
omschrijving.ibs = 'inbewaringstelling'
omschrijving.rm = 'rechterlijke machtiging'
omschrijving.vm = 'voorlopige rechterlijke machtiging'
omschrijving.mvv = 'machtiging voortgezet verblijf'
omschrijving.vwm = 'voorwaardelijke rechterlijke machtiging'
omschrijving.mev = 'machtiging eigen verzoek'
omschrijving.zm = 'zelfbinding machtiging'
omschrijving.om = 'observatie machtiging'
omschrijving.keten = 'ggz besluit tot crisisbeoordeling'
omschrijving.politie = 'politie vraagt om crisisbeoordeling'
omschrijving.hap = 'huisartsenpost vraagt om crisisbeoordeeling'
omschrijving.verwijs = 'crisisdienst maakt vervolg afspraak'
omschrijving.uitstroom = 'crisisdienst maakt geen vervolgafspraak'
omschrijving.opname = 'niet meten, maar off-label tot "therapeutische" werking'
omschrijving.suicide = 'behandelplan is niet op te vragen'
omschrijving.pogingen = 'suicide poging is mislukt'
omschrijving.weekend = 'niet bereikbaar tot maandag'
omschrijving.avond = 'wachten tot de volgende ochtend'
omschrijving.incidenten = 'code 33 gemeld bij politie - overlast veroorzaakt door gestoord/overspannen persoon'
omschrijving.acuut = 'spoedeisende psychiatrische hulp ingeschakeld'
omschrijving.zorgmijder = 'patient durft geen zorg meer te ontvangen'
omschrijving.inwoners = '5% van de nederlanders heeft GGZ problemen'
omschrijving.crisis = 'situatie is dusdanig dat men vraagt om een crisisbeoordeling'
omschrijving.alarm = 'opschaling van zorg NA de crisis'
omschrijving.oordeel = 'brengt patient aan voor beoordeling'
omschrijving.vergiftigingen = 'opgestapelde werking van giftige medicijnen'
omschrijving.neurotoxisch = '2 maanden zyprexa is genoeg'
omschrijving.speed = 'speed gebruikt'
omschrijving.cocaine = 'cocaine gebruikt'
omschrijving.alcohol = 'alcohol gedronken'
omschrijving.wiet = 'wietje gerookt'
omschrijving.antipsychotica = 'antipsychotica ingenomen'
omschrijving.antidepresiva = 'antidepressiva ingenomen'
omschrijving.slaapmiddel = 'slaapmiddel ingenomen'
omschrijving.ambulant = 'patient/behandelaar contact'
omschrijving.verslaving = 'diagnose verslaving'
omschrijving.schizofrenie = 'diagnose schizofrenie'
omschrijving.depressie = 'depressieve patient'
omschrijving.amitriptyline = 'depressie'
omschrijving.paroxetine = 'antipsychotica'
omschrijving.citalopram = 'sedatie'
omschrijving.oxazepam = 'sedatie'
omschrijving.venlafaxine = 'depressie'
omschrijving.mirtazapine = 'depressie'
omschrijving.quetiapine = 'antipschotica'
omschrijving.diazepam = 'sedatie'
omschrijving.sertraline = 'depressie'
omschrijving.haloperidol = 'antipsyochotica'
omschrijving.verslaafden = 'diagnose verslaving'
omschrijving.inwoners = 'koningrijk der nederlanden'
omschrijving.arbeidshandicap = 'volledig afgekeurd'
omschrijving.huisartsen = 'praktijkhouder in nederland'
omschrijving.opnames = 'opgenomen in ziekenhuis'
omschrijving.zorgmijder = 'zorgontwijker'
omschrijving.middelgebondenstoornissen = 'drugverslaving'
omschrijving.somatoformestoornissen = 'lichamelijke klachten heeft waarvoor geen somatische oorzaak (lichamelijke ziekte) gevonden is'
omschrijving.cognitievestoornissen = 'waarnemingsvermogen is verstoord'
omschrijving.angststoornissen = 'fobien en sociaal niet meer kunnen functioneren'
omschrijving.aanpassingsstoornissen = 'karakterstoornis, men is al te gevormd'
omschrijving.depressievestoornissen = 'somberheid troef'
omschrijving.eetstoornissen = 'vreetkicks, bolimia, anorexia'
omschrijving.restgroepdiagnose = 'niet anders vernoemd, valt niet in een standaard diagnose'
omschrijving.ontbrekendeprimairediagnose = 'geen duidelijke diagnose te stellen'
omschrijving.andereproblemenredenvoorzorg = 'niet in standaard zorg te plaatsen'
omschrijving.schizofrenieenanderepsychotischestoornissen = 'stemmen horen, waan denkbeelden'
omschrijving.bipolairestoornissen = 'stemmingswisselingen'
omschrijving.posttraumatischestressstoornis = 'stress na trauma'
omschrijving.persoonlijkheidsstoornissen = 'aanpassings problemen'
omschrijving.adhd = 'te druk, te veel energie'
omschrijving.gedrag = 'moelijk opvoedbaar'
omschrijving.kindertijdoverig = 'vroegtijdig trauma'
omschrijving.autismespectrum = 'valt in een autisme categorie'
omschrijving.seh = 'spoedeisende hulp'
omschrijving.psychosestoornis = 'een door de psychose zelf overleden persoon'
omschrijving.oorzaak = 'oorzaak van overlijden'
urls = lo.Object()
urls.ibs = 'http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf'
urls.rm = 'http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf'
urls.vm = 'http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf'
urls.mvv = 'http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf'
urls.vw = 'http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf'
urls.mev = 'http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf'
urls.zb = 'http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf'
urls.ob = 'http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf'
urls.zm = 'http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf'
urls.iatrogeen = 'https://www.nrc.nl/nieuws/2011/04/22/eenvijfde-van-de-opnames-te-wijten-aan-medicijnen-12012115-a426225'
urls.opname = 'http://www.tijdschriftvoorpsychiatrie.nl/issues/434/articles/8318'
urls.crisis = 'http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html'
urls.tuchtrecht = 'http://tuchtrecht.overheid.nl/zoeken/resultaat/uitspraak/2014/ECLI_NL_TGZRAMS_2014_94?zaaknummer=2013%2F221&Pagina=1&ItemIndex=1'
urls.suicide = 'http://www.cbs.nl/nl-NL/menu/themas/bevolking/publicaties/artikelen/archief/2014/2014-4204-wm.htm'
urls.incident = 'https://www.wodc.nl/onderzoeksdatabase/2337-de-effectiviteit-van-de-politiele-taakuitvoering-en-de-taken-en-verantwoordelijkheden-van-andere-partijen.aspx'
urls.zorgmijder = 'http://www.gezondheidsraad.nl/sites/default/files/samenvatting_noodgedwongen_0.pdf'
urls.acuut = 'http://www.gezondheidsraad.nl/sites/default/files/samenvatting_noodgedwongen_0.pdf'
urls.wvggz = 'https://www.dwangindezorg.nl/de-toekomst/wetsvoorstellen/wet-verplichte-geestelijke-gezondheidszorg'
urls.politie = 'http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html'
urls.hap = 'http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html'
urls.keten = 'http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html'
urls.verwijs = 'http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html'
urls.uitstroom = 'http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html'
urls.opnames = 'http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html'
urls.vergifitigingen = 'http://www.umcutrecht.nl/getmedia/f9f152e2-8638-4ffc-a05f-fce72f5f416a/NVIC-Jaaroverzicht-2014.pdf.aspx?ext=.pdf'
urls.neurotoxisch = 'http://www.umcutrecht.nl/getmedia/f9f152e2-8638-4ffc-a05f-fce72f5f416a/NVIC-Jaaroverzicht-2014.pdf.aspx?ext=.pdf'
urls.incidenten = 'http://www.dsp-groep.nl/userfiles/file/Politie%20en%20verwarde%20personen%20_DSP-groep.pdf'
urls.ambulant = 'https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/'
urls.verslaving = 'https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/'
urls.poh = 'https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/'
urls.meds = 'https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/'
urls.depressie = 'https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/'
urls.angst = 'https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/'
urls.schizofrenie = 'https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/'
urls.detox = 'https://www.jellinek.nl/vraag-antwoord/hoeveel-mensen-zijn-verslaafd-en-hoeveel-zijn-er-in-behandeling/'
urls.verslaafden = 'https://www.jellinek.nl/vraag-antwoord/hoeveel-mensen-zijn-verslaafd-en-hoeveel-zijn-er-in-behandeling/'
urls.volwassendoop = ''
urls.arbeidshandicap = 'http://www.nationalezorggids.nl/gehandicaptenzorg/nieuws/27841-ruim-100-000-mensen-op-sociale-werkplaats.html'
urls.overlast = 'http://nos.nl/artikel/2075227-verwarde-huurders-veroorzaken-steeds-meer-overlast.html'
urls.insluiting = 'http://www.tweedekamer.nl/downloads/document?id=78ee0f32-7487-4bcc-ba01-e01ace2bc4b4&title=Arrestantenzorg%20Nederland%20Landelijke%20rapportage.pdf'
urls.zyprexa = 'http://www.ema.europa.eu/docs/nl_NL/document_library/EPAR_-_Product_Information/human/000287/WC500055611.pdf'
urls.factor = 'http://nos.nl/artikel/2090676-aantal-incidenten-met-verwarde-mensen-flink-onderschat.html'
urls.dbc = 'https://www.nza.nl/1048076/1048181/Marktscan_ggz_2014_deel_B_en_beleidsbrief.pdf'
urls.dbs2015 = 'https://www.rijksoverheid.nl/documenten/rapporten/2016/05/25/marktscan-ggz'
urls.medicijnen = 'https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/geestelijke-gezondheidszorg/row-5/welke-geneesmiddelen-worden-het-meest-voorgeschreven-in-de-ggz/'
urls.pogingen = 'http://www.nfzp.nl/wp/wp-content/uploads/2010/09/Einddocument-AF0943-Kwaliteitsdcoument-Ketenzorg-bij-Suicidaliteit.pdf'
urls.suicidegedachte = 'http://www.nfzp.nl/wp/wp-content/uploads/2010/09/Einddocument-AF0943-Kwaliteitsdcoument-Ketenzorg-bij-Suicidaliteit.pdf'
urls.ziekenhuisopnames = 'https://www.tweedekamer.nl/kamerstukken/detail?id=2016D13371&did=2016D13371'
urls.seh = 'https://www.tweedekamer.nl/kamerstukken/detail?id=2016D13371&did=2016D13371'
urls.epa = 'https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/ernstige-psychiatrische-aandoeningen/'
urls.rechter = 'https://www.ggdghorkennisnet.nl/?file=43865&m=1541606110&action=file.download'
urls.psychosestoornis = 'https://www.volksgezondheidenzorg.info/echi-indicators/mortality#node-disease-specific-mortality'
soort = lo.Object()
soort.alarm = 'patient'
soort.oordeel = 'arts'
soort.neurotoxisch = 'patient'
soort.angst = 'patient'
soort.depressie = 'patient'
soort.schizofrenie = 'patient'
soort.ibs = 'burgemeester'
soort.rm = 'civiele rechter'
soort.vm = 'civiele rechter'
soort.mvv = 'civiele rechter'
soort.vwm = 'civiele rechter'
soort.ev = 'civiele rechter'
soort.om = 'civiele rechter'
soort.zm = 'civiele rechter'
soort.politie = 'agent'
soort.hap = 'huisarts'
soort.keten = 'spv/psychiater'
soort.verwijs = 'crisisdienst'
soort.uitstroom = 'eigen behandelaar'
soort.suicide = 'slachtoffer'
soort.crisis = 'burger'
soort.pogingen = 'wanhopige patient'
soort.incidenten = 'hulproepende patient'
soort.acuut = 'vergiftigde patient'
soort.meds = 'toegediende patient'
soort.amitriptyline = 'patient'
soort.paroxetine = 'patient'
soort.citalopram = 'patient'
soort.oxazepam = 'patient'
soort.venlafaxine = 'patient'
soort.mirtazapine = 'patient'
soort.quetiapine = 'patient'
soort.diazepam = 'patient'
soort.sertrali = 'patient'
soort.haloperidol = 'patient'
soort.insluiting = 'politie'
soort.ambulant = 'casemanager'
soort.verslaafden = 'gebruiker'
soort.slaapmiddel = 'insomnia patient'
wanted = lo.Object()
wanted.oorzaak = oorzaak
wanted.pogingen = pogingen
demo = lo.Object()
demo.dbc = dbc
demo.medicijnen = medicijnen
demo.drugs = drugs