import pytest
import numpy as np
from financial_math.financial_math import (
    capitalization_regime,
    uniform_payments_series,
    investment_evaluation_methods
)


@pytest.mark.parametrize(
    'term, day_basis, target_value, fee, expected_result',
    [
        (5, 1, 20000, 0.09, 29000.00)  # future and linear
    ]
)
def test_capitalization_regime1(term, day_basis, target_value, fee, expected_result):
    cr = capitalization_regime(term, day_basis)
    vf = cr.discrete_future_value(target_value, fee, capitalization_regime='lin')
    vf = round(vf, 2)
    assert vf == expected_result


@pytest.mark.parametrize(
    'term, day_basis, target_value, fee, expected_result',
    [
        (2, 1/12, 100000, 0.02, 67567.57)  # present and linear
    ]
)
def test_capitalization_regime2(term, day_basis, target_value, fee, expected_result):
    cr = capitalization_regime(term, day_basis)
    vp = cr.discrete_present_value(target_value, fee, capitalization_regime='lin')
    vp = round(vp, 2)
    assert vp == expected_result


@pytest.mark.parametrize(
    'term, day_basis, target_value, fee, expected_result',
    [
        (4, 1, 20000, 0.10, 29282.00),    # future and exponential
        (81, 30, 60000, 0.04, 66702.37)   # future and exponential
    ]
)
def test_capitalization_regime3(term, day_basis, target_value, fee, expected_result):
    cr = capitalization_regime(term, day_basis)
    vf = cr.discrete_future_value(target_value, fee, capitalization_regime='exp')
    vf = round(vf, 2)
    assert vf == expected_result


@pytest.mark.parametrize(
    'term, day_basis, target_value, fee, expected_result',
    [
        (5, 1, 30000, 0.08, 20417.50)  # present and exponential
    ]
)
def test_capitalization_regime4(term, day_basis, target_value, fee, expected_result):
    cr = capitalization_regime(term, day_basis)
    vp = cr.discrete_present_value(target_value, fee, capitalization_regime='exp')
    vp = round(vp, 2)
    assert vp == expected_result


@pytest.mark.parametrize(
    'term, day_basis, future_target_value, present_target_value, expected_result',
    [
        (68, 30, 55700, 40000, 15.73)  # exponential
    ]
)
def test_discrete_effective_transaction_rate1(
        term, day_basis, future_target_value, present_target_value, expected_result):
    cr = capitalization_regime(term, day_basis)
    etr = cr.discrete_effective_transaction_rate(future_target_value, present_target_value, capitalization_regime='exp')
    etr = round(etr, 4) * 100
    assert etr == expected_result


@pytest.mark.parametrize(
    'term, day_basis, future_target_value, present_target_value, expected_result',
    [
        (68, 30, 55700, 40000, 17.32),  # linear
        (5, 1, 29000, 20000, 9.00),
        (720, 30, 100000, 67567.57, 2.00)
    ]
)
def test_discrete_effective_transaction_rate2(
        term, day_basis, future_target_value, present_target_value, expected_result):
    cr = capitalization_regime(term, day_basis)
    etr = cr.discrete_effective_transaction_rate(future_target_value, present_target_value, capitalization_regime='lin')
    etr = round(etr, 4) * 100
    assert etr == expected_result


@pytest.mark.parametrize(
    'term, day_basis, target_value, fee, expected_result',
    [
        (3, 1, 100, 0.016263, 105.00),
        (5, 1, 20000, 0.09, 31366.24)
    ]
)
def test_continuous_future_value(term, day_basis, target_value, fee, expected_result):
    cr = capitalization_regime(term, day_basis)
    vf = cr.continuous_future_value(target_value, fee)
    vf = round(vf, 2)
    assert vf == expected_result


@pytest.mark.parametrize(
    'term, day_basis, target_value, fee, expected_result',
    [
        (3, 1, 105, 0.016263, 100.00),
        (5, 1, 31366.24, 0.09, 20000.00)
    ]
)
def test_continuous_present_value(term, day_basis, target_value, fee, expected_result):
    cr = capitalization_regime(term, day_basis)
    vp = cr.continuous_present_value(target_value, fee)
    vp = round(vp, 2)
    assert vp == expected_result


@pytest.mark.parametrize(
    'term, day_basis, future_target_value, present_target_value, expected_result',
    [
        (3, 1, 105.00, 100.00, 1.63)
    ]
)
def test_continuous_effective_transaction_rate(
        term, day_basis, future_target_value, present_target_value, expected_result):
    cr = capitalization_regime(term, day_basis)
    etr = cr.continuous_effective_transaction_rate(future_target_value, present_target_value)
    etr = round(etr, 4) * 100
    assert etr == expected_result


@pytest.mark.parametrize(
    'term, day_basis, fee, present_target_value, expected_result',
    [
        (360, 30, 0.045, 14000.00, [1535.33, 0.11]),
        (180, 30, 0.08, 1.0, [0.22, 0.22]),
        (12, 1, 0.02, 1000.00, [94.56, 0.09])
    ]
)
def test_deferred_uniform_payments_series(term, day_basis, fee, present_target_value, expected_result):
    ups = uniform_payments_series(term, day_basis)
    pv, fc = ups.deferred_uniform_payments_series(fee, present_target_value)
    pv = round(pv, 2)
    fc = round(fc, 2)
    result = np.array([pv, fc])
    assert np.array_equal(result, expected_result)


@pytest.mark.parametrize(
    'term, day_basis, fee, payments, expected_result',
    [
        (180, 30, 0.05, 3000.00, 15227.08),
        (12, 1, 0.02, 100.00, 1057.53)
    ]
)
def test_present_value_deferred_uniform_series(term, day_basis, fee, payments, expected_result):
    ups = uniform_payments_series(term, day_basis)
    vp = ups.present_value_deferred_uniform_series(fee, payments)
    vp = round(vp, 2)
    assert vp == expected_result


@pytest.mark.parametrize(
    'term, day_basis, fee, present_target_value, expected_result',
    [
        (150, 30, 0.08, 2000.00, [463.81, 0.23]),
        (180, 30, 0.075, 1.0, [0.20, 0.20]),
        (12, 1, 0.02, 1000.00, [92.71, 0.09])
    ]
)
def test_advance_uniform_payments_series(term, day_basis, fee, present_target_value, expected_result):
    ups = uniform_payments_series(term, day_basis)
    pv, fc = ups.advance_uniform_payments_series(fee, present_target_value)
    pv = round(pv, 2)
    fc = round(fc, 2)
    result = np.array([pv, fc])
    assert np.array_equal(result, expected_result)


@pytest.mark.parametrize(
    'term, day_basis, fee, payments, expected_result',
    [
        (120, 30, 0.07, 200.00, 724.86),
        (12, 1, 0.02, 100.00, 1078.68)
    ]
)
def test_present_value_advance_uniform_series(term, day_basis, fee, payments, expected_result):
    ups = uniform_payments_series(term, day_basis)
    vp = ups.present_value_advance_uniform_series(fee, payments)
    vp = round(vp, 2)
    assert vp == expected_result


@pytest.mark.parametrize(
    'term, day_basis, fee, payments, future_target_value, expected_result',
    [
        (5400, 30, 0.01, 500.00, 1.0, 249790.10)
    ]
)
def test_future_value_uniform_payments_series1(term, day_basis, fee, payments, future_target_value, expected_result):
    ups = uniform_payments_series(term, day_basis)
    fv, _ = ups.future_value_uniform_payments_series(fee, payments, future_target_value)
    fv = round(fv, 2)
    assert fv == expected_result


@pytest.mark.parametrize(
    'term, day_basis, fee, payments, future_target_value, expected_result',
    [
        (5400, 30, 0.01, 1.0, 249790.10, 500.00)
    ]
)
def test_future_value_uniform_payments_series2(term, day_basis, fee, payments, future_target_value, expected_result):
    ups = uniform_payments_series(term, day_basis)
    _, pv = ups.future_value_uniform_payments_series(fee, payments, future_target_value)
    pv = round(pv, 2)
    assert pv == expected_result


@pytest.mark.parametrize(
    'flows, rates, expected_result',
    [
        ([-200000.00, 0, 0, 50000.00, 50000.00, 50000.00, 50000.00, 76000.00, 76000.00],
         [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08],
         27386.45),

        ([-25000.00, 9000.00, 8000.00, 8000.00, 7500.00, 7500.00, 7500.00],
         [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
         9816.97),
    ]
)
def test_net_present_value(flows, rates, expected_result):
    iem = investment_evaluation_methods()
    npv = iem.net_present_value(flows, rates)
    npv = round(npv, 2)
    assert npv == expected_result


@pytest.mark.parametrize(
    'flows, expected_result',
    [
        ([-200000.00, 0, 0, 50000.00, 50000.00, 50000.00, 50000.00, 76000.00, 76000.00],
         10.54),

        ([-10000.00, 2500.00, 2500.00, 2500.00, 3000.00, 3000.00],
         10.48)
    ]
)
def test_internal_rate_return(flows, expected_result):
    iem = investment_evaluation_methods()
    irr = iem.internal_rate_return(flows)
    irr = round(irr, 4) * 100
    assert irr == expected_result
