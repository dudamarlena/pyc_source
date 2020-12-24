# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/vbp/ucod/united_states.py
# Compiled at: 2019-04-28 23:48:05
# Size of source mod 2**32: 57189 bytes
import os, sys, vbp, enum, glob, math, numpy, scipy, pandas, pprint, zipfile, argparse, datetime, traceback, matplotlib, vbp.ucod.icd, urllib.request, matplotlib.pyplot, statsmodels.tools, statsmodels.tsa.api, matplotlib.offsetbox, statsmodels.stats.api, statsmodels.formula.api, statsmodels.stats.diagnostic, statsmodels.tools.eval_measures
from vbp import DictTree
from vbp.ucod.icd import ICD

class DataType(vbp.DataSourceDataType):
    US_ICD_113_SELECTED_CAUSES_ALL = enum.auto()
    US_ICD_113_SELECTED_CAUSES_LEAVES = enum.auto()
    US_ICD_113_SELECTED_CAUSES_ROOTS = enum.auto()
    US_ICD10_CHAPTERS = enum.auto()
    US_ICD10_SUB_CHAPTERS = enum.auto()
    US_ICD10_MINIMALLY_GROUPED = enum.auto()
    US_ICD_LONGTERM_COMPARABLE_LEADING = enum.auto()


class UCODUnitedStates(vbp.ucod.icd.ICDDataSource):
    mortality_uspopulation_years = list(range(1900, 2018))
    mortality_uspopulation_per_year = [
     19965446, 20237453, 20582907, 20943223, 21332076, 21767980, 33782288, 34552837, 38634758, 44223513,
     47470437, 53929644, 54847700, 58156738, 60963307, 61894847, 66971177, 70234775, 79008411, 83157982,
     86079263, 87814447, 92702899, 96788196, 99318098, 102031554, 103822682, 107084531, 113636159, 115317449,
     117238278, 118148987, 118903899, 125578763, 126373773, 127250232, 128053180, 128824829, 129824939, 130879718,
     131669275, 133121000, 133920000, 134245000, 132885000, 132481000, 140054000, 143446000, 146093000, 148665000,
     150697361, 153310000, 155687000, 158242000, 161164000, 164308000, 167306000, 170371000, 173320000, 176513000,
     179323175, 182992000, 185771000, 188483000, 191141000, 193526000, 195576000, 197457000, 199399000, 201385000,
     203211926, 206827000, 209284000, 211357000, 213342000, 215465000, 217563000, 219760000, 222095000, 224567000,
     226545805, 229466000, 231664000, 233792000, 235825000, 237924000, 240133000, 242289000, 244499000, 246819000,
     248709873, 252177000, 255077536, 257783004, 260340990, 262755270, 265283783, 267636061, 270248003, 279040168,
     281421906, 284968955, 287625193, 290107933, 292805298, 295516599, 298379912, 301231207, 304093966, 306771529,
     308745538, 311591917, 313914040, 316128839, 318857056, 321418820, 323127513, 325719178]
    mortality_icd_revision = [
     5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
     5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
     5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
     5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
     5, 5, 5, 5, 5, 5, 5, 5, 5, 6,
     6, 6, 6, 6, 6, 6, 6, 6, 7, 7,
     7, 7, 7, 7, 7, 7, 7, 7, 8, 8,
     8, 8, 8, 8, 8, 8, 8, 8, 8, 9,
     9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
     9, 9, 9, 9, 9, 9, 9, 9, 9, 10,
     10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
     10, 10, 10, 10, 10, 10, 10, 10]
    mortality_uspopulation = pandas.DataFrame({'Population':mortality_uspopulation_per_year, 
     'ICDRevision':mortality_icd_revision},
      index=mortality_uspopulation_years)
    icd10_ucod113 = DictTree({1:'Salmonella infections (A01-A02)', 
     2:'Shigellosis and amebiasis (A03,A06)', 
     3:'Certain other intestinal infections (A04,A07-A09)', 
     4:DictTree(value='Tuberculosis (A16-A19)', d={5:'Respiratory tuberculosis (A16)', 
      6:'Other tuberculosis (A17-A19)'}), 
     7:'Whooping cough (A37)', 
     8:'Scarlet fever and erysipelas (A38,A46)', 
     9:'Meningococcal infection (A39)', 
     10:'Septicemia (A40-A41)', 
     11:'Syphilis (A50-A53)', 
     12:'Acute poliomyelitis (A80)', 
     13:'Arthropod-borne viral encephalitis (A83-A84,A85.2)', 
     14:'Measles (B05)', 
     15:'Viral hepatitis (B15-B19)', 
     16:'Human immunodeficiency virus (HIV) disease (B20-B24)', 
     17:'Malaria (B50-B54)', 
     18:'Other and unspecified infectious and parasitic diseases and their sequelae (A00,A05,A20-A36,A42-A44,A48-A49,A54-A79,A81-A82,A85.0-A85.1,A85.8,A86-B04,B06-B09,B25-B49,B55-B99)', 
     19:DictTree(value='Malignant neoplasms (C00-C97)', d={20:'Malignant neoplasms of lip, oral cavity and pharynx (C00-C14)', 
      21:'Malignant neoplasm of esophagus (C15)', 
      22:'Malignant neoplasm of stomach (C16)', 
      23:'Malignant neoplasms of colon, rectum and anus (C18-C21)', 
      24:'Malignant neoplasms of liver and intrahepatic bile ducts (C22)', 
      25:'Malignant neoplasm of pancreas (C25)', 
      26:'Malignant neoplasm of larynx (C32)', 
      27:'Malignant neoplasms of trachea, bronchus and lung (C33-C34)', 
      28:'Malignant melanoma of skin (C43)', 
      29:'Malignant neoplasm of breast (C50)', 
      30:'Malignant neoplasm of cervix uteri (C53)', 
      31:'Malignant neoplasms of corpus uteri and uterus, part unspecified (C54-C55)', 
      32:'Malignant neoplasm of ovary (C56)', 
      33:'Malignant neoplasm of prostate (C61)', 
      34:'Malignant neoplasms of kidney and renal pelvis (C64-C65)', 
      35:'Malignant neoplasm of bladder (C67)', 
      36:'Malignant neoplasms of meninges, brain and other parts of central nervous system (C70-C72)', 
      37:DictTree(value='Malignant neoplasms of lymphoid, hematopoietic and related tissue (C81-C96)', d={38:"Hodgkin's disease (C81)", 
       39:"Non-Hodgkin's lymphoma (C82-C85)", 
       40:'Leukemia (C91-C95)', 
       41:'Multiple myeloma and immunoproliferative neoplasms (C88,C90)', 
       42:'Other and unspecified malignant neoplasms of lymphoid, hematopoietic and related tissue (C96)'}), 
      43:'All other and unspecified malignant neoplasms (C17,C23-C24,C26-C31,C37-C41,C44-C49,C51-C52,C57-C60,C62-C63,C66,C68-C69,C73-C80,C97)'}), 
     44:'In situ neoplasms, benign neoplasms and neoplasms of uncertain or unknown behavior (D00-D48)', 
     45:'Anemias (D50-D64)', 
     46:'Diabetes mellitus (E10-E14)', 
     47:DictTree(value='Nutritional deficiencies (E40-E64)', d={48:'Malnutrition (E40-E46)', 
      49:'Other nutritional deficiencies (E50-E64)'}), 
     50:'Meningitis (G00,G03)', 
     51:"Parkinson's disease (G20-G21)", 
     52:"Alzheimer's disease (G30)", 
     53:DictTree(value='Major cardiovascular diseases (I00-I78)', d={54:DictTree(value='Diseases of heart (I00-I09,I11,I13,I20-I51)', d={55:'Acute rheumatic fever and chronic rheumatic heart diseases (I00-I09)', 
       56:'Hypertensive heart disease (I11)', 
       57:'Hypertensive heart and renal disease (I13)', 
       58:'Ischemic heart diseases (I20-I25)', 
       59:'Acute myocardial infarction (I21-I22)', 
       60:'Other acute ischemic heart diseases (I24)', 
       61:DictTree(value='Other forms of chronic ischemic heart disease (I20,I25)', d={62:'Atherosclerotic cardiovascular disease, so described (I25.0)', 
        63:'All other forms of chronic ischemic heart disease (I20,I25.1-I25.9)'}), 
       64:DictTree(value='Other heart diseases (I26-I51)', d={65:'Acute and subacute endocarditis (I33)', 
        66:'Diseases of pericardium and acute myocarditis (I30-I31,I40)', 
        67:'Heart failure (I50)', 
        68:'All other forms of heart disease (I26-I28,I34-I38,I42-I49,I51)'})}), 
      69:'Essential (primary) hypertension and hypertensive renal disease (I10,I12,I15)', 
      70:'Cerebrovascular diseases (I60-I69)', 
      71:'Atherosclerosis (I70)', 
      72:DictTree(value='Other diseases of circulatory system (I71-I78)', d={73:'Aortic aneurysm and dissection (I71)', 
       74:'Other diseases of arteries, arterioles and capillaries (I72-I78)'})}), 
     75:'Other disorders of circulatory system (I80-I99)', 
     76:DictTree(value='Influenza and pneumonia (J09-J18)', d={77:'Influenza (J09-J11)', 
      78:'Pneumonia (J12-J18)'}), 
     79:DictTree(value='Other acute lower respiratory infections (J20-J22,U04)', d={80:'Acute bronchitis and bronchiolitis (J20-J21)', 
      81:'Other and unspecified acute lower respiratory infection (J22,U04)'}), 
     82:DictTree(value='Chronic lower respiratory diseases (J40-J47)', d={83:'Bronchitis, chronic and unspecified (J40-J42)', 
      84:'Emphysema (J43)', 
      85:'Asthma (J45-J46)', 
      86:'Other chronic lower respiratory diseases (J44,J47)'}), 
     87:'Pneumoconioses and chemical effects (J60-J66,J68)', 
     88:'Pneumonitis due to solids and liquids (J69)', 
     89:'Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98)', 
     90:'Peptic ulcer (K25-K28)', 
     91:'Diseases of appendix (K35-K38)', 
     92:'Hernia (K40-K46)', 
     93:DictTree(value='Chronic liver disease and cirrhosis (K70,K73-K74)', d={94:'Alcoholic liver disease (K70)', 
      95:'Other chronic liver disease and cirrhosis (K73-K74)'}), 
     96:'Cholelithiasis and other disorders of gallbladder (K80-K82)', 
     97:DictTree(value='Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27)', d={98:'Acute and rapidly progressive nephritic and nephrotic syndrome (N00-N01,N04)', 
      99:'Chronic glomerulonephritis, nephritis and nephropathy not specified as acute or chronic, and renal sclerosis unspecified (N02-N03,N05-N07,N26)', 
      100:'Renal failure (N17-N19)', 
      101:'Other disorders of kidney (N25,N27)', 
      102:'Infections of kidney (N10-N12,N13.6,N15.1)'}), 
     103:'Hyperplasia of prostate (N40)', 
     104:'Inflammatory diseases of female pelvic organs (N70-N76)', 
     105:DictTree(value='Pregnancy, childbirth and the puerperium (O00-O99)', d={106:'Pregnancy with abortive outcome (O00-O07)', 
      107:'Other complications of pregnancy, childbirth and the puerperium (O10-O99)'}), 
     108:'Certain conditions originating in the perinatal period (P00-P96)', 
     109:'Congenital malformations, deformations and chromosomal abnormalities (Q00-Q99)', 
     110:'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99)', 
     111:'All other diseases (Residual) (NaN)', 
     112:DictTree(value='Accidents (unintentional injuries) (V01-X59,Y85-Y86)', d={113:'Transport accidents (V01-V99,Y85)', 
      114:'Motor vehicle accidents (V02-V04,V09.0,V09.2,V12-V14,V19.0-V19.2,V19.4-V19.6,V20-V79,V80.3-V80.5,V81.0-V81.1,V82.0-V82.1,V83-V86, V87.0-V87.8,V88.0-V88.8,V89.0,V89.2)', 
      115:'Other land transport accidents (V01,V05-V06,V09.1,V09.3-V09.9, V10-V11,V15-V18,V19.3,V19.8-V19.9,V80.0-V80.2,V80.6-V80.9,V81.2-V81.9,V82.2-V82.9,V87.9,V88.9,V89.1,V89.3,V89.9)', 
      116:'Water, air and space, and other and unspecified transport accidents and their sequelae (V90-V99,Y85)', 
      117:'Nontransport accidents (W00-X59,Y86)', 
      118:'Falls (W00-W19)', 
      119:'Accidental discharge of firearms (W32-W34)', 
      120:'Accidental drowning and submersion (W65-W74)', 
      121:'Accidental exposure to smoke, fire and flames (X00-X09)', 
      122:'Accidental poisoning and exposure to noxious substances (X40-X49)', 
      123:'Other and unspecified nontransport accidents and their sequelae (W20-W31,W35-W64,W75-W99,X10-X39,X50-X59,Y86)'}), 
     124:DictTree(value='Intentional self-harm (suicide) (*U03,X60-X84,Y87.0)', d={125:'Intentional self-harm (suicide) by discharge of firearms (X72-X74)', 
      126:'Intentional self-harm (suicide) by other and unspecified means and their sequelae (*U03,X60-X71,X75-X84,Y87.0)'}), 
     127:DictTree(value='Assault (homicide) (*U01-*U02,X85-Y09,Y87.1)', d={128:'Assault (homicide) by discharge of firearms (*U01.4,X93-X95)', 
      129:'Assault (homicide) by other and unspecified means and their sequelae (*U01.0-*U01.3,*U01.5-*U01.9,*U02,X85-X92,X96-Y09,Y87.1)'}), 
     130:'Legal intervention (Y35,Y89.0)', 
     131:'Events of undetermined intent (Y10-Y34,Y87.2,Y89.9)', 
     132:'Discharge of firearms, undetermined intent (Y22-Y24)', 
     133:'Other and unspecified events of undetermined intent and their sequelae (Y10-Y21,Y25-Y34,Y87.2,Y89.9)', 
     134:'Operations of war and their sequelae (Y36,Y89.1)', 
     135:'Complications of medical and surgical care (Y40-Y84,Y88)'})
    icd9_ucod113 = DictTree({1:'Salmonella infections (002-003)', 
     2:'Shigellosis and amebiasis (004,006)', 
     3:'Certain other intestinal infections (007-009)', 
     4:DictTree(value='Tuberculosis (010-018)', d={5:'Respiratory tuberculosis (010-012)', 
      6:'Other tuberculosis (013-018)'}), 
     7:'Whooping cough (033)', 
     8:'Scarlet fever and erysipelas (034.1-035)', 
     9:'Meningococcal infection (036)', 
     10:'Septicemia (038)', 
     11:'Syphilis (090-097)', 
     12:'Acute poliomyelitis (045)', 
     13:'Arthropod-borne viral encephalitis (062-064)', 
     14:'Measles (055)', 
     15:'Viral hepatitis (070)', 
     16:'Human immunodeficiency virus (HIV) disease (042-044)', 
     17:'Malaria (084)', 
     18:'Other and unspecified infectious and parasitic diseases and their sequelae (001,005,020-032,037,039-041,046-054,056-061,065-066,071-083,085-088,098-134,136,139,771.3)', 
     19:DictTree(value='Malignant neoplasms (140-208)', d={20:'Malignant neoplasms of lip, oral cavity and pharynx (140-149)', 
      21:'Malignant neoplasm of esophagus (150)', 
      22:'Malignant neoplasm of stomach (151)', 
      23:'Malignant neoplasms of colon, rectum and anus (153-154)', 
      24:'Malignant neoplasms of liver and intrahepatic bile ducts (155)', 
      25:'Malignant neoplasm of pancreas (157)', 
      26:'Malignant neoplasm of larynx (161)', 
      27:'Malignant neoplasms of trachea, bronchus and lung (162)', 
      28:'Malignant melanoma of skin (172)', 
      29:'Malignant neoplasm of breast (174-175)', 
      30:'Malignant neoplasm of cervix uteri (180)', 
      31:'Malignant neoplasms of corpus uteri and uterus, part unspecified (179,182)', 
      32:'Malignant neoplasm of ovary (183.0)', 
      33:'Malignant neoplasm of prostate (185)', 
      34:'Malignant neoplasms of kidney and renal pelvis (189.0,189.1)', 
      35:'Malignant neoplasm of bladder (188)', 
      36:'Malignant neoplasms of meninges, brain and other parts of central nervous system (191-192)', 
      37:DictTree(value='Malignant neoplasms of lymphoid, hematopoietic and related tissue (200-208)', d={38:"Hodgkin's disease (201)", 
       39:"Non-Hodgkin's lymphoma (200,202)", 
       40:'Leukemia (204-208)', 
       41:'Multiple myeloma and immunoproliferative neoplasms (203)', 
       42:'Other and unspecified malignant neoplasms of lymphoid, hematopoietic and related tissue (NaN)'}), 
      43:'All other and unspecified malignant neoplasms (152,156,158-160,163-171,173,181,183.2-184,186-187,189.2-190,193-199)'}), 
     44:'In situ neoplasms, benign neoplasms and neoplasms of uncertain or unknown behavior (210-239)', 
     45:'Anemias (280-285)', 
     46:'Diabetes mellitus (250)', 
     47:DictTree(value='Nutritional deficiencies (260-269)', d={48:'Malnutrition (260-263)', 
      49:'Other nutritional deficiencies (264-269)'}), 
     50:'Meningitis (320-322)', 
     51:"Parkinson's disease (332)", 
     52:"Alzheimer's disease (331.0)", 
     53:DictTree(value='Major cardiovascular diseases (390-434,436-448)', d={54:DictTree(value='Diseases of heart (390-398,402,404,410-429)', d={55:'Acute rheumatic fever and chronic rheumatic heart diseases (390-398)', 
       56:'Hypertensive heart disease (402)', 
       57:'Hypertensive heart and renal disease (404)', 
       58:'Ischemic heart diseases (410-414,429.2)', 
       59:'Acute myocardial infarction (410)', 
       60:'Other acute ischemic heart diseases (411)', 
       61:DictTree(value='Other forms of chronic ischemic heart disease (412-414,429.2)', d={62:'Atherosclerotic cardiovascular disease, so described (429.2)', 
        63:'All other forms of chronic ischemic heart disease (412-414)'}), 
       64:DictTree(value='Other heart diseases (415-429.1,429.3-429.9)', d={65:'Acute and subacute endocarditis (421)', 
        66:'Diseases of pericardium and acute myocarditis (420,422-423)', 
        67:'Heart failure (428)', 
        68:'All other forms of heart disease (415-417,424-427,429.0-429.1,429.3-429.9)'})}), 
      69:'Essential (primary) hypertension and hypertensive renal disease (401,403)', 
      70:'Cerebrovascular diseases (430-434,436-438)', 
      71:'Atherosclerosis (440)', 
      72:DictTree(value='Other diseases of circulatory system (441-448)', d={73:'Aortic aneurysm and dissection (441)', 
       74:'Other diseases of arteries, arterioles and capillaries (442-448)'})}), 
     75:'Other disorders of circulatory system (451-459)', 
     76:DictTree(value='Influenza and pneumonia (480-487)', d={77:'Influenza (487)', 
      78:'Pneumonia (480-486)'}), 
     79:DictTree(value='Other acute lower respiratory infections (466)', d={80:'Acute bronchitis and bronchiolitis (466)', 
      81:'Other and unspecified acute lower respiratory infection (NaN)'}), 
     82:DictTree(value='Chronic lower respiratory diseases (490-494,496)', d={83:'Bronchitis, chronic and unspecified (490-491)', 
      84:'Emphysema (492)', 
      85:'Asthma (493)', 
      86:'Other chronic lower respiratory diseases (494,496)'}), 
     87:'Pneumoconioses and chemical effects (500-506)', 
     88:'Pneumonitis due to solids and liquids (507)', 
     89:'Other diseases of respiratory system (034.0,460-465,470-478,495,508-519)', 
     90:'Peptic ulcer (531-534)', 
     91:'Diseases of appendix (540-543)', 
     92:'Hernia (550-553)', 
     93:DictTree(value='Chronic liver disease and cirrhosis (571)', d={94:'Alcoholic liver disease (571.0-571.3)', 
      95:'Other chronic liver disease and cirrhosis (571.4-571.9)'}), 
     96:'Cholelithiasis and other disorders of gallbladder (574-575)', 
     97:DictTree(value='Nephritis, nephrotic syndrome and nephrosis (580-589)', d={98:'Acute and rapidly progressive nephritic and nephrotic syndrome (580-581)', 
      99:'Chronic glomerulonephritis, nephritis and nephropathy not specified as acute or chronic, and renal sclerosis unspecified (582-583,587)', 
      100:'Renal failure (584-586)', 
      101:'Other disorders of kidney (588-589)', 
      102:'Infections of kidney (590)'}), 
     103:'Hyperplasia of prostate (600)', 
     104:'Inflammatory diseases of female pelvic organs (614-616)', 
     105:DictTree(value='Pregnancy, childbirth and the puerperium (630-676)', d={106:'Pregnancy with abortive outcome (630-639)', 
      107:'Other complications of pregnancy, childbirth and the puerperium (640-676)'}), 
     108:'Certain conditions originating in the perinatal period (760-771.2,771.4-779)', 
     109:'Congenital malformations, deformations and chromosomal abnormalities (740-759)', 
     110:'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (780-799)', 
     111:'All other diseases (Residual) (NaN)', 
     112:DictTree(value='Accidents (unintentional injuries) (800-869,880-929)', d={113:'Transport accidents (800-848,929.0,929.1)', 
      114:'Motor vehicle accidents (810-825)', 
      115:'Other land transport accidents (800-807,826-829)', 
      116:'Water, air and space, and other and unspecified transport accidents and their sequelae (830-848,929.0,929.1)', 
      117:'Nontransport accidents (850-869,880-928,929.2-929.9)', 
      118:'Falls (880-888)', 
      119:'Accidental discharge of firearms (922)', 
      120:'Accidental drowning and submersion (910)', 
      121:'Accidental exposure to smoke, fire and flames (890-899)', 
      122:'Accidental poisoning and exposure to noxious substances (850-869,924.1)', 
      123:'Other and unspecified nontransport accidents and their sequelae (900-909,911-921,923-924.0,924.8-928,929.2-929.9)'}), 
     124:DictTree(value='Intentional self-harm (suicide) (950-959)', d={125:'Intentional self-harm (suicide) by discharge of firearms (955.0-955.4)', 
      126:'Intentional self-harm (suicide) by other and unspecified means and their sequelae (950-954,955.5-959)'}), 
     127:DictTree(value='Assault (homicide) (960-969)', d={128:'Assault (homicide) by discharge of firearms (965.0-965.4)', 
      129:'Assault (homicide) by other and unspecified means and their sequelae (960-964,965.5-969)'}), 
     130:'Legal intervention (970-978)', 
     131:'Events of undetermined intent (980-989)', 
     132:'Discharge of firearms, undetermined intent (985.0-985.4)', 
     133:'Other and unspecified events of undetermined intent and their sequelae (980-984,985.5-989)', 
     134:'Operations of war and their sequelae (990-999)', 
     135:'Complications of medical and surgical care (870-879,930-949)'})

    def initialize_parser(self, parser):
        super().initialize_parser(parser)
        parser.add_argument('--average-ages', help='Compute average ages column with the specified column name', default='AverageAge')
        parser.add_argument('--average-age-range', help='Range over which to calculate the average age', type=int, default=5)
        parser.add_argument('--comparable-ratios', help='Process comparable ratios for raw mortality matrix for prepare_data', action='store_true', default=False)
        parser.add_argument('--data-comparable-ratios-input-file', help='Comparable ratios file', default=(os.path.join(self.get_data_dir(), 'data/ucod/united_states/comparable_ucod_estimates.xlsx')))
        parser.add_argument('--data-comparability-ratio-tables', help='Comparable ratios file', default=(os.path.join(self.get_data_dir(), 'data/ucod/united_states/Comparability_Ratio_tables.xls')))
        parser.add_argument('--data-us-icd10-sub-chapters', help='Path to file for US_ICD10_SUB_CHAPTERS', default=(os.path.join(self.get_data_dir(), 'data/ucod/united_states/Underlying Cause of Death, 1999-2017_US_ICD10_SUB_CHAPTERS.txt')))
        parser.add_argument('--data-us-icd10-chapters', help='Path to file for US_ICD10_CHAPTERS', default=(os.path.join(self.get_data_dir(), 'data/ucod/united_states/Underlying Cause of Death, 1999-2017_US_ICD10_CHAPTERS.txt')))
        parser.add_argument('--data-us-icd10-minimally-grouped', help='Path to file for US_ICD10_MINIMALLY_GROUPED', default=(os.path.join(self.get_data_dir(), 'data/ucod/united_states/Underlying Cause of Death, 1999-2017_US_ICD10_MINIMALLY_GROUPED.txt')))
        parser.add_argument('--data-us-icd10-113-selected-causes', help='Path to file for US_ICD10_113_SELECTED_CAUSES', default=(os.path.join(self.get_data_dir(), 'data/ucod/united_states/Underlying Cause of Death, 1999-2017_US_ICD10_113_SELECTED_CAUSES.txt')))
        parser.add_argument('--data-us-icd-longterm-comparable-leading', help='Path to file for US_ICD_LONGTERM_COMPARABLE_LEADING', default=(os.path.join(self.get_data_dir(), 'data/ucod/united_states/comparable_ucod_estimates_ratios_applied.xlsx')))
        parser.add_argument('--download', help='If no files in --raw-files-directory, download and extract', action='store_true', default=True)
        parser.add_argument('--raw-files-directory', help='directory with raw files', default=(os.path.join(self.default_cache_dir, 'united_states')))
        parser.add_argument('--test', help='Test')

    @staticmethod
    def get_data_types_enum():
        return DataType

    @staticmethod
    def get_data_types_enum_default():
        return DataType.US_ICD_LONGTERM_COMPARABLE_LEADING

    def run_load--- This code section failed: ---

 L. 442         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                options
                4  LOAD_ATTR                data_type
                6  LOAD_GLOBAL              DataType
                8  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_ALL
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_TRUE     42  'to 42'

 L. 443        14  LOAD_DEREF               'self'
               16  LOAD_ATTR                options
               18  LOAD_ATTR                data_type
               20  LOAD_GLOBAL              DataType
               22  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_LEAVES
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_TRUE     42  'to 42'

 L. 444        28  LOAD_DEREF               'self'
               30  LOAD_ATTR                options
               32  LOAD_ATTR                data_type
               34  LOAD_GLOBAL              DataType
               36  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_ROOTS
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE   254  'to 254'
             42_0  COME_FROM            26  '26'
             42_1  COME_FROM            12  '12'

 L. 446        42  LOAD_DEREF               'self'
               44  LOAD_METHOD              get_raw_data_selected_causes
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  STORE_FAST               'df'

 L. 448        50  LOAD_DEREF               'self'
               52  LOAD_ATTR                options
               54  LOAD_ATTR                data_type
               56  LOAD_GLOBAL              DataType
               58  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_LEAVES
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_TRUE     78  'to 78'

 L. 449        64  LOAD_DEREF               'self'
               66  LOAD_ATTR                options
               68  LOAD_ATTR                data_type
               70  LOAD_GLOBAL              DataType
               72  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_ROOTS
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE   250  'to 250'
             78_0  COME_FROM            62  '62'

 L. 451        78  LOAD_DEREF               'self'
               80  LOAD_ATTR                options
               82  LOAD_ATTR                data_type
               84  LOAD_GLOBAL              DataType
               86  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_LEAVES
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   118  'to 118'

 L. 452        92  LOAD_DEREF               'self'
               94  LOAD_ATTR                icd9_ucod113
               96  LOAD_METHOD              recursive_list
               98  LOAD_CONST               True
              100  CALL_METHOD_1         1  '1 positional argument'
              102  LOAD_DEREF               'self'
              104  LOAD_ATTR                icd10_ucod113
              106  LOAD_METHOD              recursive_list
              108  LOAD_CONST               True
              110  CALL_METHOD_1         1  '1 positional argument'
              112  BINARY_ADD       
              114  STORE_FAST               'target'
              116  JUMP_FORWARD        138  'to 138'
            118_0  COME_FROM            90  '90'

 L. 454       118  LOAD_DEREF               'self'
              120  LOAD_ATTR                icd9_ucod113
              122  LOAD_METHOD              roots_list
              124  CALL_METHOD_0         0  '0 positional arguments'
              126  LOAD_DEREF               'self'
              128  LOAD_ATTR                icd10_ucod113
              130  LOAD_METHOD              roots_list
              132  CALL_METHOD_0         0  '0 positional arguments'
              134  BINARY_ADD       
              136  STORE_FAST               'target'
            138_0  COME_FROM           116  '116'

 L. 456       138  LOAD_GLOBAL              list
              140  LOAD_GLOBAL              map
              142  LOAD_DEREF               'self'
              144  LOAD_ATTR                icd_query
              146  LOAD_GLOBAL              map
              148  LOAD_DEREF               'self'
              150  LOAD_ATTR                extract_codes
              152  LOAD_FAST                'target'
              154  CALL_FUNCTION_2       2  '2 positional arguments'
              156  CALL_FUNCTION_2       2  '2 positional arguments'
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  STORE_FAST               'keep_queries'

 L. 457       162  LOAD_FAST                'df'
              164  LOAD_DEREF               'self'
              166  LOAD_METHOD              get_code_column_name
              168  CALL_METHOD_0         0  '0 positional arguments'
              170  BINARY_SUBSCR    
              172  LOAD_METHOD              apply
              174  LOAD_DEREF               'self'
              176  LOAD_ATTR                icd_query
              178  CALL_METHOD_1         1  '1 positional argument'
              180  LOAD_FAST                'df'
              182  LOAD_STR                 'CodesQuery'
              184  STORE_SUBSCR     

 L. 460       186  LOAD_FAST                'df'
              188  LOAD_ATTR                drop
              190  LOAD_FAST                'df'
              192  LOAD_FAST                'df'
              194  LOAD_STR                 'CodesQuery'
              196  BINARY_SUBSCR    
              198  LOAD_METHOD              isin
              200  LOAD_FAST                'keep_queries'
              202  CALL_METHOD_1         1  '1 positional argument'
              204  UNARY_INVERT     
              206  BINARY_SUBSCR    
              208  LOAD_ATTR                index
              210  LOAD_CONST               True
              212  LOAD_CONST               ('inplace',)
              214  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              216  POP_TOP          

 L. 463       218  LOAD_FAST                'df'
              220  LOAD_ATTR                drop
              222  LOAD_FAST                'df'
              224  LOAD_FAST                'df'
              226  LOAD_DEREF               'self'
              228  LOAD_METHOD              get_code_column_name
              230  CALL_METHOD_0         0  '0 positional arguments'
              232  BINARY_SUBSCR    
              234  LOAD_STR                 'NaN'
              236  COMPARE_OP               ==
              238  BINARY_SUBSCR    
              240  LOAD_ATTR                index
              242  LOAD_CONST               True
              244  LOAD_CONST               ('inplace',)
              246  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              248  POP_TOP          
            250_0  COME_FROM            76  '76'
          250_252  JUMP_FORWARD        550  'to 550'
            254_0  COME_FROM            40  '40'

 L. 465       254  LOAD_DEREF               'self'
              256  LOAD_ATTR                options
              258  LOAD_ATTR                data_type
              260  LOAD_GLOBAL              DataType
              262  LOAD_ATTR                US_ICD10_SUB_CHAPTERS
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_TRUE    302  'to 302'

 L. 466       270  LOAD_DEREF               'self'
              272  LOAD_ATTR                options
              274  LOAD_ATTR                data_type
              276  LOAD_GLOBAL              DataType
              278  LOAD_ATTR                US_ICD10_MINIMALLY_GROUPED
              280  COMPARE_OP               ==
          282_284  POP_JUMP_IF_TRUE    302  'to 302'

 L. 467       286  LOAD_DEREF               'self'
              288  LOAD_ATTR                options
              290  LOAD_ATTR                data_type
              292  LOAD_GLOBAL              DataType
              294  LOAD_ATTR                US_ICD10_CHAPTERS
              296  COMPARE_OP               ==
          298_300  POP_JUMP_IF_FALSE   402  'to 402'
            302_0  COME_FROM           282  '282'
            302_1  COME_FROM           266  '266'

 L. 469       302  LOAD_GLOBAL              pandas
              304  LOAD_ATTR                read_csv

 L. 470       306  LOAD_DEREF               'self'
              308  LOAD_METHOD              get_data_file
              310  CALL_METHOD_0         0  '0 positional arguments'

 L. 471       312  LOAD_STR                 '\t'

 L. 472       314  LOAD_STR                 'Year'
              316  LOAD_STR                 'Deaths'
              318  LOAD_STR                 'Population'
              320  BUILD_LIST_3          3 
              322  LOAD_DEREF               'self'
              324  LOAD_METHOD              get_read_columns
              326  CALL_METHOD_0         0  '0 positional arguments'
              328  BINARY_ADD       

 L. 473       330  LOAD_STR                 'Unreliable'
              332  BUILD_LIST_1          1 

 L. 474       334  LOAD_CONST               0
              336  BUILD_LIST_1          1 

 L. 475       338  LOAD_STR                 'ISO-8859-1'
              340  LOAD_CONST               ('sep', 'usecols', 'na_values', 'parse_dates', 'encoding')
              342  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              344  LOAD_ATTR                dropna

 L. 476       346  LOAD_STR                 'all'
              348  LOAD_CONST               ('how',)
              350  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              352  STORE_FAST               'df'

 L. 478       354  LOAD_DEREF               'self'
              356  LOAD_ATTR                options
              358  LOAD_ATTR                data_type
              360  LOAD_GLOBAL              DataType
              362  LOAD_ATTR                US_ICD10_MINIMALLY_GROUPED
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   550  'to 550'

 L. 481       370  LOAD_FAST                'df'
              372  LOAD_ATTR                apply
              374  LOAD_CLOSURE             'self'
              376  BUILD_TUPLE_1         1 
              378  LOAD_LAMBDA              '<code_object <lambda>>'
              380  LOAD_STR                 'UCODUnitedStates.run_load.<locals>.<lambda>'
              382  MAKE_FUNCTION_8          'closure'
              384  LOAD_STR                 'columns'
              386  LOAD_CONST               ('axis',)
              388  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              390  LOAD_FAST                'df'
              392  LOAD_DEREF               'self'
              394  LOAD_METHOD              get_action_column_name
              396  CALL_METHOD_0         0  '0 positional arguments'
              398  STORE_SUBSCR     
              400  JUMP_FORWARD        550  'to 550'
            402_0  COME_FROM           298  '298'

 L. 483       402  LOAD_DEREF               'self'
              404  LOAD_ATTR                options
              406  LOAD_ATTR                data_type
              408  LOAD_GLOBAL              DataType
              410  LOAD_ATTR                US_ICD_LONGTERM_COMPARABLE_LEADING
              412  COMPARE_OP               ==
          414_416  POP_JUMP_IF_FALSE   544  'to 544'

 L. 485       418  LOAD_GLOBAL              pandas
              420  LOAD_ATTR                read_excel

 L. 486       422  LOAD_DEREF               'self'
              424  LOAD_METHOD              get_data_file
              426  CALL_METHOD_0         0  '0 positional arguments'

 L. 487       428  LOAD_CONST               0

 L. 488       430  LOAD_CONST               0
              432  BUILD_LIST_1          1 
              434  LOAD_CONST               ('index_col', 'parse_dates')
              436  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              438  STORE_FAST               'df'

 L. 490       440  LOAD_FAST                'df'
              442  LOAD_ATTR                drop
              444  LOAD_STR                 'Total Deaths'
              446  LOAD_STR                 'ICD Revision'
              448  BUILD_LIST_2          2 
              450  LOAD_CONST               True
              452  LOAD_CONST               ('columns', 'inplace')
              454  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              456  POP_TOP          

 L. 491       458  LOAD_FAST                'df'
              460  LOAD_ATTR                columns
              462  LOAD_ATTR                values
              464  STORE_FAST               'melt_cols'

 L. 492       466  LOAD_FAST                'df'
              468  LOAD_METHOD              reset_index
              470  CALL_METHOD_0         0  '0 positional arguments'
              472  LOAD_ATTR                melt
              474  LOAD_STR                 'Year'
              476  BUILD_LIST_1          1 
              478  LOAD_FAST                'melt_cols'
              480  LOAD_DEREF               'self'
              482  LOAD_METHOD              get_action_column_name
              484  CALL_METHOD_0         0  '0 positional arguments'
              486  LOAD_STR                 'Deaths'
              488  LOAD_CONST               ('id_vars', 'value_vars', 'var_name', 'value_name')
              490  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              492  LOAD_ATTR                sort_values
              494  LOAD_STR                 'Year'
              496  LOAD_DEREF               'self'
              498  LOAD_METHOD              get_action_column_name
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  BUILD_LIST_2          2 
              504  LOAD_CONST               ('by',)
              506  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              508  STORE_FAST               'df'

 L. 493       510  LOAD_FAST                'df'
              512  LOAD_ATTR                Year
              514  LOAD_FAST                'df'
              516  STORE_ATTR               Year

 L. 494       518  LOAD_FAST                'df'
              520  LOAD_ATTR                Year
              522  LOAD_METHOD              apply
              524  LOAD_CLOSURE             'self'
              526  BUILD_TUPLE_1         1 
              528  LOAD_LAMBDA              '<code_object <lambda>>'
              530  LOAD_STR                 'UCODUnitedStates.run_load.<locals>.<lambda>'
              532  MAKE_FUNCTION_8          'closure'
              534  CALL_METHOD_1         1  '1 positional argument'
              536  LOAD_FAST                'df'
              538  LOAD_STR                 'Population'
              540  STORE_SUBSCR     
              542  JUMP_FORWARD        550  'to 550'
            544_0  COME_FROM           414  '414'

 L. 497       544  LOAD_GLOBAL              NotImplementedError
              546  CALL_FUNCTION_0       0  '0 positional arguments'
              548  RAISE_VARARGS_1       1  'exception instance'
            550_0  COME_FROM           542  '542'
            550_1  COME_FROM           400  '400'
            550_2  COME_FROM           366  '366'
            550_3  COME_FROM           250  '250'

 L. 499       550  LOAD_FAST                'df'
              552  LOAD_ATTR                rename
              554  LOAD_STR                 'Year'
              556  LOAD_STR                 'Date'
              558  BUILD_MAP_1           1 
              560  LOAD_CONST               True
              562  LOAD_CONST               ('columns', 'inplace')
              564  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              566  POP_TOP          

 L. 500       568  LOAD_FAST                'df'
              570  LOAD_STR                 'Date'
              572  BINARY_SUBSCR    
              574  LOAD_ATTR                dt
              576  LOAD_ATTR                year
              578  LOAD_FAST                'df'
              580  LOAD_STR                 'Year'
              582  STORE_SUBSCR     

 L. 502       584  LOAD_FAST                'df'
              586  LOAD_ATTR                Deaths
              588  LOAD_FAST                'df'
              590  LOAD_ATTR                Population
              592  BINARY_TRUE_DIVIDE
              594  LOAD_DEREF               'self'
              596  LOAD_METHOD              crude_rate_amount
              598  CALL_METHOD_0         0  '0 positional arguments'
              600  BINARY_MULTIPLY  
              602  LOAD_FAST                'df'
              604  LOAD_DEREF               'self'
              606  LOAD_METHOD              get_value_column_name
              608  CALL_METHOD_0         0  '0 positional arguments'
              610  STORE_SUBSCR     

 L. 503       612  LOAD_DEREF               'self'
              614  LOAD_METHOD              write_spreadsheet
              616  LOAD_FAST                'df'
              618  LOAD_DEREF               'self'
              620  LOAD_METHOD              prefix_all
              622  LOAD_STR                 'data'
              624  CALL_METHOD_1         1  '1 positional argument'
              626  CALL_METHOD_2         2  '2 positional arguments'
              628  POP_TOP          

 L. 504       630  LOAD_FAST                'df'
              632  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 550

    def load_us_raw_data_with_comparability_ratios(self):
        self.check_raw_files_directory()
        df = self.get_raw_mortality_counts((self.raw_icd_basis),
          None,
          None,
          (self.raw_icd9_counts),
          (self.raw_icd10_counts),
          min_year=1979,
          calculate_total=False,
          add_icd_revision=False,
          comparability_ratios=(self.get_icd9_10_comparability_ratios()))
        df.index.name = 'Year'
        df = df.reset_index().melt(id_vars=['Year'], value_vars=(df.columns.values)).sort_values('Year')
        df.columns = ['Year', self.get_action_column_name(), 'Deaths']
        df[self.get_code_column_name()] = df.apply((lambda row: self.extract_codes((UCODUnitedStates.icd10_ucod113 if row['Year'] >= 1999 else UCODUnitedStates.icd9_ucod113).find_value(lambda v: self.extract_name(v) == row[self.get_action_column_name()]))), axis='columns')
        df['Population'] = df.Year.apply(lambda y: self.mortality_uspopulation.loc[y]['Population'])
        df['Year'] = df['Year'].apply(lambda year: pandas.datetime.strptime(str(year), '%Y'))
        return df

    def get_raw_data_selected_causes(self):
        return self.load_with_cache('us_raw_data_with_comparability_ratios', self.load_us_raw_data_with_comparability_ratios)

    def get_action_column_name(self):
        if self.options.data_type == DataType.US_ICD10_SUB_CHAPTERS:
            return 'ICD Sub-Chapter'
        if self.options.data_type == DataType.US_ICD10_CHAPTERS:
            return 'ICD Chapter'
        if self.options.data_type == DataType.US_ICD10_MINIMALLY_GROUPED:
            return 'Cause of death'
        if self.options.data_type == DataType.US_ICD_LONGTERM_COMPARABLE_LEADING:
            return 'Cause of death'
        if self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_ALL or self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_LEAVES or self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_ROOTS:
            return 'ICD-10 113 Cause List'
        raise NotImplementedError()

    def get_value_column_name(self):
        return 'Crude Rate' + super().get_value_column_name()

    def get_code_column_name(self):
        if self.options.data_type == DataType.US_ICD10_SUB_CHAPTERS:
            return 'ICD Sub-Chapter Code'
        if self.options.data_type == DataType.US_ICD10_CHAPTERS:
            return 'ICD Chapter Code'
        if self.options.data_type == DataType.US_ICD10_MINIMALLY_GROUPED:
            return 'Cause of death Code'
        if self.options.data_type == DataType.US_ICD_LONGTERM_COMPARABLE_LEADING:
            return 'Cause of death Code'
        if self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_ALL or self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_LEAVES or self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_ROOTS:
            return 'Cause of death Codes'
        raise NotImplementedError()

    def get_data_file(self):
        if self.options.data_type == DataType.US_ICD10_SUB_CHAPTERS:
            return self.options.data_us_icd10_sub_chapters
        if self.options.data_type == DataType.US_ICD10_CHAPTERS:
            return self.options.data_us_icd10_chapters
        if self.options.data_type == DataType.US_ICD10_MINIMALLY_GROUPED:
            return self.options.data_us_icd10_minimally_grouped
        if self.options.data_type == DataType.US_ICD_LONGTERM_COMPARABLE_LEADING:
            return self.options.data_us_icd_longterm_comparable_leading
        if self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_ALL or self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_LEAVES or self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_ROOTS:
            return self.options.data_us_icd10_113_selected_causes
        raise NotImplementedError()

    def get_read_columns(self):
        if self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_ALL or self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_LEAVES or self.options.data_type == DataType.US_ICD_113_SELECTED_CAUSES_ROOTS:
            return [
             self.get_action_column_name()]
        return [self.get_action_column_name(), self.get_code_column_name()]

    def get_action_title_prefix(self):
        return 'Deaths from '

    def download_raw_files(self):
        print('Downloading raw files from https://www.nber.org/data/vital-statistics-mortality-data-multiple-cause-of-death.html')
        if not os.path.exists(self.options.raw_files_directory):
            os.makedirs(self.options.raw_files_directory)
        for i in range(1959, 2018):
            print('Downloading {}...'.format(i))
            downloaded_file = os.path.join(self.options.raw_files_directory, 'mort{0}.csv.zip'.format(i))
            urllib.request.urlretrieve('https://www.nber.org/mortality/{0}/mort{0}.csv.zip'.format(i), downloaded_file)
            with zipfile.ZipFile(downloaded_file, 'r') as (zfile):
                print('Unzipping mort{0}.csv.zip'.format(i))
                zfile.extractall(self.options.raw_files_directory)
                os.remove(downloaded_file)

    def check_raw_files_directory(self):
        if self.options.raw_files_directory is None:
            raise ValueError('--raw-files-directory required')
        else:
            if not os.path.exists(self.options.raw_files_directory):
                if self.options.download:
                    self.download_raw_files()
                else:
                    raise ValueError('--raw-files-directory does not exist')
            assert os.path.isdir(self.options.raw_files_directory), '--raw-files-directory is not a directory'

    def run_prepare_data(self):
        self.options.data_type = DataType.US_ICD_LONGTERM_COMPARABLE_LEADING
        self.check_raw_files_directory()
        if self.options.comparable_ratios:
            self.create_comparable()
        else:
            self.process_raw_mortality_data()

    def get_mortality_files(self):
        return sorted(glob.glob(os.path.join(self.options.raw_files_directory, '*.csv')))

    def get_mortality_file_info(self, csv):
        filename, file_extension = os.path.splitext(os.path.basename(csv))
        if filename.startswith('mort'):
            filename = filename[4:]
            file_year = int(filename)
            return (filename, file_extension, file_year)
        return (None, None, None)

    def get_mortality_data(self, csv, file_year):
        yearcol = 'datayear' if file_year <= 1995 else 'year'
        df = pandas.read_csv(csv,
          usecols=[
         yearcol, 'age', 'ucod'],
          dtype={yearcol: numpy.int32, 
         'age': str, 
         'ucod': str},
          na_values=[
         '&', '-'])
        if file_year >= 1968:
            if file_year <= 1977:
                df[yearcol] = df[yearcol].apply(lambda x:                 if x >= 8:
x + 1960 # Avoid dead code: x + 1970)
        if file_year == 1978:
            df[yearcol] = df[yearcol].apply(lambda x: x + 1970)
        if file_year >= 1979:
            if file_year <= 1995:
                df[yearcol] = df[yearcol].apply(lambda x: x + 1900)
        if df[yearcol].min() != file_year or df[yearcol].max() != file_year:
            raise ValueError('Unexpected year value {} in data for {}'.format(df[yearcol].min(), csv))
        df['AgeMinutes'] = df['age'].apply(ICD.convert_age_minutes)
        df['icdint'] = df['ucod'].apply(ICD.toint)
        df['icdfloat'] = df['ucod'].apply(ICD.tofloat)
        scale = 1
        if file_year == 1972:
            scale = 2
        return (df, scale)

    def get_longterm_comparable_yearly_basis(self):
        return {'Total Deaths':0, 
         'ICD Revision':0, 
         'Influenza and pneumonia':numpy.NaN, 
         'Tuberculosis':numpy.NaN, 
         'Diarrhea, enteritis, and colitis':numpy.NaN, 
         'Heart disease':numpy.NaN, 
         'Stroke':numpy.NaN, 
         'Kidney disease':numpy.NaN, 
         'Accidents excluding motor vehicles':numpy.NaN, 
         'Cancer':numpy.NaN, 
         'Perinatal Conditions':numpy.NaN, 
         'Diabetes':numpy.NaN, 
         'Motor vehicle accidents':numpy.NaN, 
         'Arteriosclerosis':numpy.NaN, 
         'Congenital Malformations':numpy.NaN, 
         'Cirrhosis of liver':numpy.NaN, 
         'Typhoid fever':numpy.NaN, 
         'Measles':numpy.NaN, 
         'Whooping cough':numpy.NaN, 
         'Diphtheria':numpy.NaN, 
         'Intestinal infections':numpy.NaN, 
         'Meningococcal infections':numpy.NaN, 
         'Acute poliomyelitis':numpy.NaN, 
         'Syphilis':numpy.NaN, 
         'Acute rheumatic fever':numpy.NaN, 
         'Hypertension':numpy.NaN, 
         'Chronic respiratory diseases':numpy.NaN, 
         'Ulcer':numpy.NaN, 
         'Suicide':numpy.NaN, 
         'Homicide':numpy.NaN}

    def longterm_comparable_icd7(self, df, count_years, scale, comparability_ratios):
        count_years['Tuberculosis'] = len(df.query(self.icd_query('001-019'))) * scale
        count_years['Diarrhea, enteritis, and colitis'] = len(df.query(self.icd_query('543,571,572'))) * scale
        count_years['Cancer'] = len(df.query(self.icd_query('140-205'))) * scale
        count_years['Diabetes'] = len(df.query(self.icd_query('260'))) * scale
        count_years['Heart disease'] = len(df.query(self.icd_query('400-402,410-443'))) * scale
        count_years['Stroke'] = len(df.query(self.icd_query('330-334'))) * scale
        count_years['Arteriosclerosis'] = len(df.query(self.icd_query('450'))) * scale
        count_years['Influenza and pneumonia'] = len(df.query(self.icd_query('480-493'))) * scale
        count_years['Cirrhosis of liver'] = len(df.query(self.icd_query('581'))) * scale
        count_years['Kidney disease'] = len(df.query(self.icd_query('590-594'))) * scale
        count_years['Congenital Malformations'] = len(df.query(self.icd_query('750-759'))) * scale
        count_years['Perinatal Conditions'] = len(df.query(self.icd_query('760-776'))) * scale
        count_years['Motor vehicle accidents'] = len(df.query(self.icd_query('810-835'))) * scale
        count_years['Accidents excluding motor vehicles'] = len(df.query(self.icd_query('800-802,840-962'))) * scale
        count_years['Typhoid fever'] = len(df.query(self.icd_query('040'))) * scale
        count_years['Measles'] = len(df.query(self.icd_query('085'))) * scale
        count_years['Whooping cough'] = len(df.query(self.icd_query('056'))) * scale
        count_years['Diphtheria'] = len(df.query(self.icd_query('055'))) * scale
        count_years['Intestinal infections'] = len(df.query(self.icd_query('571,764'))) * scale
        count_years['Meningococcal infections'] = len(df.query(self.icd_query('057'))) * scale
        count_years['Acute poliomyelitis'] = len(df.query(self.icd_query('080'))) * scale
        count_years['Syphilis'] = len(df.query(self.icd_query('020-029'))) * scale
        count_years['Acute rheumatic fever'] = len(df.query(self.icd_query('400-402'))) * scale
        count_years['Hypertension'] = len(df.query(self.icd_query('444-447'))) * scale
        count_years['Chronic respiratory diseases'] = len(df.query(self.icd_query('241,501,502,527.1'))) * scale
        count_years['Ulcer'] = len(df.query(self.icd_query('540,541'))) * scale
        count_years['Suicide'] = len(df.query(self.icd_query('963,970-979'))) * scale
        count_years['Homicide'] = len(df.query(self.icd_query('964,980-985'))) * scale

    def longterm_comparable_icd8(self, df, count_years, scale, comparability_ratios):
        count_years['Tuberculosis'] = len(df.query(self.icd_query('010-019'))) * scale
        count_years['Diarrhea, enteritis, and colitis'] = len(df.query(self.icd_query('009'))) * scale
        count_years['Cancer'] = len(df.query(self.icd_query('140-209'))) * scale
        count_years['Diabetes'] = len(df.query(self.icd_query('250'))) * scale
        count_years['Heart disease'] = len(df.query(self.icd_query('390-398,402,404,410-429'))) * scale
        count_years['Stroke'] = len(df.query(self.icd_query('430-438'))) * scale
        count_years['Arteriosclerosis'] = len(df.query(self.icd_query('440'))) * scale
        count_years['Influenza and pneumonia'] = len(df.query(self.icd_query('470-474,480-486'))) * scale
        count_years['Cirrhosis of liver'] = len(df.query(self.icd_query('571'))) * scale
        count_years['Kidney disease'] = len(df.query(self.icd_query('580-584'))) * scale
        count_years['Congenital Malformations'] = len(df.query(self.icd_query('740-759'))) * scale
        count_years['Perinatal Conditions'] = len(df.query(self.icd_query('760-769.2,769.4-772,774-778'))) * scale
        count_years['Motor vehicle accidents'] = len(df.query(self.icd_query('810-823'))) * scale
        count_years['Accidents excluding motor vehicles'] = len(df.query(self.icd_query('800-807,825-949'))) * scale
        count_years['Typhoid fever'] = len(df.query(self.icd_query('001'))) * scale
        count_years['Measles'] = len(df.query(self.icd_query('055'))) * scale
        count_years['Whooping cough'] = len(df.query(self.icd_query('033'))) * scale
        count_years['Diphtheria'] = len(df.query(self.icd_query('032'))) * scale
        count_years['Intestinal infections'] = len(df.query(self.icd_query('008,009'))) * scale
        count_years['Meningococcal infections'] = len(df.query(self.icd_query('036'))) * scale
        count_years['Acute poliomyelitis'] = len(df.query(self.icd_query('040-043'))) * scale
        count_years['Syphilis'] = len(df.query(self.icd_query('090-097'))) * scale
        count_years['Acute rheumatic fever'] = len(df.query(self.icd_query('390-392'))) * scale
        count_years['Hypertension'] = len(df.query(self.icd_query('400,401,403'))) * scale
        count_years['Chronic respiratory diseases'] = len(df.query(self.icd_query('490-493'))) * scale
        count_years['Ulcer'] = len(df.query(self.icd_query('531-533'))) * scale
        count_years['Suicide'] = len(df.query(self.icd_query('950-959'))) * scale
        count_years['Homicide'] = len(df.query(self.icd_query('960-978'))) * scale

    def longterm_comparable_icd9(self, df, count_years, scale, comparability_ratios):
        count_years['Tuberculosis'] = len(df.query(self.icd_query('010-018'))) * scale
        count_years['Diarrhea, enteritis, and colitis'] = len(df.query(self.icd_query('009'))) * scale
        count_years['Cancer'] = len(df.query(self.icd_query('140-208'))) * scale
        count_years['Diabetes'] = len(df.query(self.icd_query('250'))) * scale
        count_years['Heart disease'] = len(df.query(self.icd_query('390-398,402,404,410-429'))) * scale
        count_years['Stroke'] = len(df.query(self.icd_query('430-438'))) * scale
        count_years['Arteriosclerosis'] = len(df.query(self.icd_query('440'))) * scale
        count_years['Influenza and pneumonia'] = len(df.query(self.icd_query('480-487'))) * scale
        count_years['Cirrhosis of liver'] = len(df.query(self.icd_query('571'))) * scale
        count_years['Kidney disease'] = len(df.query(self.icd_query('580-589'))) * scale
        count_years['Congenital Malformations'] = len(df.query(self.icd_query('740-759'))) * scale
        count_years['Perinatal Conditions'] = len(df.query(self.icd_query('760-779'))) * scale
        count_years['Motor vehicle accidents'] = len(df.query(self.icd_query('810-825'))) * scale
        count_years['Accidents excluding motor vehicles'] = len(df.query(self.icd_query('800-807,826-949'))) * scale
        count_years['Typhoid fever'] = len(df.query(self.icd_query('002.0'))) * scale
        count_years['Measles'] = len(df.query(self.icd_query('055'))) * scale
        count_years['Whooping cough'] = len(df.query(self.icd_query('033'))) * scale
        count_years['Diphtheria'] = len(df.query(self.icd_query('032'))) * scale
        count_years['Intestinal infections'] = len(df.query(self.icd_query('007-009'))) * scale
        count_years['Meningococcal infections'] = len(df.query(self.icd_query('036'))) * scale
        count_years['Acute poliomyelitis'] = len(df.query(self.icd_query('045'))) * scale
        count_years['Syphilis'] = len(df.query(self.icd_query('090-097'))) * scale
        count_years['Acute rheumatic fever'] = len(df.query(self.icd_query('390-392'))) * scale
        count_years['Hypertension'] = len(df.query(self.icd_query('401,403'))) * scale
        count_years['Chronic respiratory diseases'] = len(df.query(self.icd_query('490-496'))) * scale
        count_years['Ulcer'] = len(df.query(self.icd_query('531-533'))) * scale
        count_years['Suicide'] = len(df.query(self.icd_query('950-959'))) * scale
        count_years['Homicide'] = len(df.query(self.icd_query('960-978'))) * scale

    def longterm_comparable_icd10(self, df, count_years, scale, comparability_ratios):
        count_years['Tuberculosis'] = len(df.query(self.icd_query('A16-A19'))) * scale
        count_years['Diarrhea, enteritis, and colitis'] = len(df.query(self.icd_query('A09'))) * scale
        count_years['Cancer'] = len(df.query(self.icd_query('C00-C97'))) * scale
        count_years['Diabetes'] = len(df.query(self.icd_query('E10-E14'))) * scale
        count_years['Heart disease'] = len(df.query(self.icd_query('I00-I09,I11,I13,I20-I51'))) * scale
        count_years['Stroke'] = len(df.query(self.icd_query('I60-I69,G45'))) * scale
        count_years['Arteriosclerosis'] = len(df.query(self.icd_query('I70'))) * scale
        count_years['Influenza and pneumonia'] = len(df.query(self.icd_query('J10-J18'))) * scale
        count_years['Cirrhosis of liver'] = len(df.query(self.icd_query('K70,K73-K74'))) * scale
        count_years['Kidney disease'] = len(df.query(self.icd_query('N00-N07,N17-N19,N25-N27'))) * scale
        count_years['Congenital Malformations'] = len(df.query(self.icd_query('Q00-Q99'))) * scale
        count_years['Perinatal Conditions'] = len(df.query(self.icd_query('P00-P96, A33'))) * scale
        count_years['Motor vehicle accidents'] = len(df.query(self.icd_query('V02-V04,V09.0,V09.2,V12-V14,V19.0-V19.2,V19.4-V19.6,V20-V79,V80.3-V80.5,V81.0-V81.1,V82.0-V82.1,V83-V86,V87.0-V87.8,V88.0-V88.8,V89.0,V89.2'))) * scale
        count_years['Accidents excluding motor vehicles'] = len(df.query(self.icd_query('V01,V05-V08,V09.1,V09.3-V11,V15-V18,V19.3,V19.7-V19.9,V80.0-V80.2,V80.6-V80.9,V81.2-V81.9,V82.2-V82.9,V87.9,V88.9,V89.1,V89.3-X59,Y85-Y86'))) * scale
        count_years['Typhoid fever'] = len(df.query(self.icd_query('A01.0'))) * scale
        count_years['Measles'] = len(df.query(self.icd_query('B05'))) * scale
        count_years['Whooping cough'] = len(df.query(self.icd_query('A37'))) * scale
        count_years['Diphtheria'] = len(df.query(self.icd_query('A36'))) * scale
        count_years['Intestinal infections'] = len(df.query(self.icd_query('A04,A07-A09'))) * scale
        count_years['Meningococcal infections'] = len(df.query(self.icd_query('A39'))) * scale
        count_years['Acute poliomyelitis'] = len(df.query(self.icd_query('A80'))) * scale
        count_years['Syphilis'] = len(df.query(self.icd_query('A50-A53'))) * scale
        count_years['Acute rheumatic fever'] = len(df.query(self.icd_query('I00-I02'))) * scale
        count_years['Hypertension'] = len(df.query(self.icd_query('I10, I12'))) * scale
        count_years['Chronic respiratory diseases'] = len(df.query(self.icd_query('J40-J47,J67'))) * scale
        count_years['Ulcer'] = len(df.query(self.icd_query('K25-K28'))) * scale
        count_years['Suicide'] = len(df.query(self.icd_query('X60-X84,Y87.0'))) * scale
        count_years['Homicide'] = len(df.query(self.icd_query('X85-Y09,Y35,Y87.1,Y89.0'))) * scale

    def get_raw_mortality_counts(self, yearly_basis, process_icd7, process_icd8, process_icd9, process_icd10, min_year=None, calculate_total=True, add_icd_revision=True, comparability_ratios=None):
        counts = {}
        csvs = self.get_mortality_files()
        for i, csv in enumerate(csvs):
            filename, file_extension, file_year = self.get_mortality_file_info(csv)
            if filename:
                if min_year is not None:
                    if file_year < min_year:
                        continue
                    else:
                        count_years = yearly_basis()
                        counts[file_year] = count_years
                        if add_icd_revision:
                            count_years['ICD Revision'] = UCODUnitedStates.mortality_uspopulation.loc[file_year]['ICDRevision']
                        self.print_processing_csv(i, csv, csvs)
                        df, scale = self.get_mortality_data(csv, file_year)
                        if calculate_total:
                            count_years['Total Deaths'] = len(df) * scale
                        if file_year >= 1958:
                            if file_year <= 1967:
                                process_icd7(df, count_years, scale, comparability_ratios)
                    if file_year >= 1968:
                        if file_year <= 1978:
                            process_icd8(df, count_years, scale, comparability_ratios)
                elif file_year >= 1979:
                    if file_year <= 1998:
                        process_icd9(df, count_years, scale, comparability_ratios)
                if file_year >= 1999:
                    process_icd10(df, count_years, scale, comparability_ratios)

        df = pandas.DataFrame.from_dict(counts, orient='index')
        return df

    def process_raw_mortality_data(self):
        df = self.get_raw_mortality_counts(self.get_longterm_comparable_yearly_basis, self.longterm_comparable_icd7(), self.longterm_comparable_icd8(), self.longterm_comparable_icd9(), self.longterm_comparable_icd10())
        output_file = os.path.abspath(os.path.join(self.options.cachedir, 'comparable_data_since_1959.xlsx'))
        df.to_excel(output_file)
        print('Created {}'.format(output_file))

    def create_comparable(self):
        comparability_ratios = pandas.read_excel((self.options.data_comparable_ratios_input_file), sheet_name='Comparability Ratios', index_col=0, usecols=[0, 2, 4, 6, 8, 10]).fillna(1)
        comparable_ucods = pandas.read_excel((self.options.data_comparable_ratios_input_file), index_col='Year')
        comparable_ucods = comparable_ucods.transform((self.transform_row), axis='columns', comparability_ratios=comparability_ratios)
        comparable_ucods.to_excel(self.get_data_file())
        print('Created {}'.format(self.get_data_file()))

    def transform_row(self, row, comparability_ratios):
        icd = row['ICD Revision']
        currenticd = 10
        if icd < currenticd:
            icd_index = int(icd - 5)
            for column in row.index.values:
                if column in comparability_ratios.index:
                    ratios = comparability_ratios.loc[column]
                    ratios = ratios.iloc[icd_index:]
                    row[column] = row[column] * numpy.prod(ratios.values)

        return row

    def create_with_multi_index2(self, d, indexcols):
        if len(d) > 0:
            reform = {(firstKey, secondKey):values for firstKey, secondDict in d.items() for secondKey, values in secondDict.items()}
            return pandas.DataFrame.from_dict(reform, orient='index').rename_axis(indexcols).sort_index()
        return

    def print_processing_csv(self, i, csv, csvs):
        print('Processing {} ({} of {})'.format(csv, i + 1, len(csvs)))

    def run_filter(self):
        self.data['icdint'] = self.data[self.get_code_column_name()].apply(ICD.toint)
        self.data['icdfloat'] = self.data[self.get_code_column_name()].apply(ICD.tofloat)
        self.data = self.data.query(self.icd_query(self.options.filter))

    def post_process_b(self, df):
        df.drop((df[(df.index == 'All other diseases (Residual)')].index), inplace=True)
        return df

    def get_calculated_scale_function_values--- This code section failed: ---

 L. 909         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              check_raw_files_directory
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 910         8  LOAD_DEREF               'self'
               10  LOAD_ATTR                options
               12  LOAD_ATTR                average_age_range
               14  STORE_FAST               'average_range'

 L. 911        16  LOAD_DEREF               'self'
               18  LOAD_ATTR                data
               20  LOAD_STR                 'Year'
               22  BINARY_SUBSCR    
               24  LOAD_METHOD              max
               26  CALL_METHOD_0         0  '0 positional arguments'
               28  LOAD_DEREF               'self'
               30  LOAD_ATTR                options
               32  LOAD_ATTR                average_age_range
               34  BINARY_SUBTRACT  
               36  LOAD_CONST               1
               38  BINARY_ADD       
               40  STORE_FAST               'min_year'

 L. 913        42  LOAD_DEREF               'self'
               44  LOAD_ATTR                options
               46  LOAD_ATTR                data_type
               48  LOAD_GLOBAL              DataType
               50  LOAD_ATTR                US_ICD10_SUB_CHAPTERS
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_TRUE    126  'to 126'

 L. 914        56  LOAD_DEREF               'self'
               58  LOAD_ATTR                options
               60  LOAD_ATTR                data_type
               62  LOAD_GLOBAL              DataType
               64  LOAD_ATTR                US_ICD10_MINIMALLY_GROUPED
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_TRUE    126  'to 126'

 L. 915        70  LOAD_DEREF               'self'
               72  LOAD_ATTR                options
               74  LOAD_ATTR                data_type
               76  LOAD_GLOBAL              DataType
               78  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_ALL
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_TRUE    126  'to 126'

 L. 916        84  LOAD_DEREF               'self'
               86  LOAD_ATTR                options
               88  LOAD_ATTR                data_type
               90  LOAD_GLOBAL              DataType
               92  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_LEAVES
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_TRUE    126  'to 126'

 L. 917        98  LOAD_DEREF               'self'
              100  LOAD_ATTR                options
              102  LOAD_ATTR                data_type
              104  LOAD_GLOBAL              DataType
              106  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_ROOTS
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_TRUE    126  'to 126'

 L. 918       112  LOAD_DEREF               'self'
              114  LOAD_ATTR                options
              116  LOAD_ATTR                data_type
              118  LOAD_GLOBAL              DataType
              120  LOAD_ATTR                US_ICD10_CHAPTERS
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   180  'to 180'
            126_0  COME_FROM           110  '110'
            126_1  COME_FROM            96  '96'
            126_2  COME_FROM            82  '82'
            126_3  COME_FROM            68  '68'
            126_4  COME_FROM            54  '54'

 L. 919       126  LOAD_DEREF               'self'
              128  LOAD_ATTR                data
              130  LOAD_DEREF               'self'
              132  LOAD_METHOD              get_code_column_name
              134  CALL_METHOD_0         0  '0 positional arguments'
              136  BINARY_SUBSCR    
              138  LOAD_METHOD              unique
              140  CALL_METHOD_0         0  '0 positional arguments'
              142  STORE_FAST               'icd_codes'

 L. 920       144  LOAD_GLOBAL              dict
              146  LOAD_GLOBAL              zip
              148  LOAD_FAST                'icd_codes'
              150  LOAD_LISTCOMP            '<code_object <listcomp>>'
              152  LOAD_STR                 'UCODUnitedStates.get_calculated_scale_function_values.<locals>.<listcomp>'
              154  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              156  LOAD_GLOBAL              range
              158  LOAD_CONST               0
              160  LOAD_GLOBAL              len
              162  LOAD_FAST                'icd_codes'
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  CALL_FUNCTION_2       2  '2 positional arguments'
              168  GET_ITER         
              170  CALL_FUNCTION_1       1  '1 positional argument'
              172  CALL_FUNCTION_2       2  '2 positional arguments'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  STORE_FAST               'icd_codes_map'
              178  JUMP_FORWARD        274  'to 274'
            180_0  COME_FROM           124  '124'

 L. 921       180  LOAD_DEREF               'self'
              182  LOAD_ATTR                options
              184  LOAD_ATTR                data_type
              186  LOAD_GLOBAL              DataType
              188  LOAD_ATTR                US_ICD_LONGTERM_COMPARABLE_LEADING
              190  COMPARE_OP               ==
          192_194  POP_JUMP_IF_FALSE   268  'to 268'

 L. 922       196  LOAD_GLOBAL              pandas
              198  LOAD_ATTR                read_excel

 L. 923       200  LOAD_DEREF               'self'
              202  LOAD_ATTR                options
              204  LOAD_ATTR                data_comparable_ratios_input_file

 L. 924       206  LOAD_CONST               0

 L. 925       208  LOAD_STR                 'Comparability Ratios'

 L. 926       210  LOAD_CONST               0
              212  LOAD_CONST               11
              214  BUILD_LIST_2          2 

 L. 927       216  LOAD_CONST               True
              218  LOAD_CONST               ('index_col', 'sheet_name', 'usecols', 'squeeze')
              220  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              222  STORE_DEREF              'ulcl_codes'

 L. 929       224  LOAD_DEREF               'ulcl_codes'
              226  LOAD_METHOD              unique
              228  CALL_METHOD_0         0  '0 positional arguments'
              230  STORE_FAST               'icd_codes'

 L. 930       232  LOAD_GLOBAL              dict
              234  LOAD_GLOBAL              zip
              236  LOAD_FAST                'icd_codes'
              238  LOAD_LISTCOMP            '<code_object <listcomp>>'
              240  LOAD_STR                 'UCODUnitedStates.get_calculated_scale_function_values.<locals>.<listcomp>'
              242  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              244  LOAD_GLOBAL              range
              246  LOAD_CONST               0
              248  LOAD_GLOBAL              len
              250  LOAD_FAST                'icd_codes'
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  CALL_FUNCTION_2       2  '2 positional arguments'
              256  GET_ITER         
              258  CALL_FUNCTION_1       1  '1 positional argument'
              260  CALL_FUNCTION_2       2  '2 positional arguments'
              262  CALL_FUNCTION_1       1  '1 positional argument'
              264  STORE_FAST               'icd_codes_map'
              266  JUMP_FORWARD        274  'to 274'
            268_0  COME_FROM           192  '192'

 L. 932       268  LOAD_GLOBAL              NotImplementedError
              270  CALL_FUNCTION_0       0  '0 positional arguments'
              272  RAISE_VARARGS_1       1  'exception instance'
            274_0  COME_FROM           266  '266'
            274_1  COME_FROM           178  '178'

 L. 934       274  LOAD_DEREF               'self'
              276  LOAD_METHOD              get_mortality_files
              278  CALL_METHOD_0         0  '0 positional arguments'
              280  STORE_FAST               'csvs'

 L. 935       282  BUILD_MAP_0           0 
              284  STORE_FAST               'stats'

 L. 936       286  LOAD_GLOBAL              sys
              288  LOAD_ATTR                maxsize
              290  STORE_FAST               'max_year'

 L. 937       292  SETUP_LOOP          530  'to 530'
              294  LOAD_GLOBAL              enumerate
              296  LOAD_FAST                'csvs'
              298  CALL_FUNCTION_1       1  '1 positional argument'
              300  GET_ITER         
            302_0  COME_FROM           348  '348'
            302_1  COME_FROM           338  '338'
            302_2  COME_FROM           328  '328'
              302  FOR_ITER            528  'to 528'
              304  UNPACK_SEQUENCE_2     2 
              306  STORE_FAST               'i'
              308  STORE_FAST               'csv'

 L. 938       310  LOAD_DEREF               'self'
              312  LOAD_METHOD              get_mortality_file_info
              314  LOAD_FAST                'csv'
              316  CALL_METHOD_1         1  '1 positional argument'
              318  UNPACK_SEQUENCE_3     3 
              320  STORE_FAST               'filename'
              322  STORE_FAST               'file_extension'
              324  STORE_FAST               'file_year'

 L. 939       326  LOAD_FAST                'filename'
          328_330  POP_JUMP_IF_FALSE   302  'to 302'
              332  LOAD_FAST                'file_year'
              334  LOAD_FAST                'min_year'
              336  COMPARE_OP               >=
          338_340  POP_JUMP_IF_FALSE   302  'to 302'
              342  LOAD_FAST                'file_year'
              344  LOAD_FAST                'max_year'
              346  COMPARE_OP               <=
          348_350  POP_JUMP_IF_FALSE   302  'to 302'

 L. 940       352  LOAD_DEREF               'self'
              354  LOAD_METHOD              print_processing_csv
              356  LOAD_FAST                'i'
              358  LOAD_FAST                'csv'
              360  LOAD_FAST                'csvs'
              362  CALL_METHOD_3         3  '3 positional arguments'
              364  POP_TOP          

 L. 941       366  BUILD_MAP_0           0 
              368  STORE_FAST               'year_stats'

 L. 942       370  LOAD_FAST                'year_stats'
              372  LOAD_FAST                'stats'
              374  LOAD_FAST                'file_year'
              376  STORE_SUBSCR     

 L. 943       378  LOAD_DEREF               'self'
              380  LOAD_METHOD              get_mortality_data
              382  LOAD_FAST                'csv'
              384  LOAD_FAST                'file_year'
              386  CALL_METHOD_2         2  '2 positional arguments'
              388  UNPACK_SEQUENCE_2     2 
              390  STORE_FAST               'df'
              392  STORE_FAST               'scale'

 L. 944       394  SETUP_LOOP          524  'to 524'
              396  LOAD_FAST                'icd_codes_map'
              398  LOAD_METHOD              items
              400  CALL_METHOD_0         0  '0 positional arguments'
              402  GET_ITER         
            404_0  COME_FROM           428  '428'
            404_1  COME_FROM           418  '418'
              404  FOR_ITER            522  'to 522'
              406  UNPACK_SEQUENCE_2     2 
              408  STORE_FAST               'icd_range'
              410  STORE_FAST               'trash'

 L. 945       412  LOAD_FAST                'icd_range'
              414  LOAD_STR                 'Residual'
              416  COMPARE_OP               !=
          418_420  POP_JUMP_IF_FALSE   404  'to 404'
              422  LOAD_FAST                'icd_range'
              424  LOAD_STR                 'NaN'
              426  COMPARE_OP               !=
          428_430  POP_JUMP_IF_FALSE   404  'to 404'

 L. 946       432  LOAD_FAST                'df'
              434  LOAD_METHOD              query
              436  LOAD_DEREF               'self'
              438  LOAD_METHOD              icd_query
              440  LOAD_FAST                'icd_range'
              442  CALL_METHOD_1         1  '1 positional argument'
              444  CALL_METHOD_1         1  '1 positional argument'
              446  LOAD_STR                 'AgeMinutes'
              448  BINARY_SUBSCR    
              450  STORE_FAST               'ages'

 L. 947       452  LOAD_GLOBAL              type
              454  LOAD_FAST                'ages'
              456  CALL_FUNCTION_1       1  '1 positional argument'
              458  LOAD_GLOBAL              numpy
              460  LOAD_ATTR                float64
              462  COMPARE_OP               is
          464_466  POP_JUMP_IF_FALSE   488  'to 488'

 L. 948       468  LOAD_FAST                'ages'
              470  LOAD_FAST                'ages'
              472  LOAD_CONST               1
              474  LOAD_FAST                'scale'
              476  LOAD_CONST               ('Sum', 'Max', 'Count', 'Scale')
              478  BUILD_CONST_KEY_MAP_4     4 
              480  LOAD_FAST                'year_stats'
              482  LOAD_FAST                'icd_range'
              484  STORE_SUBSCR     
              486  JUMP_BACK           404  'to 404'
            488_0  COME_FROM           464  '464'

 L. 950       488  LOAD_FAST                'ages'
              490  LOAD_METHOD              sum
              492  CALL_METHOD_0         0  '0 positional arguments'
              494  LOAD_FAST                'ages'
              496  LOAD_METHOD              max
              498  CALL_METHOD_0         0  '0 positional arguments'
              500  LOAD_FAST                'ages'
              502  LOAD_METHOD              count
              504  CALL_METHOD_0         0  '0 positional arguments'
              506  LOAD_FAST                'scale'
              508  LOAD_CONST               ('Sum', 'Max', 'Count', 'Scale')
              510  BUILD_CONST_KEY_MAP_4     4 
              512  LOAD_FAST                'year_stats'
              514  LOAD_FAST                'icd_range'
              516  STORE_SUBSCR     
          518_520  JUMP_BACK           404  'to 404'
              522  POP_BLOCK        
            524_0  COME_FROM_LOOP      394  '394'
          524_526  JUMP_BACK           302  'to 302'
              528  POP_BLOCK        
            530_0  COME_FROM_LOOP      292  '292'

 L. 952       530  LOAD_STR                 'Codes'
              532  STORE_FAST               'codescol'

 L. 953       534  LOAD_DEREF               'self'
              536  LOAD_METHOD              create_with_multi_index2
              538  LOAD_FAST                'stats'
              540  LOAD_STR                 'Year'
              542  LOAD_FAST                'codescol'
              544  BUILD_LIST_2          2 
              546  CALL_METHOD_2         2  '2 positional arguments'
              548  STORE_FAST               'statsdf'

 L. 954       550  LOAD_FAST                'statsdf'
              552  LOAD_METHOD              dropna
              554  CALL_METHOD_0         0  '0 positional arguments'
              556  STORE_FAST               'statsdf'

 L. 955       558  LOAD_DEREF               'self'
              560  LOAD_METHOD              write_spreadsheet
              562  LOAD_FAST                'statsdf'
              564  LOAD_DEREF               'self'
              566  LOAD_METHOD              prefix_all
              568  LOAD_STR                 'statsdf'
              570  CALL_METHOD_1         1  '1 positional argument'
              572  CALL_METHOD_2         2  '2 positional arguments'
              574  POP_TOP          

 L. 956       576  LOAD_FAST                'statsdf'
              578  LOAD_ATTR                loc
              580  LOAD_FAST                'statsdf'
              582  LOAD_ATTR                index
              584  LOAD_METHOD              max
              586  CALL_METHOD_0         0  '0 positional arguments'
              588  LOAD_CONST               0
              590  BINARY_SUBSCR    
              592  LOAD_FAST                'average_range'
              594  BINARY_SUBTRACT  
              596  LOAD_FAST                'statsdf'
              598  LOAD_ATTR                index
              600  LOAD_METHOD              max
              602  CALL_METHOD_0         0  '0 positional arguments'
              604  LOAD_CONST               0
              606  BINARY_SUBSCR    
              608  BUILD_SLICE_2         2 
              610  BINARY_SUBSCR    
              612  STORE_FAST               'subset'

 L. 957       614  LOAD_FAST                'statsdf'
              616  LOAD_STR                 'Max'
              618  BINARY_SUBSCR    
              620  LOAD_METHOD              max
              622  CALL_METHOD_0         0  '0 positional arguments'
              624  STORE_DEREF              'deathmax'

 L. 958       626  LOAD_DEREF               'self'
              628  LOAD_ATTR                options
              630  LOAD_ATTR                average_ages
              632  STORE_FAST               'calculated_col'

 L. 959       634  LOAD_FAST                'subset'
              636  LOAD_METHOD              groupby
              638  LOAD_FAST                'codescol'
              640  CALL_METHOD_1         1  '1 positional argument'
              642  LOAD_METHOD              apply
              644  LOAD_CLOSURE             'deathmax'
              646  BUILD_TUPLE_1         1 
              648  LOAD_LAMBDA              '<code_object <lambda>>'
              650  LOAD_STR                 'UCODUnitedStates.get_calculated_scale_function_values.<locals>.<lambda>'
              652  MAKE_FUNCTION_8          'closure'
              654  CALL_METHOD_1         1  '1 positional argument'
              656  LOAD_METHOD              sort_values
              658  CALL_METHOD_0         0  '0 positional arguments'
              660  LOAD_METHOD              rename
              662  LOAD_FAST                'calculated_col'
              664  CALL_METHOD_1         1  '1 positional argument'
              666  LOAD_METHOD              to_frame
              668  CALL_METHOD_0         0  '0 positional arguments'
              670  STORE_FAST               'agesbygroup'

 L. 960       672  LOAD_DEREF               'deathmax'
              674  LOAD_FAST                'agesbygroup'
              676  LOAD_STR                 'MaxAgeMinutes'
              678  STORE_SUBSCR     

 L. 961       680  LOAD_FAST                'agesbygroup'
              682  LOAD_STR                 'MaxAgeMinutes'
              684  BINARY_SUBSCR    
              686  LOAD_CONST               525960
              688  BINARY_TRUE_DIVIDE
              690  LOAD_FAST                'agesbygroup'
              692  LOAD_STR                 'MaxAgeYears'
              694  STORE_SUBSCR     

 L. 962       696  LOAD_FAST                'subset'
              698  LOAD_METHOD              groupby
              700  LOAD_FAST                'codescol'
              702  CALL_METHOD_1         1  '1 positional argument'
              704  LOAD_METHOD              apply
              706  LOAD_LAMBDA              '<code_object <lambda>>'
              708  LOAD_STR                 'UCODUnitedStates.get_calculated_scale_function_values.<locals>.<lambda>'
              710  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              712  CALL_METHOD_1         1  '1 positional argument'
              714  LOAD_FAST                'agesbygroup'
              716  LOAD_STR                 'AverageAgeMinutes'
              718  STORE_SUBSCR     

 L. 963       720  LOAD_FAST                'agesbygroup'
              722  LOAD_STR                 'AverageAgeMinutes'
              724  BINARY_SUBSCR    
              726  LOAD_CONST               525960
              728  BINARY_TRUE_DIVIDE
              730  LOAD_FAST                'agesbygroup'
              732  LOAD_STR                 'AverageAgeYears'
              734  STORE_SUBSCR     

 L. 964       736  LOAD_FAST                'subset'
              738  LOAD_METHOD              groupby
              740  LOAD_FAST                'codescol'
              742  CALL_METHOD_1         1  '1 positional argument'
              744  LOAD_METHOD              apply
              746  LOAD_LAMBDA              '<code_object <lambda>>'
              748  LOAD_STR                 'UCODUnitedStates.get_calculated_scale_function_values.<locals>.<lambda>'
              750  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              752  CALL_METHOD_1         1  '1 positional argument'
              754  LOAD_FAST                'agesbygroup'
              756  LOAD_STR                 'SumAgeMinutes'
              758  STORE_SUBSCR     

 L. 965       760  LOAD_FAST                'agesbygroup'
              762  LOAD_STR                 'SumAgeMinutes'
              764  BINARY_SUBSCR    
              766  LOAD_CONST               525960
              768  BINARY_TRUE_DIVIDE
              770  LOAD_FAST                'agesbygroup'
              772  LOAD_STR                 'SumAgeYears'
              774  STORE_SUBSCR     

 L. 966       776  LOAD_FAST                'subset'
              778  LOAD_METHOD              groupby
              780  LOAD_FAST                'codescol'
              782  CALL_METHOD_1         1  '1 positional argument'
              784  LOAD_METHOD              apply
              786  LOAD_LAMBDA              '<code_object <lambda>>'
              788  LOAD_STR                 'UCODUnitedStates.get_calculated_scale_function_values.<locals>.<lambda>'
              790  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              792  CALL_METHOD_1         1  '1 positional argument'
              794  LOAD_FAST                'agesbygroup'
              796  LOAD_STR                 'Count'
              798  STORE_SUBSCR     

 L. 968       800  LOAD_DEREF               'self'
              802  LOAD_ATTR                options
              804  LOAD_ATTR                data_type
              806  LOAD_GLOBAL              DataType
              808  LOAD_ATTR                US_ICD10_SUB_CHAPTERS
              810  COMPARE_OP               ==
          812_814  POP_JUMP_IF_TRUE    896  'to 896'

 L. 969       816  LOAD_DEREF               'self'
              818  LOAD_ATTR                options
              820  LOAD_ATTR                data_type
              822  LOAD_GLOBAL              DataType
              824  LOAD_ATTR                US_ICD10_MINIMALLY_GROUPED
              826  COMPARE_OP               ==
          828_830  POP_JUMP_IF_TRUE    896  'to 896'

 L. 970       832  LOAD_DEREF               'self'
              834  LOAD_ATTR                options
              836  LOAD_ATTR                data_type
              838  LOAD_GLOBAL              DataType
              840  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_ALL
              842  COMPARE_OP               ==
          844_846  POP_JUMP_IF_TRUE    896  'to 896'

 L. 971       848  LOAD_DEREF               'self'
              850  LOAD_ATTR                options
              852  LOAD_ATTR                data_type
              854  LOAD_GLOBAL              DataType
              856  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_LEAVES
              858  COMPARE_OP               ==
          860_862  POP_JUMP_IF_TRUE    896  'to 896'

 L. 972       864  LOAD_DEREF               'self'
              866  LOAD_ATTR                options
              868  LOAD_ATTR                data_type
              870  LOAD_GLOBAL              DataType
              872  LOAD_ATTR                US_ICD_113_SELECTED_CAUSES_ROOTS
              874  COMPARE_OP               ==
          876_878  POP_JUMP_IF_TRUE    896  'to 896'

 L. 973       880  LOAD_DEREF               'self'
              882  LOAD_ATTR                options
              884  LOAD_ATTR                data_type
              886  LOAD_GLOBAL              DataType
              888  LOAD_ATTR                US_ICD10_CHAPTERS
              890  COMPARE_OP               ==
          892_894  POP_JUMP_IF_FALSE   928  'to 928'
            896_0  COME_FROM           876  '876'
            896_1  COME_FROM           860  '860'
            896_2  COME_FROM           844  '844'
            896_3  COME_FROM           828  '828'
            896_4  COME_FROM           812  '812'

 L. 974       896  LOAD_FAST                'agesbygroup'
              898  LOAD_ATTR                apply
              900  LOAD_CLOSURE             'self'
              902  BUILD_TUPLE_1         1 
              904  LOAD_LAMBDA              '<code_object <lambda>>'
              906  LOAD_STR                 'UCODUnitedStates.get_calculated_scale_function_values.<locals>.<lambda>'
              908  MAKE_FUNCTION_8          'closure'
              910  LOAD_CONST               True
              912  LOAD_STR                 'columns'
              914  LOAD_CONST               ('raw', 'axis')
              916  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              918  LOAD_FAST                'agesbygroup'
              920  LOAD_DEREF               'self'
              922  LOAD_ATTR                obfuscated_column_name
              924  STORE_SUBSCR     
              926  JUMP_FORWARD        984  'to 984'
            928_0  COME_FROM           892  '892'

 L. 975       928  LOAD_DEREF               'self'
              930  LOAD_ATTR                options
              932  LOAD_ATTR                data_type
              934  LOAD_GLOBAL              DataType
              936  LOAD_ATTR                US_ICD_LONGTERM_COMPARABLE_LEADING
              938  COMPARE_OP               ==
          940_942  POP_JUMP_IF_FALSE   978  'to 978'

 L. 976       944  LOAD_FAST                'agesbygroup'
              946  LOAD_ATTR                apply
              948  LOAD_CLOSURE             'self'
              950  LOAD_CLOSURE             'ulcl_codes'
              952  BUILD_TUPLE_2         2 
              954  LOAD_LAMBDA              '<code_object <lambda>>'
              956  LOAD_STR                 'UCODUnitedStates.get_calculated_scale_function_values.<locals>.<lambda>'
              958  MAKE_FUNCTION_8          'closure'
              960  LOAD_CONST               True
              962  LOAD_STR                 'columns'
              964  LOAD_CONST               ('raw', 'axis')
              966  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              968  LOAD_FAST                'agesbygroup'
              970  LOAD_DEREF               'self'
              972  LOAD_ATTR                obfuscated_column_name
              974  STORE_SUBSCR     
              976  JUMP_FORWARD        984  'to 984'
            978_0  COME_FROM           940  '940'

 L. 978       978  LOAD_GLOBAL              NotImplementedError
              980  CALL_FUNCTION_0       0  '0 positional arguments'
              982  RAISE_VARARGS_1       1  'exception instance'
            984_0  COME_FROM           976  '976'
            984_1  COME_FROM           926  '926'

 L. 980       984  LOAD_DEREF               'self'
              986  LOAD_METHOD              write_spreadsheet
              988  LOAD_FAST                'agesbygroup'
              990  LOAD_DEREF               'self'
              992  LOAD_METHOD              prefix_all
              994  LOAD_STR                 'agesbygroup'
              996  CALL_METHOD_1         1  '1 positional argument'
              998  CALL_METHOD_2         2  '2 positional arguments'
             1000  POP_TOP          

 L. 981      1002  LOAD_FAST                'agesbygroup'
             1004  LOAD_DEREF               'self'
             1006  LOAD_ATTR                obfuscated_column_name
             1008  LOAD_FAST                'calculated_col'
             1010  BUILD_LIST_2          2 
             1012  BINARY_SUBSCR    
             1014  STORE_FAST               'result'

 L. 982      1016  LOAD_FAST                'result'
             1018  LOAD_ATTR                set_index
             1020  LOAD_DEREF               'self'
             1022  LOAD_ATTR                obfuscated_column_name
             1024  LOAD_CONST               True
             1026  LOAD_CONST               ('inplace',)
             1028  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1030  POP_TOP          

 L. 984      1032  LOAD_FAST                'result'
             1034  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 178

    def get_icd9_10_comparability_ratios(self):
        df = pandas.read_excel((self.options.data_comparability_ratio_tables),
          header=None,
          skiprows=5,
          usecols='A:J',
          na_values=[
         '*'],
          skipfooter=4)
        df = df[[0, 9]]
        df.fillna(1, inplace=True)
        df.columns = ['List number', 'Final comparability ratio']
        return df

    def raw_icd9_counts(self, df, count_years, scale, comparability_ratios):
        for k, v in UCODUnitedStates.icd9_ucod113.recursive_dict(False).items():
            comparability_ratio = comparability_ratios[(comparability_ratios['List number'] == k)]['Final comparability ratio'].iloc[0]
            count_years[self.extract_name(v)] = len(df.query(self.icd_query(self.extract_codes(v)))) * scale * comparability_ratio

    def raw_icd10_counts(self, df, count_years, scale, comparability_ratios):
        for k, v in UCODUnitedStates.icd10_ucod113.recursive_dict(False).items():
            count_years[self.extract_name(v)] = len(df.query(self.icd_query(self.extract_codes(v)))) * scale

    def raw_icd_basis(self):
        x = {self.extract_name(i):numpy.NaN for i in UCODUnitedStates.icd10_ucod113.recursive_list(False)}
        return x

    def run_test(self):
        pass