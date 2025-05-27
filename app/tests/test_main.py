import pytest
from src import main

@pytest.mark.normal
@pytest.mark.parametrize([
  'kwargs',
  'exact',
], [
  ({'x': 3, 'target': 0}, 9),
  ({'x': 4}, 4),
], ids=[
  'with-target',
  'without-target',
])
def test_objective_function(get_compare_float_value, kwargs, exact):
  compare = get_compare_float_value
  estimated = main.calc_square(**kwargs)

  assert compare(estimated - exact)