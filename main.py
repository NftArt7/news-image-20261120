"""news-image-20261120 entry program.

The entry image is pre-rendered (see gen_image.py) and shipped in this
repository as entry.png. This program only copies it into the grader's
output directory, so both runs produce exactly the same bytes.

Python 3.13, standard library only, no network.
"""

import os
import shutil
import sys

SOURCE_NAME = "entry.png"
DEST_NAME = "entry.png"


def locate_source():
    """entry.png sits next to this program in the repository."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, SOURCE_NAME)


def output_dir():
    """The grader sets MAKEFUN_OUTPUT_DIR; /output is the default."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def run():
    src = locate_source()
    if not os.path.isfile(src):
        print(f"missing {SOURCE_NAME} next to main.py", file=sys.stderr)
        return 1
    dst_dir = output_dir()
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, DEST_NAME)
    shutil.copyfile(src, dst)
    # Confirm the copy is complete: same byte count as the source.
    if os.path.getsize(dst) != os.path.getsize(src):
        print("copy size mismatch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
