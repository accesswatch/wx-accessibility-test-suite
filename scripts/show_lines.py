"""Helper to show source lines for debugging large files (used locally)."""

from pathlib import Path

p = Path(r'c:\code\glen\tabs\grid_tab.py')
s = p.read_text().splitlines()
for i in range(225, 245):
    if i < len(s):
        print(f"{i+1:4}: {repr(s[i])}")
