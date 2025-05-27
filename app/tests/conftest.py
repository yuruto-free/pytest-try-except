import pytest

@pytest.fixture
def get_compare_float_value():
  inner = lambda val, threshold=1e-10: abs(val) < threshold

  return inner