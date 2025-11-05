import pytest
import numpy as np
from interest_rates.interest_rates import (
    equivalent_rates
)


@pytest.mark.parametrize(
    'term_to_convert, day_basis_to_convert, rate_to_convert, required_term, required_day_basis, expected_result',
    [
        (360, 360, 0.21, 360, 90, 5.25),
        (360, 360, 0.36, 360, 30, 3.00),
        (30, 30, 0.027, 30, 1, 0.09),
        (1, 1, 0.00053, 1, 360, 19.08),
    ]
)
def test_calculate_equivalent_rates1(
        term_to_convert,
        day_basis_to_convert,
        rate_to_convert,
        required_term,
        required_day_basis,
        expected_result):
    er = equivalent_rates(term_to_convert, day_basis_to_convert, rate_to_convert, required_term, required_day_basis)
    rr = er.calculate_equivalent_rates(capitalization_regime='lin')
    rr = round(rr, 4) * 100
    assert rr == expected_result


@pytest.mark.parametrize(
    'term_to_convert, day_basis_to_convert, rate_to_convert, required_term, required_day_basis, expected_result',
    [
        (360, 360, 0.30, 360, 90, 6.78),
        (360, 30, 0.03, 360, 360, 42.58),
        (30, 30, 0.04, 30, 1, 0.13),
        (21, 21, 0.053, 30, 1, 0.13),
        (30, 30, 0.04, 30, 1, 0.13)
    ]
)
def test_calculate_equivalent_rates2(
        term_to_convert,
        day_basis_to_convert,
        rate_to_convert,
        required_term,
        required_day_basis,
        expected_result):
    er = equivalent_rates(term_to_convert, day_basis_to_convert, rate_to_convert, required_term, required_day_basis)
    rr = er.calculate_equivalent_rates(capitalization_regime='exp')
    rr = round(rr, 4) * 100
    assert rr == expected_result
