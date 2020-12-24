# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/vcf/filters.py
# Compiled at: 2016-03-18 12:16:02
# Size of source mod 2**32: 6240 bytes
try:
    from rpy2 import robjects
except:
    robjects = None

class Base(object):
    __doc__ = ' Base class for vcf_filter.py filters.\n\n        Use the class docstring to provide the filter description\n        as it appears in vcf_filter.py\n    '
    name = 'f'

    @classmethod
    def customize_parser(self, parser):
        """ hook to extend argparse parser with custom arguments """
        pass

    def __init__(self, args):
        """ create the filter using argparse ``args`` """
        self.threshold = 0

    def __call__(self):
        """ filter a site, return not None if the site should be filtered """
        raise NotImplementedError('Filters must implement this method')

    def filter_name(self):
        """ return the name to put in the VCF header, default is ``name`` + ``threshold`` """
        return '%s%s' % (self.name, self.threshold)


class SiteQuality(Base):
    __doc__ = ' Filter low quailty sites '
    name = 'sq'

    @classmethod
    def customize_parser(self, parser):
        parser.add_argument('--site-quality', type=int, default=30, help='Filter sites below this quality')

    def __init__(self, args):
        self.threshold = args.site_quality

    def __call__(self, record):
        if record.QUAL < self.threshold:
            return record.QUAL


class VariantGenotypeQuality(Base):
    __doc__ = ' Filters sites with only low quality variants.\n\n        It is possible to have a high site quality with many low quality calls.  This\n        filter demands at least one call be above a threshold quality.\n    '
    name = 'mgq'

    @classmethod
    def customize_parser(self, parser):
        parser.add_argument('--genotype-quality', type=int, default=50, help='Filter sites with no genotypes above this quality')

        def __init__(self, args):
            self.threshold = args.genotype_quality

    def __call__(self, record):
        if not record.is_monomorphic:
            vgq = max([x['GQ'] for x in record if x.is_variant])
            if vgq < self.threshold:
                pass
            return vgq


class ErrorBiasFilter(Base):
    __doc__ = ' Filter sites that look like correlated sequencing errors.\n\n        Some sequencing technologies, notably pyrosequencing, produce mutation\n        hotspots where there is a constant level of noise, producing some reference\n        and some heterozygote calls.\n\n        This filter computes a Bayes Factor for each site by comparing\n        the binomial likelihood of the observed allelic depths under:\n\n        * A model with constant error equal to the MAF.\n        * A model where each sample is the ploidy reported by the caller.\n\n        The test value is the log of the bayes factor.  Higher values\n        are more likely to be errors.\n\n        Note: this filter requires rpy2\n    '
    name = 'eb'

    @classmethod
    def customize_parser(self, parser):
        parser.add_argument('--eblr', type=int, default=-10, help='Filter sites above this error log odds ratio')

    def __init__(self, args):
        self.threshold = args.eblr
        if robjects is None:
            raise Exception('Please install rpy2')
        self.ll_test = robjects.r('\n            function(ra, aa, gt, diag=F) {\n                ra_sum = sum(ra)\n                aa_sum = sum(aa)\n                ab = aa_sum / (ra_sum + aa_sum)\n                gtp = 0.5 + (0.48*(gt-1))\n\n                error_likelihood = log(dbinom(aa, ra+aa, ab))\n                gt_likelihood = log(dbinom(aa, ra+aa, gtp))\n\n                if (diag) {\n                    print(ra)\n                    print(aa)\n                    print(gtp)\n                    print(ab)\n                    print(error_likelihood)\n                    print(gt_likelihood)\n                }\n                error_likelihood = sum(error_likelihood)\n                gt_likelihood = sum(gt_likelihood)\n                c(error_likelihood - gt_likelihood, ab)\n            }\n            ')

    def __call__(self, record):
        if record.is_monomorphic:
            return
        passed, tv, ab = self.bias_test(record.samples)
        if tv > self.threshold:
            return tv

    def bias_test(self, calls):
        calls = [x for x in calls if x.called]
        try:
            ra = robjects.IntVector([x['RO'][0] for x in calls])
            aa = robjects.IntVector([x['AO'][0] for x in calls])
        except AttributeError:
            ra = robjects.IntVector([x['AD'][0] for x in calls])
            aa = robjects.IntVector([x['AD'][1] for x in calls])

        gt = robjects.IntVector([x.gt_type for x in calls])
        test_val, ab = self.ll_test(ra, aa, gt)
        return (
         test_val < 0, test_val, ab)


class DepthPerSample(Base):
    __doc__ = 'Threshold read depth per sample'
    name = 'dps'

    @classmethod
    def customize_parser(self, parser):
        parser.add_argument('--depth-per-sample', type=int, default=5, help='Minimum required coverage in each sample')

    def __init__(self, args):
        self.threshold = args.depth_per_sample

    def __call__(self, record):
        if record.is_indel:
            return
        mindepth = min([sam['DP'] for sam in record.samples])
        if mindepth < self.threshold:
            return mindepth


class AvgDepthPerSample(Base):
    __doc__ = 'Threshold average read depth per sample (read_depth / sample_count)'
    name = 'avg-dps'

    @classmethod
    def customize_parser(self, parser):
        parser.add_argument('--avg-depth-per-sample', type=int, default=3, help='Minimum required average coverage per sample')

    def __init__(self, args):
        self.threshold = args.avg_depth_per_sample

    def __call__(self, record):
        avgcov = float(record.INFO['DP']) / len(record.samples)
        if avgcov < self.threshold:
            return avgcov


class SnpOnly(Base):
    __doc__ = 'Choose only SNP variants'
    name = 'snp-only'

    def __call__(self, record):
        if not record.is_snp:
            return True

    def filter_name(self):
        return self.name