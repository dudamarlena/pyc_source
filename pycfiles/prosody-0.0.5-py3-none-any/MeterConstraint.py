# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: lib/MeterConstraint.py
# Compiled at: 2019-06-02 18:11:38
import os, tools
PSTRESS_THRESH_DEFAULT = 2

class MeterConstraint:

    def __init__(self, id=None, name=None, logic=None, weight=1, meter=None, mu=0.0, sigma=1.0):
        self.id = id
        self.constr = None
        self.meter = meter
        self.mu = mu
        self.sigma = sigma
        if not name:
            self.name = id
        else:
            self.name = name
            if os.path.exists(name + '.py'):
                originalPath = os.getcwd()
                constraintPath, constraintName = os.path.split(name)
                os.chdir(constraintPath)
                self.constr = __import__(constraintName)
                os.chdir(originalPath)
        self.weight = weight
        self.logic = logic
        return

    def __repr__(self):
        return '[*' + self.name + ']'

    @property
    def name_weight(self):
        weight = str(self.weight) if int(self.weight) != self.weight else str(int(self.weight))
        return '[*' + self.name + '/' + weight + ']'

    def violationScore(self, meterPos, pos_i=None, slot_i=None, num_slots=None, all_positions=None, parse=None):
        """call this on a MeterPosition to return an integer representing the violation value
                for this Constraint in this MPos (0 represents no violation)"""
        violation = None
        if self.constr != None:
            violation = self.constr.parse(meterPos)
        else:
            violation = self.__hardparse(meterPos, pos_i=pos_i, slot_i=slot_i, num_slots=num_slots, all_positions=all_positions, parse=parse)
        if violation != '*':
            meterPos.constraintScores[self] += violation
        return violation

    def __hardparse(self, meterPos, pos_i=None, slot_i=None, num_slots=None, all_positions=None, parse=None):
        import prosodic as p
        if '.' in self.name:
            if 'extrametrical-first-pos' in parse.constraintNames and pos_i == 0:
                return 0
            else:
                if 'skip_initial_foot' in parse.constraintNames and pos_i in (0, 1):
                    return 0
                promSite = self.name.split('.')[1]
                promType = self.name.split('.')[0]
                promSite_meter = promSite.split('=>')[0].strip()
                promSite_prom = promSite.split('=>')[1].strip()
                if meterPos.meterVal != promSite_meter:
                    return 0
                if promSite_prom[0:1] == '-':
                    promSite_isneg = True
                    promSite_prom = promSite_prom[1:]
                else:
                    promSite_isneg = False
                promSite_prom = promSite_prom == 'p'
                if promSite_isneg:
                    numtrue = 0
                    for slot in meterPos.slots:
                        slot_prom = slot.feature('prom.' + promType, True)
                        if slot_prom == None:
                            continue
                        pstress_thresh = self.meter.config.get('phrasal_stress_threshold', PSTRESS_THRESH_DEFAULT)
                        try:
                            pstress_thresh = float(pstress_thresh)
                        except ValueError:
                            pstress_thresh = PSTRESS_THRESH_DEFAULT

                        bool_prom_type = bool(slot_prom) if promType != 'phrasal_stress' else slot_prom <= pstress_thresh
                        if bool_prom_type == promSite_prom:
                            return self.weight

                    return self.weight * numtrue
                violated = True
                ran = False
                for slot in meterPos.slots:
                    slot_prom = slot.feature('prom.' + promType, True)
                    if slot_prom == None:
                        continue
                    ran = True
                    if bool(slot_prom) == promSite_prom:
                        violated = False

                if ran and violated:
                    return self.weight
                return 0

        else:
            if self.name.lower().startswith('initialstrong'):
                if pos_i == 0:
                    if meterPos.meterVal == 's':
                        return self.weight
                return 0
            if self.name.lower().startswith('functiontow'):
                if p.config.get('skip_initial_foot', 0) and meterPos.slots[0].i < 2:
                    return 0
            if meterPos.meterVal != 's':
                return 0
            vio = 0
            for slot in meterPos.slots:
                if slot.word.feature('functionword'):
                    vio += self.weight

            return vio
        if self.name.lower().startswith('footmin'):
            if len(meterPos.slots) < 2:
                return 0
            if len(meterPos.slots) > 2:
                return self.weight
            name = self.name.lower()
            a = meterPos.slots[0]
            b = meterPos.slots[1]
            if name == 'footmin-nohx':
                if bool(a.feature('prom.weight', True)):
                    return self.weight
            if name == 'footmin-w-resolution':
                if a.word != b.word:
                    return 0
                firstsyll_islight = bool(a.feature('prom.weight', True)) == False
                firstsyll_isstressed = bool(a.feature('prom.stress', True)) == True
                if not (firstsyll_islight and firstsyll_isstressed):
                    return self.weight
            if name == 'footmin-f-resolution':
                if a.word == b.word:
                    return 0
                if meterPos.meterVal == 's':
                    return self.weight
                a_is_fw = bool(a.word.feature('functionword'))
                b_is_fw = bool(b.word.feature('functionword'))
                if not (a_is_fw and b_is_fw):
                    return self.weight
            if name == 'footmin-s-nohx':
                if meterPos.meterVal == 's':
                    if bool(a.feature('prom.weight', True)) or a.word != b.word:
                        return self.weight
            if 'nolh' in name:
                if bool(b.feature('prom.weight', True)):
                    return self.weight
            if 'strongconstraint' in name:
                if bool(b.feature('prom.strength', True)):
                    return self.weight
                if bool(a.feature('prom.strength', True)):
                    if not bool(a.feature('prom.weight', True)):
                        if a.word == b.word and not a.wordpos[0] == a.wordpos[1]:
                            if not bool(b.feature('prom.stress', True)):
                                return 0
                    return self.weight
            if name == 'footmin-none':
                return self.weight
            if name == 'footmin-none-unless-in-first-two-positions':
                if pos_i != 0 and pos_i != 1:
                    return self.weight
            if name == 'footmin-none-unless-in-second-position':
                if pos_i != 1:
                    return self.weight
            if name == 'footmin-no-s':
                return self.weight * int(meterPos.meterVal == 's')
            if name == 'footmin-no-w':
                return self.weight * int(meterPos.meterVal == 'w')
            if name == 'footmin-no-s-unless-preceded-by-ww':
                if meterPos.meterVal != 's':
                    return 0
                if pos_i == 0:
                    return self.weight
                prevpos = all_positions[(pos_i - 1)]
                if len(prevpos.slots) > 1 and prevpos.meterVal == 'w':
                    return 0
                return self.weight
            if 'wordbound' in name:
                if name == 'footmin-wordbound':
                    if a.word != b.word:
                        return self.weight
                if 'nomono' in name:
                    if a.word.numSyll == 1 or b.word.numSyll == 1:
                        return self.weight
                if 'lexmono' in name:
                    if a.word.isLexMono() or b.word.isLexMono():
                        return self.weight
                if a.word.feature('functionword') and b.word.feature('functionword'):
                    return 0
                if a.word != b.word:
                    if 'bothnotfw' in name:
                        if not (a.word.feature('functionword') and b.word.feature('functionword')):
                            return self.weight
                    elif not (a.word.feature('functionword') or b.word.feature('functionword')):
                        return self.weight
                if a.wordpos[0] == a.wordpos[1]:
                    if 'bothnotfw' in name:
                        if not (a.word.feature('functionword') and b.word.feature('functionword')):
                            return self.weight
                    elif not (a.word.feature('functionword') or b.word.feature('functionword')):
                        return self.weight
                return 0
        if self.name == 'word-elision':
            words = set([ slot.word for slot in meterPos.slots if hasattr(slot.word, 'is_elision') and slot.word.is_elision ])
            sylls = []
            for slot in meterPos.slots:
                sylls += slot.children

            for word in words:
                lastsyll = word.children[(-1)]
                if lastsyll in sylls:
                    return self.weight

        is_end = slot_i + 1 == num_slots and meterPos.slots == all_positions[(-1)].slots
        if self.name == 'attridge-ss-not-by-ww':
            if pos_i == 0:
                return 0
            prevpos = all_positions[(pos_i - 1)]
            prevprevpos = all_positions[(pos_i - 2)] if pos_i - 2 >= 0 else None
            if prevpos.meterVal2 == 'ss':
                if prevprevpos and prevprevpos.meterVal2 == 'ww' and not hasattr(prevprevpos, '_flag_already_served_as_ww'):
                    prevprevpos._flag_already_served_as_ww = True
                elif meterPos.meterVal2 == 'ww' and not hasattr(meterPos, '_flag_already_served_as_ww'):
                    meterPos._flag_already_served_as_ww = True
                else:
                    for cnstr in prevpos.constraintScores:
                        if cnstr.name == self.name:
                            prevpos.constraintScores[cnstr] = self.weight
                            parse.constraintScores[cnstr] += self.weight

            elif is_end and meterPos.meterVal2 == 'ss':
                if prevpos.meterVal2 == 'ww':
                    pass
                else:
                    return self.weight
        if is_end:
            final_meter_str = ('').join([ ('').join(pos.meterVal for slot in pos.slots) for pos in all_positions ])
            if self.name.startswith('headedness'):
                shouldbe = self.name.split('!=')[(-1)]
                quasi_feet = [ ('').join(x) for x in tools.slice([ pos.meterVal for pos in all_positions ], slice_length=2, runts=False) ]
                headedness = 'rising' if quasi_feet.count('ws') >= quasi_feet.count('sw') else 'falling'
                if shouldbe != headedness:
                    return self.weight
            if self.name.startswith('number_feet'):
                shouldbe = int(self.name.split('!=')[(-1)])
                strong_pos = [ pos for pos in all_positions if pos.meterVal == 's' ]
                num_feet = len(strong_pos)
                if shouldbe != num_feet:
                    return self.weight
            if self.name.startswith('posthoc'):
                if self.name == 'posthoc-no-final-ww':
                    if len(all_positions[(-1)].slots) > 1 and all_positions[(-1)].meterVal == 'w':
                        return self.weight
                if self.name == 'posthoc-no-final-w':
                    if all_positions[(-1)].meterVal == 'w':
                        return self.weight
                if self.name == 'posthoc-standardize-weakpos':
                    weak_pos = [ pos for pos in all_positions if pos.meterVal == 'w' ]
                    if len(weak_pos) < 2:
                        return 0
                    weak_pos_types = [ ('').join('w' for slot in pos.slots) for pos in weak_pos ]
                    maxcount = max([ weak_pos_types.count(wtype) for wtype in set(weak_pos_types) ])
                    diff = len(weak_pos) - maxcount
                    return self.weight * diff
        return 0