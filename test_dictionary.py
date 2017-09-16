import pytest
from main import *


def test_mapping_inversion():
    inverse_mapping = inverse_initial_mapping(MAPPING)

    assert inverse_mapping['e'] == '0'
    assert inverse_mapping['A'] == '5'
    assert inverse_mapping['i'] == '6'
