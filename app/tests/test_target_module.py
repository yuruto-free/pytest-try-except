import pytest

@pytest.fixture
def get_resetter_of_sys_modules(mocker):
  def module_setter(remove_cached_modules=None, mocker_modules=None):
    # Initialization
    remove_cached_modules = remove_cached_modules or []
    mocker_modules = mocker_modules or []
    # Reset cached module data
    import sys
    _fake_modules = {key: val for key, val in sys.modules.items() if key not in remove_cached_modules}
    # Set specific module which is replaced to mock instance
    for key in mocker_modules:
      _fake_modules[key] = mocker.Mock()
    # Enable patch
    mocker.patch.dict('sys.modules', _fake_modules, clear=True)

  return module_setter

@pytest.mark.abnormal
def test_cannot_load_specific_files(get_resetter_of_sys_modules):
  module_setter = get_resetter_of_sys_modules
  # Remove old modules
  module_setter(remove_cached_modules=[
    'src.target_module',
    'src.sample_with_having_errors',
    'disabled_module',
    'cannot_use_package.cannot_use_module',
  ])

  # ==================
  # Import test module
  # ==================
  # [Attention] Cannot use `from src import target_module as tm` becuase the imported module is separated from original one
  import src.target_module as tm

  assert not tm.g_sample

@pytest.mark.normal
def test_avoid_raising_import_exception(get_resetter_of_sys_modules):
  module_setter = get_resetter_of_sys_modules
  # Remove old modules and replace original module to mock module
  module_setter(
    remove_cached_modules=['src.target_module', 'src.sample_with_having_errors'],
    mocker_modules=['disabled_module', 'cannot_use_package.cannot_use_module'],
  )

  # ==================
  # Import test module
  # ==================
  # [Attention] Cannot use `from src import target_module as tm` becuase the imported module is separated from original one
  import src.target_module as tm

  assert tm.g_sample

@pytest.mark.normal
def test_can_load_private_file(get_resetter_of_sys_modules):
  module_setter = get_resetter_of_sys_modules
  # Remove old modules
  module_setter(remove_cached_modules=[
    'src.target_module',
    'src.private',
  ])

  # ==================
  # Import test module
  # ==================
  import src.target_module as tm

  assert tm.g_private

@pytest.mark.abnormal
def test_raise_import_exception_with_existing_file(get_resetter_of_sys_modules, mocker):
  module_setter = get_resetter_of_sys_modules
  # Remove old modules
  module_setter(remove_cached_modules=[
    'src.target_module',
    'src.private',
  ])
  # Define fake finder
  import importlib
  original_finder = importlib._bootstrap._find_and_load

  def _fake_finder(name, *args, **kwargs):
    # Raise Exception when specific filepath is given
    if name == 'src.private':
      raise Exception()
  
    return original_finder(name, *args, **kwargs)
  # Mock find_spec method
  mocker.patch('importlib._bootstrap._find_and_load', side_effect=_fake_finder)

  # ==================
  # Import test module
  # ==================
  import src.target_module as tm

  assert not tm.g_private

@pytest.mark.normal
def test_execute_func(get_resetter_of_sys_modules, mocker):
  module_setter = get_resetter_of_sys_modules
  # Remove old modules and replace original module to mock module
  module_setter(
    remove_cached_modules=['src.target_module', 'src.sample_with_having_errors'],
    mocker_modules=['disabled_module', 'cannot_use_package.cannot_use_module'],
  )
  # Define return-value
  ret_y1 = 4
  ret_y2 = 5
  y_sum  = ret_y1 + ret_y2
  # Setup mock
  import sys
  disabled_module_mocker = sys.modules['disabled_module']
  mocker.patch.object(disabled_module_mocker, 'undefined_function', return_value=ret_y1)
  mocker.patch('src.sample_with_having_errors.disabled_function', return_value=ret_y2)

  import src.sample_with_having_errors as swhe
  estimate_y = swhe.execute(1)

  assert estimate_y == y_sum