"""
This file will be auto-imported for every testing session, so you can use
these objects and functions across test files.
"""
import os

import pytest
import pandas as pd


CURRENT_DIR = os.path.dirname(__file__)


class ExampleData(object):
    __slots__ = ('experiment_design_data', 'expression', 'splicing', 'data')

    def __init__(self, experiment_design_data, expression, splicing):
        self.experiment_design_data = experiment_design_data
        self.expression = expression
        self.splicing = splicing
        self.data = (experiment_design_data, expression, splicing)


@pytest.fixture(scope='module')
def example_data():
    data_dir = '{}/data'.format(CURRENT_DIR.rstrip('/'))
    expression = pd.read_table('{}/expression.tsv'.format(data_dir),
                               index_col=0)
    splicing = pd.read_table('{}/splicing.tsv'.format(data_dir), index_col=0)
    metadata = pd.read_table('{}/metadata.tsv'.format(data_dir), index_col=0)
    return ExampleData(metadata, expression, splicing)


@pytest.fixture(scope='module')
def example_study(example_data):
    from flotilla.data_model import Study

    return Study(experiment_design_data=example_data.experiment_design_data,
                 expression_data=example_data.expression,
                 splicing_data=example_data.splicing)


@pytest.fixture(scope='module')
def example_url():
    return 'http://sauron.ucsd' \
           '.edu/flotilla_projects/neural_diff_chr22/datapackage.json'


@pytest.fixture(scope='module')
def expression(example_data):
    from flotilla.data_model import ExpressionData

    return ExpressionData(example_data.expression)