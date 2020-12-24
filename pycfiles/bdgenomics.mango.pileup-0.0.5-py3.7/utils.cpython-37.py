# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/io/utils.py
# Compiled at: 2019-09-04 14:12:25
# Size of source mod 2**32: 1890 bytes


def parse_bed_dataframe(dataframe):
    """ Transforms a dataframe with bed information to a GA4GHFeature JSON String

    Args:
        :param dataframe: dataframe containing bed data

    """
    df_cols = list(dataframe.columns)
    valid_columns = True
    for name in ('chrom', 'chromStart', 'chromEnd'):
        if name not in df_cols:
            valid_columns = False

    if not valid_columns:
        chrom, chrom_start, chom_end = df_cols[:3]
        chrom_starts = [
         int(chrom_start)] + list(dataframe[chrom_start])
        chrom_ends = [int(chom_end)] + list(dataframe[chom_end])
        chromosomes = [chrom] + list(dataframe[chrom])
        return build_json_from_bed(chrom_starts, chrom_ends, chromosomes)
    chromosomes = list(dataframe['chrom'])
    chrom_starts = list(dataframe['chromStart'])
    chrom_ends = list(dataframe['chromEnd'])
    return build_json_from_bed(chrom_starts, chrom_ends, chromosomes)


def build_json_from_bed(chrom_starts, chrom_ends, chromosomes):
    """ Converts a parsed bed file into a json string in GA4GH schema.

    Args:
        :param list: start range values
        :param list: end range values
        :param list: chromosome range values

    """
    json_ga4gh = '{"features":['
    for i in range(len(chromosomes) + 1):
        if i < len(chromosomes):
            bed_content = '"referenceName":{}, "start":{}, "end":{}'.format('"' + chromosomes[i] + '"', '"' + str(chrom_starts[i]) + '"', '"' + str(chrom_ends[i]) + '"')
            json_ga4gh = json_ga4gh + '{' + bed_content + '},'
        else:
            json_ga4gh = json_ga4gh[:len(json_ga4gh) - 1]

    json_ga4gh = json_ga4gh + ']}'
    return json_ga4gh