"""Quick compile check helper used by CI or local checks."""

import py_compile, traceback, sys

try:
    py_compile.compile(r'c:\\code\\glen\\tabs\\grid_tab.py', doraise=True)
    print('COMPILE_OK')
except Exception:
    traceback.print_exc()
    sys.exit(1)
