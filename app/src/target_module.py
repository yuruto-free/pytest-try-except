# ==============
# Test pattern 1
# ==============
try:
  import src.sample_with_having_errors
  g_sample = True
except:
  g_sample = False

# ==============
# Test pattern 2
# ==============
try:
  import src.private
  g_private = True
except:
  g_private = False