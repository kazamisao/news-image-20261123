# news-image-20261123 entry (Python 3.13, standard library only).
# The image is drawn at build time and committed as news.png beside this
# file; the program copies it to /output/entry.png. No network, no
# randomness: two runs write byte-identical output.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

_SRC = os.path.join(_HERE, "news.png")
_DST = os.path.join(_OUT, "entry.png")

os.makedirs(_OUT, exist_ok=True)
shutil.copyfile(_SRC, _DST)
assert os.path.getsize(_DST) == os.path.getsize(_SRC), "short copy"
