# 508 Media Co. → Squarespace

Publishing the site you built as an Artifact onto your own Squarespace plan and domain,
with booking running through your Google Workspace calendar.

---

## The one constraint you should know

Squarespace has no FTP, no HTML file upload, and no Developer Mode on version 7.1.
You **cannot** upload `index.html` and have Squarespace serve it as a site.

What we do instead: your site is a *single self-contained page*, so it goes into one
blank Squarespace page as a Code Block, with the CSS in Code Injection. Squarespace
hosts it, serves it, bills it on your existing plan, and puts it on your domain with
their SSL. The design is unchanged — verified pixel-for-pixel against a simulated
Squarespace DOM (see "What was tested").

---

## Files in this folder

| File | What it is |
|---|---|
| `01-site-header-injection.html` | Paste into **Code Injection → HEADER** |
| `02-code-block.html` | Paste into the **Code Block** on the blank page |
| `03-seo-fields.txt` | Type into Squarespace's **SEO panel** (not the code) |
| `extracted/` | 17 media files to upload (7.1 MB total, largest 1.3 MB) |
| `asset-map.json` | You fill in: uploaded file → Squarespace URL |
| `config.json` | You fill in: Google booking link, Formspree ID |
| `build.py` | Regenerates 01/02/03. Re-run after any edit |
| `site-v2-tokenized.html` | Source of truth (the artifact, media extracted out) |

Everything in `01`/`02`/`03` is generated. Edit `site-v2-tokenized.html` or the two
JSON files, then re-run `build.py` — never hand-edit the numbered files.

---

## Step 1 — Upload the 17 media files

**Website → Website Tools → Custom CSS → Custom Files → Add images or fonts**

Upload everything in `extracted/`. Limit is 20 MB per file; your largest is 1.3 MB.

Click each uploaded file — its URL appears at the top of the Custom CSS box. Copy that
URL into `asset-map.json` next to the matching filename:

```json
{
  "auto-build.jpg": "https://static1.squarespace.com/static/.../auto-build.jpg",
  "auto-build.mp4": "https://static1.squarespace.com/static/.../auto-build.mp4",
  ...
}
```

> If Custom Files rejects `.mp4` on your plan, use the fallback: add a temporary Image
> Block, open its **Link → File → Upload**, and use the `/s/filename.mp4` URL it gives
> you. Delete the temporary block afterwards; the file stays uploaded.

## Step 2 — Create the Google Workspace booking page

In **Google Calendar** (signed in as your Workspace account):

1. **Create → Appointment schedule**
2. Name it (e.g. "Discovery call"), set duration to 30 min and your available hours
3. Under **Booked appointment settings**, turn on **calendar conflict checking** so your
   existing events automatically block those slots
4. **Open booking page** → copy the link

Paste it into `config.json` as `booking_url`. It looks like
`https://calendar.google.com/calendar/appointments/schedules/AcZssZ...?gv=true`

This is included in your existing Workspace subscription — no extra cost. Bookings land
straight on your calendar and two-way sync is native. (Squarespace Scheduling / Acuity
would do the same job but is a separate $16–49/mo add-on on top of your website plan.)

## Step 3 — Connect the contact form

Your form's `FORM_ID` is currently empty, so the form tells people to email or call
instead of submitting. Create a form at **formspree.io**, take the part after `/f/` in
the endpoint, and put it in `config.json` as `formspree_id`.

> Alternative worth considering: a native **Squarespace Form Block** placed in a second
> section below the code block can deliver straight to your email and a Google Drive
> spreadsheet — no third party, and it uses the Workspace account you already pay for.
> It won't match the custom form's styling, which is why the built-in form is the default here.

## Step 4 — Rebuild

```bash
cd ~/claude/508mediaco/squarespace && python3 build.py
```

It prints anything still unresolved. Wait for **"All placeholders resolved."**

## Step 5 — Build the Squarespace page

1. **Pages → +** → add a **Blank** page, name it `Home`
2. Add a **Section**, then inside it add a **Code Block**
3. Delete the Code Block's placeholder content and paste **all** of `02-code-block.html`
4. Turn **off** the block's "Display Source Code" option if shown
5. Set the section's padding to minimum and width to **Full Bleed**
6. **Settings → Advanced → Code Injection → HEADER** → paste all of `01-site-header-injection.html`
7. Save

The injected CSS hides Squarespace's header, footer and announcement bar, so you don't
need to delete them — but disabling them in the editor too is harmless belt-and-braces.

## Step 6 — SEO and homepage

- Right-click the page in **Pages → Settings → SEO** → paste the two values from `03-seo-fields.txt`
- **Pages → Home → Set as Homepage**
- The structured data (business info, services, prices, FAQ) is already in the header
  injection — Squarespace doesn't generate that, so it's pure gain for local search.

## Step 7 — Domain

**Settings → Domains.** If `508mediaco.com` is already registered with Squarespace,
connect it to this site and Squarespace issues SSL automatically. If it's registered
elsewhere, point its nameservers or A/CNAME records at Squarespace per their instructions.

---

## What was tested

The build was verified against a deliberately hostile mock of the Squarespace 7.1 DOM —
`#siteWrapper`/`#page`/`#sections` with `overflow:hidden`, `.page-section` with a
`transform`, `.sqs-block-content` with `will-change`, a 960px `max-width` content wrapper,
and Squarespace-style `h1..h6/p/li/a/input` typography rules — with these results:

| Check | Result |
|---|---|
| Squarespace header + footer | hidden |
| Site width vs viewport | 529 / 529 — full bleed |
| Fixed nav survives ancestor `transform` | yes, stays viewport-anchored |
| Fonts (Schibsted Grotesk / IBM Plex Mono / Oswald) | all correct, no leakage |
| Colours across headings, body, forms | all correct |
| `.plan .px em` keeps IBM Plex Mono | yes — relative specificity preserved |
| Images | 9/9 loaded |
| Click-to-play video | creates `<video>`, plays |
| FAQ accordion | opens |
| Portfolio filter | "Automotive" → 8 items to 5 |
| Mobile burger menu | opens |
| Booking button | href resolves |

Two subtle failures were found and fixed during that testing:

1. **`overflow-x:hidden` → `overflow-x:clip`.** As a plain `<div>`, the wrapper's
   `overflow-x:hidden` would have made it a scroll container, silently breaking
   `position:sticky`. `clip` clips identically without becoming one.
2. **Containing-block defence.** `position:fixed` (the nav bar and mobile CTA dock) is
   viewport-anchored only while no ancestor has `transform`, `filter`, `perspective`,
   `will-change` or `contain`. Squarespace sections apply these. The injection now
   neutralises them on every wrapper between the page root and the code block.

## Rolling back

Everything lives in two places: the Code Injection header and the one Code Block.
Clear both and the site is gone with no residue. Nothing else on the account is touched.
