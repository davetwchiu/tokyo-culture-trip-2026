"""Validate rendered Jekyll pages using only Python's standard library."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import os
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
ORIGIN = "https://davetwchiu.github.io"
BASE = "/tokyo-culture-trip-2026"
issues = []


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = Counter()
        self.links = []
        self.tables = 0
        self.images = 0
        self.h1 = 0
        self.article = False
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article":
            self.article = True
        if attrs.get("id"):
            self.ids[attrs["id"]] += 1
        if tag == "h1":
            self.h1 += 1
        if tag == "table" and self.article:
            self.tables += 1
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "img":
            if self.article:
                self.images += 1
            if "alt" not in attrs:
                issues.append(f"{self.path}: image lacks alt attribute")

    def handle_endtag(self, tag):
        if tag == "article":
            self.article = False


def rendered_file(url_path):
    path = unquote(url_path)
    if path == BASE or path.startswith(BASE + "/"):
        path = path[len(BASE):]
    path = path.lstrip("/")
    file = ROOT / path
    if file.is_dir() or not path or path.endswith("/"):
        file = file / "index.html"
    return file


pages = {p: Page(p) for p in sorted(ROOT.rglob("*.html"))}
if not pages:
    sys.exit("No rendered HTML pages found")

sources = sorted(Path("content").rglob("*.md"))
expected_tables = 0
expected_images = 0
for source in sources:
    raw = source.read_text(encoding="utf-8")
    match = re.search(r"^permalink:\s*([^\n]+)", raw, re.M)
    if not match:
        issues.append(f"{source}: missing permalink")
        continue
    permalink = match.group(1).strip().strip("'\"")
    target = rendered_file(permalink)
    if target not in pages:
        issues.append(f"{source}: missing rendered page {target}")
        continue
    body = raw.split("---", 2)[-1]
    tables = len(re.findall(r"(?m)^\s*\|(?:\s*:?-{3,}:?\s*\|)+[ \t]*$", body))
    images = len(re.findall(r"!\[[^\]\n]*\]\(", body))
    expected_tables += tables
    expected_images += images
    page = pages[target]
    if page.tables != tables:
        issues.append(f"{source}: expected {tables} rendered tables, got {page.tables}")
    if page.images < images:
        issues.append(f"{source}: expected at least {images} rendered images, got {page.images}")

checked_links = 0
for file, page in pages.items():
    if page.h1 != 1:
        issues.append(f"{file}: expected one h1, got {page.h1}")
    for anchor, count in page.ids.items():
        if count > 1:
            issues.append(f"{file}: duplicate id #{anchor}")
    relative = file.relative_to(ROOT).as_posix()
    location = ORIGIN + BASE + "/" + relative
    if relative.endswith("index.html"):
        location = location[:-len("index.html")]
    for href in page.links:
        url = urlsplit(urljoin(location, href))
        if url.scheme not in ("http", "https") or url.netloc != urlsplit(ORIGIN).netloc:
            continue
        if url.path != BASE and not url.path.startswith(BASE + "/"):
            continue
        checked_links += 1
        target = rendered_file(url.path)
        if not target.exists():
            issues.append(f"{file}: broken internal link {href}")
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            issues.append(f"{file}: missing anchor {href}")

issues = sorted(set(issues))
lines = [
    f"Checked {len(sources)} source pages, {len(pages)} rendered pages, "
    f"{expected_tables} Markdown tables, {expected_images} Markdown images, "
    f"and {checked_links} internal links.",
    f"Found {len(issues)} unique issue(s).",
    *issues,
]
report = "\n".join(lines)
print(report)
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
        summary.write("## Site quality check\n\n" + "\n\n".join(lines[:2]) + "\n\n")
        summary.write("\n".join("- " + item for item in issues) + "\n")
sys.exit(1 if issues else 0)
