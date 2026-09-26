import pytest
import pandas as pd

@pytest.fixture(scope='session')
def cap_regime_data():
    '''Fixture to generate data to our tests'''
    return pd.DataFrame({
        "target_value": [10000, 20000, 30000],
        "fee": [0.10, 0.08, 0.05],
        "term": [30, 60, 90]
    })
