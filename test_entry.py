"""Local tests for the news-image-20261123 entry.

Run: python3 test_entry.py
All tests use the standard library only (plus Pillow, which is only the
test harness's reader - the entry program itself is stdlib-only).
"""
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
NEWS = os.path.join(HERE, "news.png")
MAIN = os.path.join(HERE, "main.py")
MAX_BYTES = 1048576


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_main(out_dir):
    env = dict(os.environ)
    env["MAKEFUN_OUTPUT_DIR"] = out_dir
    return subprocess.run(
        [sys.executable, MAIN], env=env, capture_output=True, text=True,
        timeout=60, cwd=HERE,
    )


class TestEntry(unittest.TestCase):
    def test_news_png_exists_and_under_1mib(self):
        self.assertTrue(os.path.isfile(NEWS), "news.png is missing")
        size = os.path.getsize(NEWS)
        self.assertLessEqual(size, MAX_BYTES,
                             f"news.png is {size} bytes, over the 1 MiB cap")

    def test_news_png_is_1024x1024(self):
        from PIL import Image
        with Image.open(NEWS) as im:
            self.assertEqual(im.size, (1024, 1024),
                             f"news.png is {im.size}, expected 1024x1024")

    def test_news_png_is_valid_png(self):
        with open(NEWS, "rb") as f:
            magic = f.read(8)
        self.assertEqual(magic, b"\x89PNG\r\n\x1a\n",
                         "news.png does not start with the PNG magic bytes")
        from PIL import Image
        with Image.open(NEWS) as im:
            im.verify()
        with Image.open(NEWS) as im:
            im.load()  # full decode: catches truncated/corrupt data

    def test_main_writes_entry_png_to_output_dir(self):
        with tempfile.TemporaryDirectory() as d:
            res = run_main(d)
            self.assertEqual(res.returncode, 0,
                             f"main.py exited {res.returncode}: {res.stderr}")
            out = os.path.join(d, "entry.png")
            self.assertTrue(os.path.isfile(out),
                            "main.py did not write $MAKEFUN_OUTPUT_DIR/entry.png")
            with open(NEWS, "rb") as f, open(out, "rb") as g:
                self.assertEqual(g.read(), f.read(),
                                 "entry.png bytes differ from news.png")

    def test_main_is_deterministic_across_two_runs(self):
        with tempfile.TemporaryDirectory() as d1, \
                tempfile.TemporaryDirectory() as d2:
            r1 = run_main(d1)
            r2 = run_main(d2)
            self.assertEqual(r1.returncode, 0, r1.stderr)
            self.assertEqual(r2.returncode, 0, r2.stderr)
            h1 = sha256_of(os.path.join(d1, "entry.png"))
            h2 = sha256_of(os.path.join(d2, "entry.png"))
            self.assertEqual(h1, h2,
                             f"two runs differ: {h1} vs {h2}")

    def test_main_uses_no_network(self):
        with open(MAIN, "r", encoding="utf-8") as f:
            src = f.read()
        for banned in ("socket", "urllib", "requests", "http.client",
                       "urlopen", "httpx", "aiohttp"):
            self.assertNotIn(banned, src,
                             f"main.py mentions {banned!r}: no network allowed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
