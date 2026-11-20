# Tokyo Culture Trip 2026

Public, Markdown-first website scaffold. This commit contains page structure only; guide and itinerary content is intentionally empty.

## Authoring contract

- Guide pages live in `content/**/*.md`; the reusable empty template is `_templates/EMPTY_PAGE.md`.
- Keep one page per Markdown file. Preserve the front matter keys and set `title`, `permalink`, `section`, and `parent` where applicable.
- The main menu reads pages with `navigation: true`. A section page lists children whose `parent` equals its permalink. New museum, building, work, glossary, map, or update pages appear automatically when they use the matching `parent` path; no layout, config, or workflow edits are needed.
- Set `source` to the primary source URL and `last_checked` to an ISO date (`YYYY-MM-DD`). Additional citations can live in the page body.
- Set `maps_query` to a place name or address for a Google Maps search link. `maps_destination` and optional `maps_origin` generate a directions link. Links within a page can use Google's `https://www.google.com/maps/search/?api=1&query=...` URL format.
- Pages marked `offline: true` are cached for offline reading after the first online visit.

### Stable page paths

| Page | Markdown source |
| --- | --- |
| Home | `content/home.md` |
| Itinerary | `content/itinerary.md` |
| History index and political, cultural, craft history | `content/history/index.md`, `content/history/political.md`, `content/history/culture.md`, `content/history/craft.md` |
| Museum index | `content/museums/index.md` |
| Tokyo National Museum and building index | `content/museums/tokyo-national-museum/index.md`, `content/museums/tokyo-national-museum/buildings/index.md` |
| Nezu Museum | `content/museums/nezu/index.md` |
| Featured works | `content/works/index.md` |
| Craft glossary | `content/craft-glossary/index.md` |
| Lunch | `content/lunch/index.md` |
| Maps and transport | `content/transport/index.md` |
| Updates | `content/updates/index.md` |

For a new museum, add `content/museums/<slug>/index.md` with `parent: /museums/`. For an individual Tokyo National Museum building, add `content/museums/tokyo-national-museum/buildings/<slug>.md` with `parent: /museums/tokyo-national-museum/buildings/`. Featured works use `content/works/<slug>.md`; glossary entries use `content/craft-glossary/<slug>.md`; map locations use `content/transport/<slug>.md`.

## Build and publishing

GitHub Actions builds the Jekyll site and publishes it to GitHub Pages after each push to `main`; `workflow_dispatch` is also available for a manual rebuild. The live site is `https://davetwchiu.github.io/tokyo-culture-trip-2026/`.

This repository and its Pages site are public so the link can be shared with friends. Every page and commit in this repository is visible publicly. Content edits made on `main` are published automatically.
