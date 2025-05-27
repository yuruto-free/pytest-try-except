import disabled_module
from cannot_use_package.cannot_use_module import disabled_function

def execute(x):
  y1 = disabled_module.undefined_function(x + 1)
  y2 = disabled_function(x + 2)
  y = y1 + y2

  return y