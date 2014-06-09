__author__ = 'lovci'

import params
from .src.loaders import load_descriptors, load_transcriptome_data
from flotilla import schooner


def embark(load_cargo=True, drop_outliers=False,):

    """return a flotilla study"""
    interactive_args = {'load_cargo': load_cargo, 'drop_outliers': drop_outliers}
    metadata_dict = {
        'sample_descriptors_data_dump': params.sample_descriptors_data_dump,
        'gene_descriptors_data_dump': params.gene_descriptors_data_dump,
        'event_descriptors_data_dump': params.event_descriptors_data_dump,
    }
    data_dict = {
        'splicing_data_dump': params.splicing_data_dump,
        'expression_data_dump': params.expression_data_dump
    }
    return schooner.FlotillaStudy(metadata_dict = metadata_dict, metadata_loader = load_descriptors,
                                  data_dict = data_dict, data_loader = load_transcriptome_data,
                                  params_dict=vars(params), **interactive_args)