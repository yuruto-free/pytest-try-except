import pytest
from src import newton

@pytest.mark.normal
@pytest.mark.parametrize([
  'idx',
  'value',
], [
  (-1, -1.0),
  ( 0,  1.0),
  ( 1,  0.0),
  ( 2,  123),
], ids=[
  'both-are-negative',
  'idx-is-zero',
  'value-is-almost-zero',
  'value-is-integer',
])
def test_check_method_of_store(get_compare_float_value, idx, value):
  compare = get_compare_float_value
  store = newton._Store(iter=idx, value=value)
  out_iter, out_value = store.get_pair()

  assert out_iter == idx
  assert compare(out_value - value)

@pytest.mark.normal
def test_check_members_of_newton1d(get_compare_float_value):
  compare = get_compare_float_value
  func = lambda x: x
  instance = newton.Newton1d(func)

  assert isinstance(instance._store_class(), newton._Store)
  assert callable(instance._objective_function)
  assert isinstance(instance._eps, float)
  assert compare(instance._eps - 1e-5)
  assert isinstance(instance._history, list)
  assert len(instance._history) == 0

@pytest.mark.normal
@pytest.mark.parametrize([
  'func',
  'is_callable',
], [
  (lambda x: 3, True),
  (3, False),
  (None, False),
], ids=[
  'set-function',
  'set-non-function',
  'set-none',
])
def test_constructor_of_newton1d(func, is_callable):
  instance = newton.Newton1d(func)

  assert callable(instance._objective_function) == is_callable

@pytest.mark.normal
@pytest.mark.parametrize([
  'x',
  'const',
], [
  (3, 1),
  (-1, 1),
], ids=[
  'is-positive-value',
  'is-negative-value',
])
def test_check_diff_func(get_compare_float_value, x, const):
  compare = get_compare_float_value
  func = lambda val, c=0: val + c
  instance = newton.Newton1d(func)
  exact_diff = 0.5 * (func(x+1e-5, c=const) - func(x-1e-5, c=const)) / 1e-5
  estimated_diff = instance._center_numerical_diff(x, c=const)

  assert compare(exact_diff - estimated_diff)

@pytest.mark.normal
def test_check_history():
  instance = newton.Newton1d(None)
  _ = instance.estimate(1, max_iter=0)
  hist = instance.histories

  assert len(hist) == 1
  assert isinstance(hist[0], newton._Store)

@pytest.mark.normal
def test_newton_method(get_compare_float_value):
  compare = get_compare_float_value
  func = lambda x: x ** 2 - 2.0 * 2.0
  instance = newton.Newton1d(func)
  #     x_new <-  x - 0.5 * (x^2 - 4) / x
  # <=> x_new <-  (0.5 * x^2 + 2) / x
  x0 = 1.0
  threshold = 1e-6
  # idx | x_old       | x_new       | diff
  # ----+-------------+-------------+------------------------
  #   0 | 1.0         |             |
  #   1 | 1.0         | 2.500000000 | 1.50000000 -> 1.50e-0
  #   2 | 2.5         | 2.050000000 | 0.45000000 -> 4.50e-1
  #   3 | 2.05        | 2.000609761 | 0.00493902 -> 4.49e-2
  #   4 | 2.000609761 | 2.000000093 | 0.00006097 -> 6.10e-4
  #   5 | 2.000000093 | 2.000000000 |            -> 9.29e-8
  hat_x = instance.estimate(x0, threshold=threshold)
  hist = instance.histories

  assert compare(hat_x - 2.0, threshold=threshold)
  assert len(hist) == 6