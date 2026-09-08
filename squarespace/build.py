#!/usr/bin/env python3
"""
Split the 508 Media Co. site into the two pieces Squarespace needs.

  01-site-header-injection.html -> Settings > Advanced > Code Injection > HEADER
  02-code-block.html            -> the Code Block on the blank Home page
  03-seo-fields.txt             -> values to type into Squarespace's SEO panel

Source of truth is site-v2-tokenized.html (the published artifact with its
embedded media pulled out to squarespace/extracted/ and replaced by
__MEDIA_<name>__ tokens).

Fill in asset-map.json (Squarespace file URLs) and config.json (booking URL),
then re-run. Re-run after any edit to the source.
"""
import json, re, pathlib

HERE   = pathlib.Path(__file__).resolve().parent
SRC    = (HERE / "site-v2-tokenized.html").read_text()
ASSETS = json.loads((HERE / "asset-map.json").read_text())
CONFIG = json.loads((HERE / "config.json").read_text()) if (HERE / "config.json").exists() else {}
WRAP   = "#mc508"

# ------------------------------------------------------------- CSS scoping

def strip_comments(css):
    """A comment containing a brace would desync the depth counter below, and
    comments also glue themselves onto the next selector's prelude."""
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)

def split_top_level(css):
    out, depth, buf, prelude = [], 0, "", None
    for ch in css:
        if ch == "{":
            depth += 1
            if depth == 1:
                prelude, buf = buf, ""
                continue
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append((prelude, buf)); buf, prelude = "", None
                continue
        buf += ch
    if buf.strip():
        out.append((buf, None))
    return out

# Stay global: they define tokens or paint the page itself.
GLOBAL_EXACT = {"::selection", "html", ":root"}

def scope_selector(sel):
    parts = []
    for one in (p.strip() for p in sel.split(",")):
        if not one:
            continue
        if one.startswith(":root") or one in GLOBAL_EXACT:
            parts.append(one)
        elif one == "body":
            parts.append(WRAP)
        elif one.startswith("body"):
            parts.append(WRAP + one[4:])          # body::after -> #mc508::after
        elif one == "*":
            parts.append(f"{WRAP}, {WRAP} *")
        elif one.startswith("*"):
            parts.append(f"{WRAP} *{one[1:]}")    # *::before -> #mc508 *::before
        else:
            parts.append(f"{WRAP} {one}")
    return ", ".join(parts)

def scope_css(css):
    out = []
    for prelude, body in split_top_level(css):
        if body is None:
            out.append(prelude); continue
        p = prelude.strip()
        if p.startswith("@keyframes") or p.startswith("@font-face"):
            out.append(f"{p}{{{body}}}")
        elif p.startswith("@media") or p.startswith("@supports"):
            out.append(f"{p}{{{scope_css(body)}}}")
        else:
            if p == "body":
                # As a plain div, overflow-x:hidden makes the wrapper a scroll
                # container, which silently kills position:sticky on .pin.
                # overflow-x:clip clips identically without becoming one.
                body = body.replace("overflow-x:hidden", "overflow-x:clip")
            out.append(f"{scope_selector(p)}{{{body}}}")
    return "\n".join(out)

# ------------------------------------------------------------- extract parts

doc       = SRC[SRC.index("<body>") + 6 : SRC.index("</body>")]
font_link = "\n".join(re.findall(r'<link rel="(?:preconnect|stylesheet)"[^>]*>', doc))
css       = "\n".join(re.findall(r"<style>(.*?)</style>", doc, re.S))
jsonld    = "\n".join(m.group(0) for m in
                      re.finditer(r'<script type="application/ld\+json">.*?</script>', doc, re.S))
scripts   = re.findall(r"<script>(.*?)</script>", doc, re.S)

title = re.search(r"<title>(.*?)</title>", doc, re.S).group(1).strip()
desc  = re.search(r'<meta name="description" content="(.*?)"', doc, re.S).group(1).strip()

# markup = everything that is not head-ish metadata, style or script
markup = doc
for pat in (r"<script.*?</script>", r"<style>.*?</style>", r"<title>.*?</title>",
            r'<meta[^>]*>', r'<link[^>]*>'):
    markup = re.sub(pat, "", markup, flags=re.S)
markup = re.sub(r"<!--.*?-->", "", markup, flags=re.S).strip()

# ------------------------------------------------------- placeholder filling

unresolved, deferred = [], []

booking = (CONFIG.get("booking_url") or "").strip()
body_js = "\n".join(scripts)
if booking:
    markup  = markup.replace("__BOOKING_URL__", booking)
    body_js = body_js.replace("__BOOKING_URL__", booking)
elif "__BOOKING_URL__" in markup:
    # Ship-safe: with no calendar yet, drop the button rather than render a dead
    # link. The form, email and phone in the same section still convert.
    markup = re.sub(r'\s*<a class="btn js-gcal"[^>]*>.*?</a>', "", markup, flags=re.S)
    markup = re.sub(r'\s*<p class="micro rv"[^>]*>Picks a time straight off my calendar[^<]*</p>', "", markup)
    deferred.append("booking button hidden (no booking_url yet) - add it after launch, re-run, re-paste block 02")

# The form posts into the shared Google Form (same backend as 508 Filmzz).
# Nothing to configure — no form service, no key.

for name, url in ASSETS.items():
    tok = f"__MEDIA_{name}__"
    if url:
        markup, body_js = markup.replace(tok, url), body_js.replace(tok, url)
    elif tok in markup + body_js:
        unresolved.append(f"{name} -> upload to Squarespace, paste URL in asset-map.json")

# ------------------------------------------------- Squarespace chrome overrides

CHROME = """
/* ==========================================================
   508 MEDIA CO. — Squarespace container overrides
   Neutralises Squarespace's page chrome so the injected site
   renders edge to edge exactly as it does standalone.
   ========================================================== */

/* Squarespace's own header, footer and announcement bar. */
#header, .header, #footer-sections, footer.sections,
.sqs-announcement-bar-dropzone { display: none !important; }

/* Strip every layer of padding / max-width between the page root and
   our Code Block so the site can run full bleed. */
#sections .page-section, #sections .section-border,
#sections .content-wrapper, .page-section > .content-wrapper,
.sqs-layout, .sqs-row, .row.sqs-row, .col, [class*="sqs-col"],
.sqs-block, .sqs-block.code-block, .sqs-block-code, .sqs-block-content {
  padding: 0 !important; margin: 0 !important;
  max-width: none !important; width: 100% !important;
}

/* CRITICAL: position:sticky (the pinned process section) only works when no
   ancestor is a scroll container. Squarespace sets overflow:hidden on several
   wrappers, .sqs-row included. overflow:visible restores sticky. */
#siteWrapper, #page, #sections, article, .page-section, .section-border,
.content-wrapper, .content, .sqs-layout, .sqs-row, .row.sqs-row, .col,
[class*="sqs-col"], .sqs-block, .sqs-block-content { overflow: visible !important; }

#sections .page-section { min-height: 0 !important; }

/* CRITICAL: position:fixed (the nav bar and the mobile CTA dock) is anchored
   to the viewport ONLY while no ancestor establishes a containing block.
   transform / filter / perspective / will-change / contain all do. Squarespace
   templates and section animations apply these, which would silently re-anchor
   the fixed nav inside the section and break it. */
#siteWrapper, #page, #sections, article, .page-section, .section-border,
.content-wrapper, .content, .sqs-layout, .sqs-row, .row.sqs-row, .col,
[class*="sqs-col"], .sqs-block, .sqs-block-content {
  transform: none !important; filter: none !important;
  perspective: none !important; will-change: auto !important;
  contain: none !important; backdrop-filter: none !important;
}

/* Squarespace styles h1-h6, p, a, form controls directly, and a direct rule
   beats our inherited colour. Re-assert inheritance inside the wrapper. */
#mc508 h1, #mc508 h2, #mc508 h3, #mc508 h4, #mc508 h5, #mc508 h6,
#mc508 p, #mc508 li, #mc508 span, #mc508 strong, #mc508 em, #mc508 blockquote,
#mc508 figure, #mc508 figcaption { color: inherit; font-family: inherit; }
#mc508 input, #mc508 select, #mc508 textarea, #mc508 button {
  font-family: inherit; letter-spacing: inherit;
}
#mc508 a { color: inherit; text-decoration: none; }

/* Clip horizontal overflow WITHOUT creating a scroll container (see above). */
#mc508 { overflow-x: clip; }

/* The page itself, behind the wrapper. */
body { background: var(--ink) !important; margin: 0 !important; }
"""

# ------------------------------------------------------------------- emit

(HERE / "01-site-header-injection.html").write_text(f"""<!--
  508 MEDIA CO. — paste into Settings > Advanced > Code Injection > HEADER
  Generated by build.py. Do not hand-edit: edit the source and re-run.
-->
{font_link}
<style>
{CHROME}

/* ==========================================================
   508 MEDIA CO. — site styles, rescoped under {WRAP}
   ========================================================== */
{scope_css(strip_comments(css))}
</style>

{jsonld}
""")

(HERE / "02-code-block.html").write_text(f"""<!--
  508 MEDIA CO. — paste into the Code Block on the blank Home page.
  Requires 01-site-header-injection.html to be in Code Injection already.
-->
<div id="mc508">
{markup}
</div>
<script>
{body_js}
</script>
""")

(HERE / "03-seo-fields.txt").write_text(
    "Type these into Squarespace's own SEO panel, NOT the code block.\n"
    "Squarespace generates its own <title> and OG tags; a second set fights it.\n"
    "Home page > Page Settings > SEO\n\n"
    f"SEO Title:\n{title}\n\nSEO Description:\n{desc}\n")

a = (HERE / "01-site-header-injection.html").read_text()
b = (HERE / "02-code-block.html").read_text()
print(f"01-site-header-injection.html  {len(a):>7,} bytes")
print(f"02-code-block.html             {len(b):>7,} bytes")
print(f"03-seo-fields.txt              written")
if unresolved:
    print(f"\nBLOCKING ({len(unresolved)}) — the page will look broken without these:")
    for u in unresolved: print("  x " + u)
else:
    print("\nNo blockers — ready to paste.")
if deferred:
    print(f"\nDeferred ({len(deferred)}) — safe to launch without, add later:")
    for d in deferred: print("  . " + d)
