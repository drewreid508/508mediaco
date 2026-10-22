#!/usr/bin/env python3
"""
Hannah's Detailing & Supply fleet ads delivery → Squarespace + Artifact.

  page.html                                  source (edit this)
  squarespace-page-header-injection.html     paste into Page Settings → Advanced → Page Header Code Injection
  index.html                                 Artifact / local preview (assets relative, ./media)

Same pattern as hq-southpark: the site-wide 508 footer injection draws the homepage (#mc508) on
every page, so the injection hides it and mounts #hds508 from a <template> once the DOM is ready.
Tokens are {{KEY}} with full names only (a bare MEDIA token once ate the word in "508 MEDIA CO.").
"""
import pathlib

HERE = pathlib.Path(__file__).parent
STAR = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3 6.1 20.6l1.3-6.6L2.5 9.4l6.6-.8z"/></svg>')
CFG = {
    "MEDIA": "https://drewreid508.github.io/508mediaco/hds-fleet",
    "RAW_URL": "https://we.tl/t-3tanymarhkRG8KkO",   # raw footage WeTransfer, sent Oct 10, expires Nov 9
    "FINALS_URL": "https://we.tl/t-qX5yQbNr14e2fost",   # 4 v3 finals WeTransfer (re-sent Oct 12), expires ~Nov 11; empty removes that card
    "UPDATED": "Oct 12, 2026",
    "REVIEW_URL": "https://g.page/r/CQRtijkKqWhOEBI/review",
    "STARS": STAR * 5,
    "STAR": STAR,
    "CHART": ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20V10m6 10V4m6 16v-7m4 7H2"/></svg>'),
}

# ── Monthly videos ─────────────────────────────────────────────────────────────
# NEWEST MONTH FIRST. To add a month: drop the web copies (~10 MB, 1.55 Mbps, poster at 2 s)
# into media/ with a month suffix in the filename (dodges CDN caching), add an entry at the
# TOP of this list, run build.py, push, then re-paste the injection. Never delete old months.
MONTHS = [
    {   # Oct 21: 8 scripted $995 ads (Oct 19 shoot), 3 formats each. Download transfer not made yet.
        "id": "m2026-10-995", "month": "October", "year": "2026", "delivered": "Oct 22",
        "heading": "$995 <em>ceramic ads</em>", "dl": "https://we.tl/t-mMLt5zrDrHMLDT06", "expires": "Nov 21",   # 24 finals (8 ads x 9:16/4:5/16:9), sent Oct 22, t_exp 1795256973
        "videos": [
            {
                "id": "oct995-1", "kick": "$995 ceramic special", "title": "Lake Keowee <em>luxury owners</em>",
                "formats": [
                    ("Phone 9:16", "ad1-phone-oct995", "phone", "0:51", "1080 × 1920", "Reels · TikTok · Stories"),
                    ("Feed 4:5", "ad1-feed-oct995", "phone", "0:51", "1080 × 1350", "Meta ads · Instagram & Facebook feed"),
                    ("Widescreen", "ad1-wide-oct995", "wide", "0:51", "1920 × 1080", "website · YouTube · Facebook"),
                ],
            },
            {
                "id": "oct995-2", "kick": "$995 ceramic special", "title": "Verdae <em>picky owners</em>",
                "formats": [
                    ("Phone 9:16", "ad2-phone-oct995", "phone", "0:43", "1080 × 1920", "Reels · TikTok · Stories"),
                    ("Feed 4:5", "ad2-feed-oct995", "phone", "0:43", "1080 × 1350", "Meta ads · Instagram & Facebook feed"),
                    ("Widescreen", "ad2-wide-oct995", "wide", "0:43", "1920 × 1080", "website · YouTube · Facebook"),
                ],
            },
            {
                "id": "oct995-3", "kick": "$995 ceramic special", "title": "Lake Keowee <em>bugs &amp; pollen</em>",
                "formats": [
                    ("Phone 9:16", "ad3-phone-oct995", "phone", "0:48", "1080 × 1920", "Reels · TikTok · Stories"),
                    ("Feed 4:5", "ad3-feed-oct995", "phone", "0:48", "1080 × 1350", "Meta ads · Instagram & Facebook feed"),
                    ("Widescreen", "ad3-wide-oct995", "wide", "0:48", "1920 × 1080", "website · YouTube · Facebook"),
                ],
            },
            {
                "id": "oct995-4", "kick": "$995 ceramic special", "title": "Lake Keowee <em>keep it right</em>",
                "formats": [
                    ("Phone 9:16", "ad4-phone-oct995", "phone", "0:55", "1080 × 1920", "Reels · TikTok · Stories"),
                    ("Feed 4:5", "ad4-feed-oct995", "phone", "0:55", "1080 × 1350", "Meta ads · Instagram & Facebook feed"),
                    ("Widescreen", "ad4-wide-oct995", "wide", "0:55", "1920 × 1080", "website · YouTube · Facebook"),
                ],
            },
            {
                "id": "oct995-5", "kick": "$995 ceramic special", "title": "Verdae <em>don't pay full price</em>",
                "formats": [
                    ("Phone 9:16", "ad5-phone-oct995", "phone", "0:45", "1080 × 1920", "Reels · TikTok · Stories"),
                    ("Feed 4:5", "ad5-feed-oct995", "phone", "0:45", "1080 × 1350", "Meta ads · Instagram & Facebook feed"),
                    ("Widescreen", "ad5-wide-oct995", "wide", "0:45", "1920 × 1080", "website · YouTube · Facebook"),
                ],
            },
            {
                "id": "oct995-6", "kick": "$995 ceramic special", "title": "Verdae <em>dirty in 2 days</em>",
                "formats": [
                    ("Phone 9:16", "ad6-phone-oct995", "phone", "0:47", "1080 × 1920", "Reels · TikTok · Stories"),
                    ("Feed 4:5", "ad6-feed-oct995", "phone", "0:47", "1080 × 1350", "Meta ads · Instagram & Facebook feed"),
                    ("Widescreen", "ad6-wide-oct995", "wide", "0:47", "1920 × 1080", "website · YouTube · Facebook"),
                ],
            },
            {
                "id": "oct995-7", "kick": "$995 ceramic special", "title": "Upstate <em>sports cars</em>",
                "formats": [
                    ("Phone 9:16", "ad7-phone-oct995", "phone", "0:56", "1080 × 1920", "Reels · TikTok · Stories"),
                    ("Feed 4:5", "ad7-feed-oct995", "phone", "0:56", "1080 × 1350", "Meta ads · Instagram & Facebook feed"),
                    ("Widescreen", "ad7-wide-oct995", "wide", "0:56", "1920 × 1080", "website · YouTube · Facebook"),
                ],
            },
            {
                "id": "oct995-8", "kick": "$995 ceramic special", "title": "Upstate <em>SUVs</em>",
                "formats": [
                    ("Phone 9:16", "ad8-phone-oct995", "phone", "1:03", "1080 × 1920", "Reels · TikTok · Stories"),
                    ("Feed 4:5", "ad8-feed-oct995", "phone", "1:03", "1080 × 1350", "Meta ads · Instagram & Facebook feed"),
                    ("Widescreen", "ad8-wide-oct995", "wide", "1:03", "1920 × 1080", "website · YouTube · Facebook"),
                ],
            },
        ],
    },
    {
        "id": "m2026-10", "month": "October", "year": "2026", "delivered": "Oct 12",
        "dl": "https://we.tl/t-eiBYb4ezRnk8aLFH", "expires": "Nov 11",   # v3 + music finals, sent Oct 12 ~7:40 PM, t_exp = 2026-11-11 (v3 no-music t-tioT368cyyFn3e3D, v2 t-2NtJ7CPcF0MmRquZ, v1 t-SMvrTTqvbZG4zD6O)
        "videos": [
            {
                "id": "oct-mustang", "kick": "$995 ceramic special", "title": "2025 <em>Mustang</em>",
                "formats": [  # (button, file stem, fmt class, length, size, use)
                    ("Phone 9:16", "mustang-phone-oct-v3m", "phone", "0:51", "1080 × 1920", "Reels · TikTok · Stories"),
                    ("Feed 4:5", "mustang-feed-oct-v3m", "phone", "0:51", "1080 × 1350", "Instagram & Facebook feed"),
                ],
            },
        ],
    },
]

def month_html(m, newest):
    n = len(m["videos"])
    out = [f'  <section class="month" aria-labelledby="{m["id"]}">',
           f'    <div class="monthhead">' + ('<span class="badge">New</span>' if newest else '') +
           (f'<p class="kick">Monthly videos · {m["month"]} {m["year"]}</p><h2 id="{m["id"]}">{m["heading"]}</h2>' if m.get("heading") else
            f'<p class="kick">Monthly videos</p><h2 id="{m["id"]}">{m["month"]} <em>{m["year"]}</em></h2>') +
           f'<p class="when">{n} video{"s" if n != 1 else ""} · delivered {m["delivered"]}, {m["year"]}</p></div>']
    for k, v in enumerate(m["videos"], 1):
        f0 = v["formats"][0]
        btns = "\n".join(
            f'        <button type="button" aria-pressed="{str(i == 0).lower()}" data-target="{v["id"]}" '
            f'data-src="{{{{MEDIA}}}}/media/{f[1]}.mp4" data-poster="{{{{MEDIA}}}}/media/{f[1]}.jpg" data-fmt="{f[2]}" '
            f'data-len="{f[3]}" data-size="{f[4]}" data-use="{f[5]}">{f[0]}</button>'
            for i, f in enumerate(v["formats"]))
        out.append(f"""    <section class="reel" aria-labelledby="{v['id']}-title">
      <div class="reelhead">
        <div><p class="kick">{m['month']} · {k:02d} · {v['kick']}</p><h2 id="{v['id']}-title">{v['title']}</h2></div>
        <div class="seg" role="group" aria-label="Video version">
{btns}
        </div>
      </div>
      <div class="screen{' phone' if f0[2] == 'phone' else ''}" id="{v['id']}-screen"><video id="{v['id']}" controls playsinline preload="metadata" poster="{{{{MEDIA}}}}/media/{f0[1]}.jpg" src="{{{{MEDIA}}}}/media/{f0[1]}.mp4"></video></div>
      <div class="specs" id="{v['id']}-specs"><span><b>Length</b> {f0[3]}</span><span><b>Size</b> {f0[4]}</span><span><b>Use</b> {f0[5]}</span></div>
    </section>""")
    out.append(f"""    <div class="files" style="grid-template-columns:1fr">
      <div class="file" data-dl="{m['dl']}" data-label="Download {m['month']}'s videos">
        <b>{m['month']}'s videos · full quality</b>
        <p>Every {m['month']} video in full 1080p, ready to post. The players above are web-size copies. {(' Link works until <b style="font-size:inherit">' + m['expires'] + '</b>, so save the files somewhere you\'ll keep them.') if m['expires'] else ''}</p>
      </div>
    </div>
  </section>""")
    return "\n".join(out)

def render(media):
    src = (HERE / "page.html").read_text()
    src = src.replace("{{MONTHS}}", "\n".join(month_html(m, i == 0) for i, m in enumerate(MONTHS)))
    for k, v in {**CFG, "MEDIA": media}.items():
        src = src.replace("{{" + k + "}}", v)
    assert "{{" not in src, "unfilled token"
    head = src[src.index('<link rel="preconnect"'):src.index("</style>") + len("</style>")]
    body = src[src.index('<div id="hds508">'):src.index("<script>")].strip()
    script = src[src.index("<script>") + len("<script>"):src.index("</script>")].strip()
    return head, body, script

head, body, script = render(CFG["MEDIA"])
injection = f"""<!-- 508 Media Co. | Hannah's Detailing & Supply delivery page (508mediaco.com/hds-delivery). Generated by hds-fleet/build.py; edit page.html. -->
<meta name="robots" content="noindex,nofollow">
<meta property="og:image" content="{CFG['MEDIA']}/media/ceramic-wide-v3.jpg">
{head}
<style>#mc508{{display:none!important}} html,body{{background:#06070A!important}}</style>
<template id="hds508tpl">
{body}
</template>
<script>
document.addEventListener('DOMContentLoaded', function(){{
  var t = document.getElementById('hds508tpl');
  if (!t || document.getElementById('hds508')) return;
  document.body.appendChild(t.content.cloneNode(true));
  {script}
}});
</script>
"""
(HERE / "squarespace-page-header-injection.html").write_text(injection)

head, body, script = render(".")
(HERE / "index.html").write_text(f"""<title>Hannah's Delivery</title>
{head}<style>:root{{color-scheme:dark;background:#06070A}} html,body{{margin:0;background:#06070A}}</style>
{body}
<script>{script}</script>
""")
print("injection", len(injection), "bytes")
