from dataclasses import dataclass

@dataclass
class _Store:
  iter: int = 0
  value: float = 0

  def get_pair(self):
    return self.iter, self.value

class Newton1d:
  def __init__(self, objective_function):
    self._store_class = _Store
    self._objective_function = objective_function
    self._eps = 1e-5
    self._history = []

  # Calculate numerical differentiation
  def _center_numerical_diff(self, x, **kwargs):
    left_val = self._objective_function(x - self._eps, **kwargs)
    right_val = self._objective_function(x + self._eps, **kwargs)
    df = 0.5 * (right_val - left_val) / self._eps

    return df

  @property
  def histories(self):
    return self._history

  def estimate(self, x0, max_iter=1024, threshold=1e-10, **kwargs):
    x_new = x_old = x0
    self._history = [self._store_class(iter=0, value=x0)]

    for idx in range(max_iter):
      fval = self._objective_function(x_old, **kwargs)
      df = self._center_numerical_diff(x_old, **kwargs)
      x_new = x_old - fval / df
      self._history += [self._store_class(iter=idx+1, value=x_new)]

      if abs(x_new - x_old) < threshold:
        break
      x_old = x_new

    return x_new