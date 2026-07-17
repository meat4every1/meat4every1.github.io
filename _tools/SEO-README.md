# SEO Diary / README

Personal site SEO for **www.iancw.com** (Ian C. Woskey — Senior / Lead Technical Artist & Technical Director targeting).

## Search Console status

- **Submitted:** Site and sitemap (`https://www.iancw.com/sitemap.xml`) to Google Search Console via the **Meat4every1** account.
- Re-submit the sitemap after major URL or page additions. Ranking is not instant; GSC is for indexing and monitoring, not a guarantee of position.

## Positioning (do not drift)

| Priority | Role keywords |
|----------|----------------|
| Primary | Senior Technical Artist |
| Promotion / next hire | Lead Technical Artist, Technical Director |
| Supporting | Senior Technical Animator |

**Tools (public claims):** Maya, Unity, Blender first. Houdini may appear in schema / project meta where Genies work already documents it — **do not** add Houdini to the HTML resume proficiency list (scoped experience; avoid overselling breadth).

**Body copy:** Do not keyword-stuff About / Resume / project prose. SEO lives in titles, descriptions, canonicals, JSON-LD, alts, and visually hidden H1s.

## What lives where

| Asset | Purpose |
|-------|---------|
| Live page `<head>` | Unique title, meta description, canonical, Open Graph, Twitter Card, Person JSON-LD |
| `.visually-hidden` H1 | One per page; crawlable role ladder; **not** visible in layout |
| [robots.txt](robots.txt) | Allow site; `Disallow: /Archive/`; Sitemap URL |
| [sitemap.xml](sitemap.xml) | index, about, resume, gallery, contact only |
| [sidebar-content.html](sidebar-content.html) | Social `alt` text + LinkedIn for sameAs identity |
| OG image | `Img/logo.jpg` (site header) |

**Canonical base:** `https://www.iancw.com/`

**Exclude from sitemap:** `projects.html` (redirect), `projects2.html`, everything under `Archive/`.

## Per-page intent

| Page | Intent |
|------|--------|
| `index.html` | Portfolio proof; Senior/Lead TA + TD |
| `about.html` | Hire narrative; Lead TA & Technical Director in title |
| `resume.html` | Credentials scan for Lead / TD searches |
| `gallery.html` | Visual proof |
| `contact.html` | Conversion |

## How to update SEO safely

1. **Titles / descriptions** — Edit the `<head>` block on that page only. Keep ~50–60 char titles and ~150–160 char descriptions. Include Lead Technical Artist and/or Technical Director when the page can honestly support them.
2. **JSON-LD** — Keep `jobTitle` array in sync: Senior Technical Artist, Lead Technical Artist, Technical Director, Senior Technical Animator. Keep `sameAs` aligned with sidebar social URLs.
3. **H1** — Keep one `<h1 class="visually-hidden">…</h1>` after `<body>`; do **not** retag visible `<h3>` section headers as H1.
4. **Alts** — Logo and project headers: descriptive role/project text; no layout impact.
5. **New live page** — Add head package + H1 + entry in `sitemap.xml`. After deploy, refresh GSC (Meat4every1) if needed.
6. **Deploy** — Run `python _tools/bump-asset-hashes.py` (“prepare for deployment”) so CSS/JS `?v=` hashes refresh.

## Rationale (short)

1. Match how studios search: role + seniority + specialty (not “Homepage”).
2. Fix crawl identity so Google doesn’t invent weak snippets.
3. Person schema + LinkedIn `sameAs` ties the site to a real professional entity.
4. Preserve human trust — TDs reading About still see your voice.
5. Block Archive so old “Homepage” pages don’t compete with the live brand.

## Visual / copy constraints

- No redesign from SEO work; H1s use `.visually-hidden` in `style.css`.
- Browser tab titles **do** change (expected).
- Resume proficiency list: no Houdini add.

## Checklist after content or SEO edits

- [ ] Unique title + description + absolute canonical on each live page
- [ ] JSON-LD still lists Lead Technical Artist + Technical Director
- [ ] `sitemap.xml` / `robots.txt` still correct
- [ ] Asset hashes bumped before deploy
- [ ] (Optional) Confirm indexing in GSC under Meat4every1

## Diary

| Date | Note |
|------|------|
| 2026-07-13 | Initial Senior/Lead TA + Technical Director SEO package: heads, OG, Person JSON-LD, hidden H1s, alts, robots + sitemap. Site + sitemap submitted to Google via **Meat4every1** account. |
