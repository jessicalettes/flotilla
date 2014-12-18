"""
This file will be auto-imported for every testing session, so you can use
these objects and functions across test files.
"""
import subprocess

import numpy as np
import pytest
import pandas as pd
from scipy import stats


# CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
# SHALEK2013_BASE_URL = 'http://raw.githubusercontent.com/YeoLab/shalek2013/master'
# # SHALEK2013_BASE_URL = 'http://sauron.ucsd.edu/flotilla_projects/shalek2013'
# CHR22_BASE_URL = 'http://sauron.ucsd.edu/flotilla_projects/neural_diff_chr22'

@pytest.fixture(scope='module')
def RANDOM_STATE():
    return 0

@pytest.fixture(scope='module', params=[True, False])
def BOOLEAN(request):
    return request.param

@pytest.fixture(scope='module')
def n_samples():
    return 50

@pytest.fixture(scope='module')
def samples(n_samples):
    return ['sample_{}'.format(i+1) for i in np.arange(n_samples)]

@pytest.fixture(scope='module', params=[2, 3])
def n_groups(request):
    return request.param

@pytest.fixture(scope='module')
def groups(n_groups):
    return ['group{}'.format(i+1) for i in np.arange(n_groups)]

@pytest.fixture(scope='module')
def n_genes():
    return 50

@pytest.fixture(scope='module')
def genes(n_genes):
    return ['gene_{}'.format(i+1) for i in np.arange(n_genes)]

@pytest.fixture(scope='module')
def n_events():
    return 1000

@pytest.fixture(scope='module')
def events(n_events):
    return ['event_{}'.format(i+1) for i in np.arange(n_events)]

@pytest.fixture(scope='module')
def groupby(groups, samples):
    return dict((sample, np.random.choice(groups)) for sample in samples)

@pytest.fixture(scope='module')
def modality_models():
    rv_included = stats.beta(2, 1)
    rv_excluded = stats.beta(1, 2)
    rv_middle = stats.beta(2, 2)
    rv_uniform = stats.uniform(0, 1)
    rv_bimodal = stats.beta(.5, .5)

    models = {'included': rv_included,
              'excluded': rv_excluded,
              'middle': rv_middle,
              'uniform': rv_uniform,
              'bimodal': rv_bimodal}
    return models

@pytest.fixture(scope='module', params=[0, 0.5, 0.75, 1])
def na_thresh(request):
    return request.param

@pytest.fixture(scope='module')
def true_modalities(events, modality_models, groups, na_thresh):
    data = dict((e, dict((g, (np.random.choice(modality_models.keys())))
                         for g in groups)) for e in events)
    df = pd.DataFrame(data)
    if na_thresh > 0:
        df = df.apply(
            lambda x: x.map(lambda i: i if np.random.uniform() >
                                           np.random.uniform(0, na_thresh/10)
            else np.nan), axis=1)
    return df

@pytest.fixture(scope='module')
def splicing_data(samples, events, true_modalities, modality_models,
                  na_thresh, groupby):
    data = np.vstack(
        [modality_models[m].rvs(n_samples) for m in true_modalities]).T
    df = pd.DataFrame(data, index=samples, columns=events)
    if na_thresh > 0:
        df = df.apply(lambda x: x.map(
            lambda i: i if np.random.uniform() >
                           np.random.uniform(0, na_thresh)
            else np.nan), axis=1)
        df = pd.concat([d.apply(
            lambda x: x if np.random.uniform() >
                           np.random.uniform(0, na_thresh)
            else pd.Series(np.nan, index=x.index), axis=1) for group, d in
                   df.groupby(groupby)], axis=1)
    return df

@pytest.fixture(scope='module')
def splicing_feature_data(events, genes):
    df = pd.DataFrame(index=events)
    df['gene_name'] = df.index.map(lambda x: np.random.choice(genes))
    return df

@pytest.fixture(scope='module',
                params=['shalek2013', 'scrambled_study'])
def study(request, shalek2013, scrambled_study):
    if request.param == 'shalek2013':
        return shalek2013
    if request.param == 'scrambled_study':
        return scrambled_study


@pytest.fixture(scope='module')
def genelist_path(data_dir):
    return '{}/example_gene_list.txt'.format(data_dir)


@pytest.fixture(scope='module')
def genelist_dropbox_link():
    return 'https://www.dropbox.com/s/652y6hb8zonxe4c/example_gene_list.txt' \
           '?dl=0'


@pytest.fixture(params=['local', 'dropbox'])
def genelist_link(request, genelist_path, genelist_dropbox_link):
    if request.param == 'local':
        return genelist_path
    elif request.param == 'dropbox':
        return genelist_dropbox_link


@pytest.fixture(params=[None, 'gene_category: LPS Response',
                        'link',
                        'path'], scope='module')
def feature_subset(request, genelist_dropbox_link, genelist_path):
    from flotilla.util import link_to_list

    name_to_location = {'link': genelist_dropbox_link,
                        'path': genelist_path}

    if request.param is None:
        return request.param
    elif request.param in ('link', 'path'):

        try:
            return link_to_list(name_to_location[request.param])
        except subprocess.CalledProcessError:
            # Downloading the dropbox link failed, aka not connected to the
            # internet, so just test "None" again
            return None
    else:
        # Otherwise, this is a name of a subset
        return request.param

@pytest.fixture(scope='module')
def x_norm():
    """Normally distributed numpy array"""
    n_samples = 50
    n_features = 1000
    x = np.random.randn(n_samples * n_features)
    x = x.reshape(n_samples, n_features)
    return x


@pytest.fixture(scope='module')
def df_norm(x_norm):
    """Normally distributed pandas dataframe"""
    nrow, ncol = x_norm.shape
    index = ['sample_{0:02d}'.format(i) for i in range(nrow)]
    columns = ['feature_{0:04d}'.format(i) for i in range(ncol)]
    df = pd.DataFrame(x_norm, index=index, columns=columns)
    return df

@pytest.fixture(scope='module')
def df_nonneg(df_norm):
    """Non-negative data for testing NMF"""
    return df_norm.abs()

@pytest.fixture(scope='module', params=[0, 5])
def minimum_samples(request):
    return request.param

@pytest.fixture(params=[True, False])
def featurewise(request):
    return request.param

@pytest.fixture(scope='module')
def base_data(shalek2013_data):
    from flotilla.data_model.base import BaseData
    return BaseData(shalek2013_data.expression)

@pytest.fixture(params=[None, 'half', 'all'], scope='module')
def sample_ids(request, base_data):
    if request.param is None:
        return request.param
    elif request.param == 'some':
        half = base_data.data.shape[0] / 2
        return base_data.data.index[:half]
    elif request.param == 'all':
        return base_data.data.index


@pytest.fixture(params=[None, 'half', 'all'], scope='module')
def feature_ids(request, base_data):
    if request.param is None:
        return request.param
    elif request.param == 'some':
        half = base_data.data.shape[1] / 2
        return base_data.data.columns[:half]
    elif request.param == 'all':
        return base_data.data.columns

@pytest.fixture(params=[True, False], scope='module')
def standardize(request):
    return request.param

@pytest.fixture(params=['phenotype: Immature BDMC',
                        'not (phenotype: Immature BDMC)',
                        'pooled'],
                scope='module')
def sample_subset(request):
    return request.param