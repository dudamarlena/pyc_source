# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/cli/summarypages.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 9387 bytes
from pesummary.utils.utils import logger, gw_results_file
from pesummary.core.inputs import PostProcessing
from pesummary.gw.inputs import GWPostProcessing

class WebpageGeneration(object):
    __doc__ = 'Wrapper class for _GWWebpageGeneration and _CoreWebpageGeneration\n\n    Parameters\n    ----------\n    inputs: argparse.Namespace\n        Namespace object containing the command line options\n    colors: list, optional\n        colors that you wish to use to distinguish different result files\n    '

    def __init__(self, inputs, colors='default', gw=False):
        self.inputs = inputs
        self.colors = colors
        self.gw = gw
        self.generate_webpages()

    def generate_webpages(self):
        """Generate all plots for all result files passed
        """
        logger.info('Starting to generate webpages')
        if self.gw:
            if self.inputs.public:
                object = _PublicGWWebpageGeneration((self.inputs), colors=(self.colors))
        else:
            if self.gw:
                object = _GWWebpageGeneration((self.inputs), colors=(self.colors))
            else:
                object = _CoreWebpageGeneration((self.inputs), colors=(self.colors))
        object.generate_webpages()
        logger.info('Finished generating webpages')


class _CoreWebpageGeneration(PostProcessing):
    __doc__ = 'Class to generate all webpages for all result files with the Core module\n\n    Parameters\n    ----------\n    inputs: argparse.Namespace\n        Namespace object containing the command line options\n    colors: list, optional\n        colors that you wish to use to distinguish different result files\n    '

    def __init__(self, inputs, colors='default'):
        from pesummary.core.webpage.main import _WebpageGeneration
        super(_CoreWebpageGeneration, self).__init__(inputs, colors)
        self.webpage_object = _WebpageGeneration(webdir=(self.webdir),
          samples=(self.samples),
          labels=(self.labels),
          publication=(self.publication),
          user=(self.user),
          config=(self.config),
          same_parameters=(self.same_parameters),
          base_url=(self.baseurl),
          file_versions=(self.file_version),
          hdf5=(self.hdf5),
          colors=(self.colors),
          custom_plotting=(self.custom_plotting),
          existing_labels=(self.existing_labels),
          existing_config=(self.existing_config),
          existing_file_version=(self.existing_file_version),
          existing_injection_data=(self.existing_injection_data),
          existing_samples=(self.existing_samples),
          existing_metafile=(self.existing),
          existing_file_kwargs=(self.existing_file_kwargs),
          existing_weights=(self.existing_weights),
          add_to_existing=(self.add_to_existing),
          notes=(self.notes),
          disable_comparison=(self.disable_comparison),
          disable_interactive=(self.disable_interactive),
          package_information=(self.package_information))

    def generate_webpages(self):
        """Generate all webpages within the Core module
        """
        self.webpage_object.generate_webpages()


class _GWWebpageGeneration(GWPostProcessing):
    __doc__ = 'Class to generate all webpages for all result files with the GW module\n\n    Parameters\n    ----------\n    inputs: argparse.Namespace\n        Namespace object containing the command line options\n    colors: list, optional\n        colors that you wish to use to distinguish different result files\n    '

    def __init__(self, inputs, colors='default'):
        from pesummary.gw.webpage.main import _WebpageGeneration
        super(_GWWebpageGeneration, self).__init__(inputs, colors)
        key_data = self.grab_key_data_from_result_files()
        self.webpage_object = _WebpageGeneration(webdir=(self.webdir),
          samples=(self.samples),
          labels=(self.labels),
          publication=(self.publication),
          user=(self.user),
          config=(self.config),
          same_parameters=(self.same_parameters),
          base_url=(self.baseurl),
          file_versions=(self.file_version),
          hdf5=(self.hdf5),
          colors=(self.colors),
          custom_plotting=(self.custom_plotting),
          gracedb=(self.gracedb),
          pepredicates_probs=(self.pepredicates_probs),
          approximant=(self.approximant),
          key_data=key_data,
          file_kwargs=(self.file_kwargs),
          existing_labels=(self.existing_labels),
          existing_config=(self.existing_config),
          existing_file_version=(self.existing_file_version),
          existing_injection_data=(self.existing_injection_data),
          existing_samples=(self.existing_samples),
          existing_metafile=(self.existing),
          add_to_existing=(self.add_to_existing),
          existing_file_kwargs=(self.existing_file_kwargs),
          existing_weights=(self.existing_weights),
          result_files=(self.result_files),
          notes=(self.notes),
          disable_comparison=(self.disable_comparison),
          disable_interactive=(self.disable_interactive),
          pastro_probs=(self.pastro_probs),
          gwdata=(self.gwdata),
          publication_kwargs=(self.publication_kwargs),
          no_ligo_skymap=(self.no_ligo_skymap),
          psd=(self.psd),
          priors=(self.priors),
          package_information=(self.package_information))

    def generate_webpages(self):
        """Generate all webpages within the Core module
        """
        self.webpage_object.generate_webpages()


class _PublicGWWebpageGeneration(GWPostProcessing):
    __doc__ = 'Class to generate all webpages for all result files with the GW module\n\n    Parameters\n    ----------\n    inputs: argparse.Namespace\n        Namespace object containing the command line options\n    colors: list, optional\n        colors that you wish to use to distinguish different result files\n    '

    def __init__(self, inputs, colors='default'):
        from pesummary.gw.webpage.public import _PublicWebpageGeneration
        super(_PublicGWWebpageGeneration, self).__init__(inputs, colors)
        key_data = self.grab_key_data_from_result_files()
        self.webpage_object = _PublicWebpageGeneration(webdir=(self.webdir),
          samples=(self.samples),
          labels=(self.labels),
          publication=(self.publication),
          user=(self.user),
          config=(self.config),
          same_parameters=(self.same_parameters),
          base_url=(self.baseurl),
          file_versions=(self.file_version),
          hdf5=(self.hdf5),
          colors=(self.colors),
          custom_plotting=(self.custom_plotting),
          gracedb=(self.gracedb),
          pepredicates_probs=(self.pepredicates_probs),
          approximant=(self.approximant),
          key_data=key_data,
          file_kwargs=(self.file_kwargs),
          existing_labels=(self.existing_labels),
          existing_config=(self.existing_config),
          existing_file_version=(self.existing_file_version),
          existing_injection_data=(self.existing_injection_data),
          existing_samples=(self.existing_samples),
          existing_metafile=(self.existing),
          add_to_existing=(self.add_to_existing),
          existing_file_kwargs=(self.existing_file_kwargs),
          existing_weights=(self.existing_weights),
          result_files=(self.result_files),
          notes=(self.notes),
          disable_comparison=(self.disable_comparison),
          disable_interactive=(self.disable_interactive),
          pastro_probs=(self.pastro_probs),
          gwdata=(self.gwdata),
          publication_kwargs=(self.publication_kwargs),
          no_ligo_skymap=(self.no_ligo_skymap),
          psd=(self.psd),
          priors=(self.priors),
          package_information=(self.package_information))

    def generate_webpages(self):
        """Generate all webpages within the Core module
        """
        self.webpage_object.generate_webpages()


def main(args=None):
    """Top level interface for `summarypages`
    """
    from pesummary.core.command_line import command_line
    from pesummary.gw.command_line import insert_gwspecific_option_group, add_dynamic_PSD_to_namespace, add_dynamic_calibration_to_namespace
    from pesummary.utils import functions
    parser = command_line()
    insert_gwspecific_option_group(parser)
    opts, unknown = parser.parse_known_args(args=args)
    add_dynamic_PSD_to_namespace(opts)
    add_dynamic_calibration_to_namespace(opts)
    func = functions(opts)
    args = func['input'](opts)
    from .summaryplots import PlotGeneration
    plotting_object = PlotGeneration(args, gw=(gw_results_file(opts)))
    WebpageGeneration(args, gw=(gw_results_file(opts)))
    func['MetaFile'](args)
    if gw_results_file(opts):
        kwargs = dict(ligo_skymap_PID=(plotting_object.ligo_skymap_PID))
    else:
        kwargs = {}
    (func['FinishingTouches'])(args, **kwargs)


if __name__ == '__main__':
    main()