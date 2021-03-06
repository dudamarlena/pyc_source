# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cctyper/plot.py
# Compiled at: 2020-05-13 08:02:57
# Size of source mod 2**32: 20106 bytes
import os, logging, re, pandas as pd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Map(object):

    def __init__(self, obj):
        self.master = obj
        for key, val in vars(obj).items():
            setattr(self, key, val)

        self.font = ImageFont.truetype(os.path.join(self.db, 'arial.ttf'), 30)
        self.fontB = ImageFont.truetype(os.path.join(self.db, 'arial.ttf'), 50)
        self.fontS = ImageFont.truetype(os.path.join(self.db, 'arial.ttf'), 20)

    def draw_gene(self, start, end, strand, name, n, z, col):
        if strand > 0:
            self.draw.polygon(((self.scale / 50 * start, n * 20 * self.scale),
             (
              self.scale / 50 * end - 5 * self.scale, n * 20 * self.scale),
             (
              self.scale / 50 * end, 2.5 * self.scale + n * 20 * self.scale),
             (
              self.scale / 50 * end - 5 * self.scale, 5 * self.scale + n * 20 * self.scale),
             (
              self.scale / 50 * start, 5 * self.scale + n * 20 * self.scale)),
              fill=col,
              outline=(255, 255, 255))
        else:
            self.draw.polygon(((self.scale / 50 * start + 5 * self.scale, n * 20 * self.scale),
             (
              self.scale / 50 * end, n * 20 * self.scale),
             (
              self.scale / 50 * end, 5 * self.scale + n * 20 * self.scale),
             (
              self.scale / 50 * start + 5 * self.scale, 5 * self.scale + n * 20 * self.scale),
             (
              self.scale / 50 * start, 2.5 * self.scale + n * 20 * self.scale)),
              fill=col,
              outline=(255, 255, 255))
        if isinstance(name, str):
            name = re.sub('_[0-9]*_.*', '', name)
        else:
            name = str(name)
        if z % 2 == 1:
            self.draw.text((self.scale / 50 * start + 5, n * 20 * self.scale - 3 * self.scale), name, (0,
                                                                                                       0,
                                                                                                       0), font=(self.font))
        else:
            self.draw.text((self.scale / 50 * start + 5, n * 20 * self.scale + 5 * self.scale), name, (0,
                                                                                                       0,
                                                                                                       0), font=(self.font))

    def draw_array(self, start, end, subtype, n, z):
        self.draw.polygon(((self.scale / 50 * start, n * 20 * self.scale),
         (
          self.scale / 50 * end, n * 20 * self.scale),
         (
          self.scale / 50 * end, 5 * self.scale + n * 20 * self.scale),
         (
          self.scale / 50 * start, 5 * self.scale + n * 20 * self.scale)),
          fill=(0, 0, 255),
          outline=(255, 255, 255))
        self.draw.text((self.scale / 50 * start + self.scale / 10, n * 20 * self.scale - 3 * self.scale), subtype, (0,
                                                                                                                    0,
                                                                                                                    0), font=(self.font))

    def draw_name(self, n, pred, contig, start, end):
        self.draw.text((self.scale / 10, n * 20 * self.scale - 10 * self.scale), ('{}: {}({}-{})'.format(pred, contig, start, end)), (0,
                                                                                                                                      0,
                                                                                                                                      0),
          font=(self.fontB))

    def draw_system(self, cas, crispr, n):
        z = 0
        if len(cas) > 0:
            for i in cas:
                z += 1
                self.draw_gene(i[0], i[1], i[2], i[3], n, z, i[4])

        if len(crispr) > 0:
            for i in crispr:
                z += 1
                self.draw_array(i[0], i[1], i[2], n, z)

    def criscas_len(self, cc, cca):
        lengths = []
        self.criscaspos = {}
        for index, row in cc.iterrows():
            span_ends = False
            start = row['Operon_Pos'][0]
            end = row['Operon_Pos'][1]
            if start > end:
                span_ends = True
            if not row['Operon'] in self.cc_circ_start.keys():
                if not row['Operon'] in self.cc_circ_end.keys():
                    start = min(start, min(cca[cca['CRISPR'].isin(row['CRISPRs'])]['Start']))
                    end = max(end, max(cca[cca['CRISPR'].isin(row['CRISPRs'])]['End']))
                else:
                    if row['Operon'] in self.cc_circ_start.keys():
                        ccs = cca[cca['CRISPR'].isin(self.cc_circ_start[row['Operon']])]
                        end = max(ccs['End'])
                        span_ends = True
                    if row['Operon'] in self.cc_circ_end.keys():
                        ccs = cca[cca['CRISPR'].isin(self.cc_circ_end[row['Operon']])]
                        start = min(ccs['Start'])
                        span_ends = True
                    seq_size = self.len_dict[row['Contig']]
                    if span_ends:
                        lengths.append(end + seq_size - start)
                    else:
                        lengths.append(end - start)
                self.criscaspos[row['Operon']] = [
                 start, end, seq_size, span_ends]
            return lengths

    def get_longest(self, crisO, casO, criscasO, crisA):
        crisO_M, casO_M, cc_M = (0, 0, 0)
        if len(crisO) > 0:
            crisO_M = max(crisO['End'] - crisO['Start'])
        if len(casO) > 0:
            casO_lin = casO[(casO['Start'] < casO['End'])]
            casO_circ = casO[(casO['Start'] > casO['End'])]
            casO_lin_M, casO_circ_M = (0, 0)
            if len(casO_lin) > 0:
                casO_lin_M = max(casO_lin['End'] - casO_lin['Start'])
            if len(casO_circ) > 0:
                casO_circ['size'] = casO_circ.apply((lambda x: self.len_dict[x['Contig']]), axis=1)
                casO_circ_M = max(casO_circ['Start'] + casO_circ['size'] - casO_circ['Start'])
            casO_M = max(casO_lin_M, casO_circ_M)
        if len(criscasO) > 0:
            cc_M = max(self.criscas_len(criscasO, crisA))
        return max(crisO_M, casO_M, cc_M)

    def expandCas(self, contig, pos, startPos, endPos, seq_size, span_ends, array=False):
        all_cas = list(self.genes[(self.genes['Contig'] == contig)]['Pos'])
        if array:
            missing_cas = all_cas
        else:
            missing_cas = [x for x in all_cas if x not in pos]
        add_these = self.genes[((self.genes['Contig'] == contig) & self.genes['Pos'].isin(missing_cas))]
        if span_ends:
            add_these = add_these[((add_these['Start'] > startPos - self.expand) | (add_these['End'] < endPos + self.expand))]
            which_end = [x > endPos + self.expand for x in list(add_these['Start'])]
            add_starts = [self.expand + 1 + x[0] - startPos if x[1] else self.expand + 1 + x[0] + seq_size - startPos for x in zip(list(add_these['Start']), which_end)]
            add_ends = [self.expand + 1 + x[0] - startPos if x[1] else self.expand + 1 + x[0] + seq_size - startPos for x in zip(list(add_these['End']), which_end)]
        else:
            add_these = add_these[((add_these['Start'] > startPos - self.expand) & (add_these['End'] < endPos + self.expand))]
            add_starts = [self.expand + 1 + x - startPos for x in list(add_these['Start'])]
            add_ends = [self.expand + 1 + x - startPos for x in list(add_these['End'])]
        names = list(add_these['Pos'])
        cols = list(((150, 150, 150), ) * len(add_starts))
        hmm_contig = self.hmm_df_raw[(self.hmm_df_raw['Acc'] == contig)]
        try:
            known_contig = self.knowngenes[contig]
        except:
            known_contig = [
             0]
        else:
            add_putative = [x in list(hmm_contig['Pos']) for x in list(add_these['Pos'])]
            add_known = [x in known_contig for x in list(add_these['Pos'])]
            casNames = [list(hmm_contig[(hmm_contig['Pos'] == x)]['Hmm']) for x in list(add_these['Pos'])]
            casNames = [x[0] if len(x) > 0 else x for x in casNames]
            cols = [x[0] if not x[1] else (0, 150, 0) for x in zip(cols, add_putative)]
            cols = [x[0] if not x[1] else (255, 0, 0) for x in zip(cols, add_known)]
            names = [x[0] if not x[1] else x[2] for x in zip(names, add_putative, casNames)]
            expand_list = list(zip(add_starts, add_ends, list(add_these['Strand']), names, cols))
            return expand_list

    def expandCris(self, contig, crisprs, startPos, endPos, seq_size, span_ends):
        add_crisp = self.crisprsall[(self.crisprsall['Contig'] == contig)]
        add_crisp = add_crisp[(~add_crisp['CRISPR'].isin(crisprs))]
        if span_ends:
            add_crisp = add_crisp[((add_crisp['Start'] > startPos - self.expand) | (add_crisp['End'] < endPos + self.expand))]
        else:
            add_crisp = add_crisp[((add_crisp['Start'] > startPos - self.expand) & (add_crisp['End'] < endPos + self.expand))]
        if len(add_crisp) > 0:
            crisp_lst = list(add_crisp['CRISPR'])
            startsCris = [list(add_crisp[(add_crisp['CRISPR'] == x)]['Start'])[0] for x in crisp_lst]
            endsCris = [list(add_crisp[(add_crisp['CRISPR'] == x)]['End'])[0] for x in crisp_lst]
            nameCris = [list(add_crisp[(add_crisp['CRISPR'] == x)]['Prediction'])[0] for x in crisp_lst]
            if span_ends:
                which_end = [x > endPos + self.expand for x in startsCris]
                startsCris = [self.expand + 1 + x[0] - startPos if x[1] else self.expand + 1 + x[0] + seq_size - startPos for x in zip(startsCris, which_end)]
                endsCris = [self.expand + 1 + x[0] - startPos if x[1] else self.expand + 1 + x[0] + seq_size - startPos for x in zip(endsCris, which_end)]
            else:
                startsCris = [self.expand + 1 + x - startPos for x in startsCris]
                endsCris = [self.expand + 1 + x - startPos for x in endsCris]
            return list(zip(startsCris, endsCris, nameCris))
        return []

    def plot(self):
        total = 0
        if self.any_operon:
            cas_ambi = self.preddf[(self.preddf['Prediction'] == 'Ambiguous')]
            try:
                casAmbiOrph = pd.concat([self.orphan_cas, cas_ambi])
                casAmbiOrph = casAmbiOrph[(~casAmbiOrph['Operon'].isin(self.crispr_cas['Operon']))]
            except:
                cas_good = self.preddf[(~self.preddf['Prediction'].isin(['False', 'Ambiguous', 'Partial']))]
                casAmbiOrph = pd.concat([cas_good, cas_ambi])
            else:
                total += len(casAmbiOrph)
        else:
            casAmbiOrph = []
        try:
            total += len(self.orphan_crispr)
        except:
            self.orphan_crispr = self.crisprsall
            total += len(self.orphan_crispr)

        try:
            total += len(self.crispr_cas)
        except:
            self.crispr_cas = []
        else:
            if not self.noplot:
                if total > 0:
                    logging.info('Plotting map of CRISPR-Cas loci')
                    width = self.get_longest(self.orphan_crispr, casAmbiOrph, self.crispr_cas, self.crisprsall)
                    self.genes = pd.read_csv((self.out + 'genes.tab'), sep='\t')
                    width = width + self.expand * 2
                    self.im = Image.new('RGB', (int(round(self.scale / 50 * width + self.scale * 10)), int(round((total + 1) * 20 * self.scale))), (255,
                                                                                                                                                    255,
                                                                                                                                                    255))
                    self.draw = ImageDraw.Draw(self.im)
                    if not self.nogrid:
                        y_start = 8 * self.scale
                        y_end = self.im.height
                        step_size = int(round(1000 * self.scale / 50))
                        for x in range(step_size, self.im.width, step_size):
                            line = (
                             (
                              x, y_start), (x, y_end))
                            self.draw.line(line, fill=(150, 150, 150), width=(int(self.scale / 20)))
                            self.draw.text((x - self.scale * 4, self.scale * 5), (str(int(x / (self.scale / 50)))), (100,
                                                                                                                     100,
                                                                                                                     100), font=(self.fontS))

                    self.knowngenes = self.preddf[(self.preddf['Prediction'] != 'False')].groupby('Contig').agg({'Positions': 'sum'}).to_dict()['Positions']
                    k = 0
                    if len(self.crispr_cas) > 0:
                        for i in list(self.crispr_cas['Operon']):
                            k += 1
                            logging.debug('Plotting ' + i)
                            contig = list(self.crispr_cas[(self.crispr_cas['Operon'] == i)]['Contig'])[0]
                            prediction = list(self.crispr_cas[(self.crispr_cas['Operon'] == i)]['Prediction'])[0]
                            posCas = list(self.preddf[(self.preddf['Operon'] == i)]['Positions'])[0]
                            nameCas = list(self.preddf[(self.preddf['Operon'] == i)]['Genes'])[0]
                            hmmSub = self.hmm_df[(self.hmm_df['Acc'] == contig)]
                            startsCas = [list(hmmSub[(hmmSub['Pos'] == x)]['start'])[0] for x in posCas]
                            endsCas = [list(hmmSub[(hmmSub['Pos'] == x)]['end'])[0] for x in posCas]
                            strands = [list(hmmSub[(hmmSub['Pos'] == x)]['strand'])[0] for x in posCas]
                            crisprs = list(self.crispr_cas[(self.crispr_cas['Operon'] == i)]['CRISPRs'])[0]
                            startsCris = [list(self.crisprsall[(self.crisprsall['CRISPR'] == x)]['Start'])[0] for x in crisprs]
                            endsCris = [list(self.crisprsall[(self.crisprsall['CRISPR'] == x)]['End'])[0] for x in crisprs]
                            nameCris = [list(self.crisprsall[(self.crisprsall['CRISPR'] == x)]['Prediction'])[0] for x in crisprs]
                            startPos = self.criscaspos[i][0]
                            endPos = self.criscaspos[i][1]
                            self.draw_name(k, prediction, i, startPos, endPos)
                            seq_size = self.len_dict[contig]
                            if self.criscaspos[i][3]:
                                startsCas = [self.expand + 1 + x - startPos if x >= startPos else self.expand + 1 + x + seq_size - startPos for x in startsCas]
                                endsCas = [self.expand + 1 + x - startPos if x > startPos else self.expand + 1 + x + seq_size - startPos for x in endsCas]
                                startsCris = [self.expand + 1 + x - startPos if x >= startPos else self.expand + 1 + x + seq_size - startPos for x in startsCris]
                                endsCris = [self.expand + 1 + x - startPos if x > startPos else self.expand + 1 + x + seq_size - startPos for x in endsCris]
                                self.draw.line((((self.expand + 1 + seq_size - startPos) * self.scale / 50, k * self.scale * 20 - self.scale * 5),
                                 (
                                  (self.expand + 1 + seq_size - startPos) * self.scale / 50, k * self.scale * 20 + self.scale * 10)),
                                  fill=(0, 0, 0),
                                  width=(int(self.scale / 2)))
                            else:
                                startsCas = [self.expand + 1 + x - startPos for x in startsCas]
                                endsCas = [self.expand + 1 + x - startPos for x in endsCas]
                                startsCris = [self.expand + 1 + x - startPos for x in startsCris]
                                endsCris = [self.expand + 1 + x - startPos for x in endsCris]
                            cas_list = list(zip(startsCas, endsCas, strands, nameCas, list(((255, 0, 0), ) * len(nameCas))))
                            expand_list = self.expandCas(contig, posCas, startPos, endPos, seq_size, self.criscaspos[i][3])
                            cas_list = cas_list + expand_list
                            expand_cris = self.expandCris(contig, crisprs, startPos, endPos, seq_size, self.criscaspos[i][3])
                            cris_list = list(zip(startsCris, endsCris, nameCris)) + expand_cris
                            cas_list = sorted(cas_list, key=(lambda x: x[0]))
                            self.draw_system(cas_list, cris_list, k)

                    if len(casAmbiOrph) > 0:
                        for i in list(casAmbiOrph['Operon']):
                            k += 1
                            logging.debug('Plotting ' + i)
                            contig = list(casAmbiOrph[(casAmbiOrph['Operon'] == i)]['Contig'])[0]
                            pos = list(casAmbiOrph[(casAmbiOrph['Operon'] == i)]['Positions'])[0]
                            casName = list(casAmbiOrph[(casAmbiOrph['Operon'] == i)]['Genes'])[0]
                            hmmSub = self.hmm_df[(self.hmm_df['Acc'] == contig)]
                            starts = [list(hmmSub[(hmmSub['Pos'] == x)]['start'])[0] for x in pos]
                            ends = [list(hmmSub[(hmmSub['Pos'] == x)]['end'])[0] for x in pos]
                            strands = [list(hmmSub[(hmmSub['Pos'] == x)]['strand'])[0] for x in pos]
                            self.draw_name(k, list(casAmbiOrph[(casAmbiOrph['Operon'] == i)]['Prediction'])[0], i, min(starts), max(ends))
                            startPos = list(casAmbiOrph[(casAmbiOrph['Operon'] == i)]['Start'])[0]
                            endPos = list(casAmbiOrph[(casAmbiOrph['Operon'] == i)]['End'])[0]
                            seq_size = self.len_dict[contig]
                            if startPos < endPos:
                                span_ends = False
                                starts = [self.expand + 1 + x - startPos for x in starts]
                                ends = [self.expand + 1 + x - startPos for x in ends]
                            else:
                                span_ends = True
                                starts = [self.expand + 1 + x - startPos if x >= startPos else self.expand + 1 + x + seq_size - startPos for x in starts]
                                ends = [self.expand + 1 + x - startPos if x > startPos else self.expand + 1 + x + seq_size - startPos for x in ends]
                                self.draw.line((((self.expand + 1 + seq_size - startPos) * self.scale / 50, k * self.scale * 20 - self.scale * 5),
                                 (
                                  (self.expand + 1 + seq_size - startPos) * self.scale / 50, k * self.scale * 20 + self.scale * 10)),
                                  fill=(0, 0, 0),
                                  width=(int(self.scale / 2)))
                            cas_list = list(zip(starts, ends, strands, casName, list(((255, 0, 0), ) * len(casName))))
                            expand_list = self.expandCas(contig, pos, startPos, endPos, seq_size, span_ends)
                            cas_list = cas_list + expand_list
                            if self.any_crispr:
                                expand_cris = self.expandCris(contig, [], startPos, endPos, seq_size, span_ends)
                            else:
                                expand_cris = []
                            cas_list = sorted(cas_list, key=(lambda x: x[0]))
                            self.draw_system(cas_list, expand_cris, k)

                    elif len(self.orphan_crispr) > 0:
                        for i in list(self.orphan_crispr['CRISPR']):
                            k += 1
                            logging.debug('Plotting ' + i)
                            contig = list(self.orphan_crispr[(self.orphan_crispr['CRISPR'] == i)]['Contig'])[0]
                            pred = list(self.orphan_crispr[(self.orphan_crispr['CRISPR'] == i)]['Prediction'])[0]
                            start = list(self.orphan_crispr[(self.orphan_crispr['CRISPR'] == i)]['Start'])[0]
                            end = list(self.orphan_crispr[(self.orphan_crispr['CRISPR'] == i)]['End'])[0]
                            if self.expand > 0:
                                expand_list = self.expandCas(contig, [0], start, end, 0, False, True)
                                expand_list = sorted(expand_list, key=(lambda x: x[0]))
                                expand_cris = self.expandCris(contig, [i], start, end, 0, False)
                                self.draw_system(expand_list, expand_cris, k)
                            self.draw_array(self.expand + 1, self.expand + 1 + end - start, pred, k, 1)
                            self.draw_name(k, pred, i, start, end)

                    else:
                        self.im.save(self.out + 'plot.png')