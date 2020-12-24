# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wiktfinnish/formnames.py
# Compiled at: 2018-10-31 12:02:02
# Size of source mod 2**32: 8010 bytes
COMP_FORMS = ('', 'comp', 'sup')
CASE_FORMS = ('nom-sg', 'acc-sg', 'gen-sg', 'ptv-sg', 'ine-sg', 'ela-sg', 'ill-sg',
              'ade-sg', 'abl-sg', 'all-sg', 'ess-sg', 'tra-sg', 'ins-sg', 'abe-sg',
              'cmt-sg', 'nom-pl', 'acc-pl', 'gen-pl', 'ptv-pl', 'ine-pl', 'ela-pl',
              'ill-pl', 'ade-pl', 'abl-pl', 'all-pl', 'ess-pl', 'tra-pl', 'ins-pl',
              'abe-pl', 'cmt-pl')
POSSESSIVE_FORMS = ('', '1s', '2s', '3x', '1p', '2p')
VERB_FORMS = ('pres-1sg', 'pres-2sg', 'pres-3sg', 'pres-1pl', 'pres-2pl', 'pres-3pl',
              'pres-1sg-neg', 'pres-2sg-neg', 'pres-3sg-neg', 'pres-1pl-neg', 'pres-2pl-neg',
              'pres-3pl-neg', 'pres-pass', 'pres-pass-neg', 'past-1sg', 'past-2sg',
              'past-3sg', 'past-1pl', 'past-2pl', 'past-3pl', 'past-1sg-neg', 'past-2sg-neg',
              'past-3sg-neg', 'past-1pl-neg', 'past-2pl-neg', 'past-3pl-neg', 'past-pass',
              'past-pass-neg', 'cond-1sg', 'cond-2sg', 'cond-3sg', 'cond-1pl', 'cond-2pl',
              'cond-3pl', 'cond-1sg-neg', 'cond-2sg-neg', 'cond-3sg-neg', 'cond-1pl-neg',
              'cond-2pl-neg', 'cond-3pl-neg', 'cond-pass', 'cond-pass-neg', 'impr-2sg',
              'impr-3sg', 'impr-1pl', 'impr-2pl', 'impr-3pl', 'impr-2sg-neg', 'impr-3sg-neg',
              'impr-1pl-neg', 'impr-2pl-neg', 'impr-3pl-neg', 'impr-pass', 'impr-pass-neg',
              'potn-1sg', 'potn-2sg', 'potn-3sg', 'potn-1pl', 'potn-2pl', 'potn-3pl',
              'potn-1sg-neg', 'potn-2sg-neg', 'potn-3sg-neg', 'potn-1pl-neg', 'potn-2pl-neg',
              'potn-3pl-neg', 'potn-pass', 'potn-pass-neg', 'pres-part', 'pres-pass-part',
              'past-part', 'past-pass-part', 'agnt-part', 'nega-part', 'inf1', 'inf1-long',
              'inf2-ine', 'inf2-pass-ine', 'inf2-ins', 'inf3-ine', 'inf3-ela', 'inf3-ill',
              'inf3-ade', 'inf3-abe', 'inf3-ins', 'inf3-pass-ins', 'inf4-nom', 'inf4-par',
              'inf5')
CLITIC_FORMS = ('', 'kO', 'kin', 'kAAn', 'pA', 's', 'kA', 'hAn', 'kOhAn', 'pAhAn',
                'pAs', 'kOs', 'kinkO', 'kAAnkO', 'kinkOhAn')
all_forms_cache = {}

def all_forms_list(*args, **kwargs):
    """Returns a list/tuple of all possible word form descriptors for the given
    part-of-speech and other restrictions.  This caches the result."""
    key = (
     args, tuple(sorted(kwargs.items())))
    if key in all_forms_cache:
        return all_forms_cache[key]
    else:
        forms = tuple(x for x in all_forms_iter(*args, **kwargs))
        all_forms_cache[key] = forms
        return forms


def all_forms_iter(pos, comparable=True, transitive=True, no_clitics=False):
    """Returns an iterator that iterates over all possible word form
    descriptors for the given part-of-speech and other parameters."""
    assert isinstance(pos, str)
    clitics = [''] if no_clitics else CLITIC_FORMS

    def fn():
        if pos in ('noun', 'name', 'num', 'letter'):
            for case in CASE_FORMS:
                for poss in POSSESSIVE_FORMS:
                    if case in ('acc-sg', 'acc-pl'):
                        pass
                    else:
                        if case == 'cmt-pl':
                            if not poss:
                                continue
                        for clitic in clitics:
                            if clitic in ('s', 'kA'):
                                pass
                            else:
                                yield (
                                 '', '', case, poss, clitic)

        else:
            if pos == 'pron':
                for case in CASE_FORMS:
                    if case in ('ins-sg', 'ins-pl', 'cmt'):
                        pass
                    else:
                        for clitic in clitics:
                            if clitic in ('s', 'kA'):
                                pass
                            else:
                                yield (
                                 '', '', case, '', clitic)

            else:
                if pos == 'adj':
                    comps = COMP_FORMS if comparable else ['']
                    for comp in comps:
                        for case in CASE_FORMS:
                            if case in ('acc-sg', 'acc-pl'):
                                pass
                            else:
                                for poss in POSSESSIVE_FORMS:
                                    for clitic in clitics:
                                        if clitic in ('s', ):
                                            continue
                                        yield (
                                         '', comp, case, poss, clitic)

                else:
                    if pos == 'verb':
                        for vform in VERB_FORMS:
                            if not transitive:
                                if vform == 'agnt-part':
                                    continue
                                comps = [
                                 '']
                                cases = ['']
                                posses = ['']
                                if vform in ('pres-part', 'pres-pass-part', 'past-part',
                                             'past-pass-part', 'agnt-part', 'nega-part'):
                                    cases = CASE_FORMS
                            else:
                                if vform in ('inf1-long', 'inf2-ine', 'inf3-ine', 'inf3-ela',
                                             'inf3-ill', 'inf3-ade', 'inf3-abe',
                                             'inf4-par', 'inf5', 'agnt-part', 'pres-pass-part',
                                             'pres-part'):
                                    posses = POSSESSIVE_FORMS
                                if vform in ('pres-part', 'past-part', 'pres-pass-part',
                                             'past-pass-part'):
                                    comps = COMP_FORMS if comparable else ['']
                            for comp in comps:
                                for case in cases:
                                    if case in ('acc-sg', 'acc-pl'):
                                        pass
                                    else:
                                        for poss in posses:
                                            if not poss:
                                                if vform in ('inf1-long', 'inf5'):
                                                    continue
                                            if poss:
                                                if case != 'nom-sg':
                                                    if vform in ('pres-part', 'past-pass-part'):
                                                        continue
                                            for clitic in clitics:
                                                yield (
                                                 vform, comp, case, poss, clitic)

                    else:
                        if pos in ('conj', 'intj', 'suffix', 'clitic', 'punct'):
                            yield ('', '', '', '', '')
                        else:
                            if pos in ('postp', 'prep', 'adv'):
                                for clitic in clitics:
                                    yield (
                                     '', '', '', '', clitic)
                                    if pos == 'adv':
                                        yield (
                                         '', 'comp', '', '', clitic)
                                        yield ('', 'sup', '', '', clitic)

                            else:
                                print('all_forms_iter: unimplemented pos:', pos)
                                yield ('', '', '', '', '')

    return fn()