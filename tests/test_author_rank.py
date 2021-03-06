# imports
from author_rank.graph import create, export_to_json
from author_rank.score import top_authors
import json
import pytest


@pytest.fixture()
def sample_data() -> dict:
    """
    This fixture reads in sample data from the data directory for the purposes of testing the functionality.
    :return: None
    """

    # read in sample json
    with open("data/author_network.json", 'r') as f:
        data = json.load(f)

    return data


def test_export_format(sample_data) -> None:
    """
    Test to ensure that the graph is being effectively exported as a dictionary which is valid JSON.
    :param sample_data: the sample data
    :return: None
    """

    # generate a graph
    G = create(documents=sample_data['documents'])

    # export them
    export = export_to_json(graph=G)

    assert type(export) == dict


def test_top_author_format(sample_data) -> None:
    """
    Test to ensure that the top_author is returning a tuple of two lists with the appropriate formatting for the
    output
    :param sample_data: the sample data
    :return: None
    """

    # get the top authors for a set of documents
    top = top_authors(documents=sample_data['documents'])

    # check that it returns a tuple
    assert type(top) == tuple

    # check to ensure each value in the responses are in the appropriate format
    for k, v in zip(top[0], top[1]):
        assert type(k) == tuple
        assert type(v) == float


def test_normalization(sample_data) -> None:
    """
    Test to ensure that normalizing the author_rank scores returns values between
    0 and 1.
    :param sample_data: the sample data
    :return: None
    """

    # get the top authors for a set of documents
    top = top_authors(documents=sample_data['documents'], normalize_scores=True)

    # check that it returns a tuple
    assert type(top) == tuple

    # check to ensure each value in the responses are in the appropriate format
    for v in top[1]:
        assert 0. <= v <= 1.

    # check to ensure that the last entry in the list is a value of 0
    assert top[1][-1] == 0.

    # check to ensure that the first entry in the list is a value of 1
    assert top[1][0] == 1.0
