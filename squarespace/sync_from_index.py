#!/usr/bin/env python3
"""
Regenerate site-v2-tokenized.html from ../index.html so the two sources can
never drift. Edit index.html (the GitHub Pages copy), then run:

    python3 squarespace/sync_from_index.py && python3 squarespace/build.py

The tokenized file differs from index.html in exactly four ways:
  1. the artifact <head> wrapper instead of index's own doctype/head lines
  2. every "media-v2/<path>" becomes a __MEDIA_<path>__ token (build.py fills
     those from asset-map.json)
  3. <!-- EDIT --> markers and the trailing </body></html> form

Run with --check OLD_INDEX TOKENIZED to prove the transform reproduces an
existing pair byte for byte (whitespace-normalised).
"""
import pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent

WRAPPER = ('<!doctype html><html><head><meta charset=utf8><meta name=viewport '
           'content="width=device-width,initial-scale=1"><style>:root{color-scheme:light}'
           'body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;'
           'background:#faf9f5;color:#141413}img{max-width:100%}'
           '[hidden]:not([hidden=until-found]){display:none!important}\n'
           '</style></head><body>\n')

HEAD_RE = re.compile(r'\A<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                     r'<meta name="viewport"[^>]*>\n')


def transform(src: str) -> str:
    out, n = HEAD_RE.subn(WRAPPER, src)
    assert n == 1, "index.html head lines changed; update HEAD_RE"

    for attr in ('rel="canonical" href="https://508mediaco.com/">',
                 'property="og:url" content="https://508mediaco.com/">',
                 'property="og:image" content="https://drewreid508.github.io/508mediaco/media-v2/og-image.jpg">'):
        assert out.count(attr) == 1, attr
        out = out.replace(attr, attr + "<!-- EDIT -->")

    out = re.sub(r'"media-v2/([^"]+)"', r'"__MEDIA_\1__"', out)

    out = re.sub(r'</body>\n</html>\n?\Z', '\n</body></html>', out)
    return out


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--check":
        got = transform(pathlib.Path(sys.argv[2]).read_text())
        want = pathlib.Path(sys.argv[3]).read_text()
        if norm(got) == norm(want):
            print("transform reproduces the tokenized file")
        else:
            a, b = norm(got), norm(want)
            i = next(i for i in range(min(len(a), len(b))) if a[i] != b[i])
            print("MISMATCH at", i, "\n got:", a[i-120:i+120], "\nwant:", b[i-120:i+120])
            sys.exit(1)
    else:
        (HERE / "site-v2-tokenized.html").write_text(transform((HERE.parent / "index.html").read_text()))
        print("site-v2-tokenized.html regenerated from index.html")
