from __future__ import annotations

import html
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
OUTPUT_DIR = ROOT / "site"
ASSETS_DIR = ROOT / "assets"
LIBRARY_DIR = ROOT / "library"

SHELF_ORDER = {
    "chetty-start": 0,
    "foundations": 1,
    "recent": 2,
}

SHELF_LABELS = {
    "chetty-start": "Start Here",
    "foundations": "Foundations",
    "recent": "Recent",
}


def parse_metadata(raw: str) -> tuple[dict[str, object], str]:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, flags=re.DOTALL)
    if not match:
        return {}, raw

    metadata: dict[str, object] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if "|" in value:
            metadata[key] = [item.strip() for item in value.split("|") if item.strip()]
        elif value.lower() in {"yes", "true"}:
            metadata[key] = True
        elif value.lower() in {"no", "false"}:
            metadata[key] = False
        else:
            metadata[key] = value

    return metadata, match.group(2).strip() + "\n"


def render_inline(text: str) -> str:
    placeholders: list[str] = []

    def stash(raw_html: str) -> str:
        placeholders.append(raw_html)
        return f"@@PLACEHOLDER{len(placeholders) - 1}@@"

    escaped = html.escape(text)

    escaped = re.sub(
        r"`([^`]+)`",
        lambda m: stash(f"<code>{m.group(1)}</code>"),
        escaped,
    )
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: stash(
            f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>'
        ),
        escaped,
    )
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)

    for index, raw_html in enumerate(placeholders):
        escaped = escaped.replace(f"@@PLACEHOLDER{index}@@", raw_html)
    return escaped


def render_markdown(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    chunks: list[str] = []
    paragraph: list[str] = []
    quote_lines: list[str] = []
    list_items: list[str] = []
    list_kind: str | None = None
    code_lines: list[str] = []
    code_lang = ""
    in_code = False

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(part.strip() for part in paragraph).strip()
            chunks.append(f"<p>{render_inline(text)}</p>")
            paragraph.clear()

    def flush_quote() -> None:
        if quote_lines:
            text = " ".join(part.strip() for part in quote_lines).strip()
            chunks.append(f"<blockquote><p>{render_inline(text)}</p></blockquote>")
            quote_lines.clear()

    def flush_list() -> None:
        nonlocal list_kind
        if not list_items:
            return
        tag = "ul" if list_kind == "ul" else "ol"
        items = "".join(f"<li>{render_inline(item)}</li>" for item in list_items)
        chunks.append(f"<{tag}>{items}</{tag}>")
        list_items.clear()
        list_kind = None

    def flush_code() -> None:
        nonlocal code_lang
        if not code_lines:
            return
        escaped = html.escape("\n".join(code_lines))
        lang_attr = f" language-{code_lang}" if code_lang else ""
        chunks.append(
            '<div class="code-block">'
            '<button class="copy-button" type="button">Copy</button>'
            f'<pre><code class="{lang_attr.strip()}">{escaped}</code></pre>'
            "</div>"
        )
        code_lines.clear()
        code_lang = ""

    for line in lines:
        stripped = line.rstrip()

        if in_code:
            if stripped.startswith("```"):
                flush_code()
                in_code = False
            else:
                code_lines.append(stripped)
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            flush_quote()
            flush_list()
            in_code = True
            code_lang = stripped[3:].strip()
            continue

        if not stripped:
            flush_paragraph()
            flush_quote()
            flush_list()
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            flush_quote()
            flush_list()
            chunks.append(f"<h1>{render_inline(stripped[2:].strip())}</h1>")
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            flush_quote()
            flush_list()
            chunks.append(f"<h2>{render_inline(stripped[3:].strip())}</h2>")
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            flush_quote()
            flush_list()
            chunks.append(f"<h3>{render_inline(stripped[4:].strip())}</h3>")
            continue

        if stripped.startswith("> "):
            flush_paragraph()
            flush_list()
            quote_lines.append(stripped[2:].strip())
            continue

        unordered = re.match(r"^- (.+)$", stripped)
        ordered = re.match(r"^\d+\. (.+)$", stripped)
        if unordered or ordered:
            flush_paragraph()
            flush_quote()
            item = unordered.group(1) if unordered else ordered.group(1)
            incoming_kind = "ul" if unordered else "ol"
            if list_kind and list_kind != incoming_kind:
                flush_list()
            list_kind = incoming_kind
            list_items.append(item.strip())
            continue

        paragraph.append(stripped)

    flush_paragraph()
    flush_quote()
    flush_list()
    flush_code()
    return "\n".join(chunks)


def load_entries(folder: str) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for path in sorted((CONTENT_DIR / folder).glob("*.md")):
        metadata, body = parse_metadata(path.read_text(encoding="utf-8"))
        metadata["body"] = body
        metadata["html"] = render_markdown(body)
        metadata["slug"] = metadata.get("slug", path.stem)
        metadata["path"] = path
        entries.append(metadata)
    return entries


def base_layout(
    *,
    title: str,
    description: str,
    root_prefix: str,
    body_class: str,
    main_content: str,
) -> str:
    nav_home = f"{root_prefix}/index.html"
    nav_articles = f"{root_prefix}/articles/index.html"
    nav_themes = f"{root_prefix}/themes/index.html"
    nav_notes = f"{root_prefix}/add-your-thoughts.html"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="stylesheet" href="{root_prefix}/assets/styles.css">
</head>
<body class="{body_class}">
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="{nav_home}">Labor Supply Wiki</a>
      <nav class="site-nav" aria-label="Primary">
        <a href="{nav_articles}">Articles</a>
        <a href="{nav_themes}">Themes</a>
        <a href="{nav_notes}">Your Thoughts</a>
      </nav>
    </div>
  </header>
  <main class="page-shell">
    {main_content}
  </main>
  <footer class="site-footer">
    <p>Built from local markdown, saved PDF copies, and source links. Open <code>site/index.html</code> on any device-friendly browser.</p>
  </footer>
  <script src="{root_prefix}/assets/app.js"></script>
</body>
</html>
"""


def tag_badges(tags: list[str]) -> str:
    return "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in tags[:5])


def article_card(article: dict[str, object], root_prefix: str) -> str:
    href = f"{root_prefix}/articles/{article['slug']}.html"
    tags = article.get("tags", [])
    tag_html = tag_badges(tags if isinstance(tags, list) else [])
    journal_line = article.get("journal", "")
    year = article.get("year", "")
    shelf_label = SHELF_LABELS.get(str(article.get("shelf", "")), "")
    tag_search = " ".join(tags if isinstance(tags, list) else [])
    return f"""
    <article class="card searchable-card" data-search="{html.escape(str(article.get('title', ''))).lower()} {html.escape(str(article.get('deck', ''))).lower()} {html.escape(tag_search).lower()}">
      <p class="eyebrow">{html.escape(shelf_label)} - {html.escape(str(year))}</p>
      <h3><a href="{href}">{html.escape(str(article.get('title', '')))}</a></h3>
      <p class="meta-line">{html.escape(str(journal_line))}</p>
      <p>{html.escape(str(article.get('deck', '')))}</p>
      <div class="tag-row">{tag_html}</div>
    </article>
    """


def theme_card(theme: dict[str, object], root_prefix: str) -> str:
    href = f"{root_prefix}/themes/{theme['slug']}.html"
    return f"""
    <article class="card">
      <p class="eyebrow">Theme</p>
      <h3><a href="{href}">{html.escape(str(theme.get('title', '')))}</a></h3>
      <p>{html.escape(str(theme.get('deck', '')))}</p>
    </article>
    """


def article_meta(article: dict[str, object], root_prefix: str) -> str:
    raw_pdf_path = str(article.get("pdf_path", "")).strip()
    pdf_path = ""
    if raw_pdf_path:
        if raw_pdf_path.startswith(("http://", "https://")):
            pdf_path = raw_pdf_path
        else:
            pdf_path = f"{root_prefix}/{raw_pdf_path}"

    source_url = str(article.get("source_url", "")).strip()
    doi = article.get("doi", "")
    related_themes = article.get("related_themes", [])
    theme_links = []
    for slug in related_themes if isinstance(related_themes, list) else []:
        theme_links.append(f'<a class="pill-link" href="{root_prefix}/themes/{slug}.html">{html.escape(slug.replace("-", " "))}</a>')

    button_parts: list[str] = []
    if pdf_path:
        pdf_label = "Open PDF" if raw_pdf_path.startswith(("http://", "https://")) else "Open local PDF"
        button_parts.append(f'<a class="button" href="{html.escape(pdf_path, quote=True)}">{pdf_label}</a>')

    if source_url:
        source_button_class = "button subtle" if button_parts else "button"
        button_parts.append(
            f'<a class="{source_button_class}" href="{html.escape(source_url, quote=True)}">Open source page</a>'
        )

    doi_line = ""
    if doi:
        doi_url = f"https://doi.org/{doi}"
        doi_line = f'<dt>DOI</dt><dd><a href="{doi_url}">{html.escape(str(doi))}</a></dd>'

    copy_type = str(article.get("copy_type", "")).strip()
    saved_pdf_line = ""
    if copy_type:
        saved_pdf_line = f"<dt>Saved PDF</dt><dd>{html.escape(copy_type)}</dd>"

    author_list = article.get("authors", [])
    if not isinstance(author_list, list):
        author_list = [str(author_list)]

    return f"""
    <aside class="sidebar-card">
      <div class="button-stack">
        {''.join(button_parts)}
      </div>
      <dl class="meta-grid">
        <dt>Authors</dt>
        <dd>{html.escape(', '.join(author_list))}</dd>
        <dt>Journal</dt>
        <dd>{html.escape(str(article.get('journal', '')))}</dd>
        <dt>Year</dt>
        <dd>{html.escape(str(article.get('year', '')))}</dd>
        {saved_pdf_line}
        {doi_line}
      </dl>
      <div class="sidebar-section">
        <p class="sidebar-label">Related themes</p>
        <div class="pill-row">{''.join(theme_links) if theme_links else '<span class="muted">Theme links will appear here as the collection grows.</span>'}</div>
      </div>
    </aside>
    """


def theme_article_links(theme: dict[str, object], articles_by_slug: dict[str, dict[str, object]]) -> str:
    cards = []
    featured = theme.get("featured_articles", [])
    for slug in featured if isinstance(featured, list) else []:
        article = articles_by_slug.get(slug)
        if article:
            cards.append(article_card(article, ".."))
    return "".join(cards)


def write_page(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def copy_tree_contents(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    destination.mkdir(parents=True, exist_ok=True)
    for item in source.rglob("*"):
        target = destination / item.relative_to(source)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(item.read_bytes())


def article_sort_key(article: dict[str, object]) -> tuple[int, int, str]:
    year_text = str(article.get("year", "0"))
    try:
        year = int(year_text)
    except ValueError:
        year = 0
    shelf_rank = SHELF_ORDER.get(str(article.get("shelf", "")), 99)
    return (shelf_rank, -year, str(article.get("title", "")))


def build() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    copy_tree_contents(ASSETS_DIR, OUTPUT_DIR / "assets")
    copy_tree_contents(LIBRARY_DIR, OUTPUT_DIR / "library")

    articles = sorted(load_entries("articles"), key=article_sort_key)
    themes = load_entries("themes")
    pages = load_entries("pages")
    articles_by_slug = {str(article["slug"]): article for article in articles}

    start_here_cards = "".join(
        article_card(article, ".")
        for article in articles
        if article.get("shelf") == "chetty-start"
    )
    foundation_cards = "".join(
        article_card(article, ".")
        for article in articles
        if article.get("shelf") == "foundations"
    )
    recent_cards = "".join(
        article_card(article, ".")
        for article in articles
        if article.get("shelf") == "recent"
    )
    theme_cards = "".join(theme_card(theme, ".") for theme in themes)

    home = base_layout(
        title="Labor Supply Wiki",
        description="A responsive labor supply research wiki built from peer-reviewed articles and local PDF copies.",
        root_prefix=".",
        body_class="home-body",
        main_content=f"""
        <section class="hero">
          <div class="hero-copy">
            <p class="eyebrow">Research-first collection</p>
            <h1>Labor supply research that is readable on a phone and still useful at a desk.</h1>
            <p class="lead">This wiki starts with Raj Chetty and nearby papers around 2010, then reaches backward to the 1970s and 1980s foundations, and forward to newer policy and review work. Featured articles carry short summaries, copyable BibTeX, and either a saved PDF copy or a stable source link.</p>
            <div class="button-row">
              <a class="button" href="./articles/index.html">Browse articles</a>
              <a class="button subtle" href="./themes/index.html">Browse themes</a>
            </div>
          </div>
          <div class="hero-panel">
            <h2>Collection rules</h2>
            <ul>
              <li>Article pages are mainly for peer-reviewed research, with a small number of frontier working papers included when they are especially useful.</li>
              <li>When an open PDF is available, the page keeps a saved local copy tied to the article or working-paper version; otherwise it links to the source page until a stable open copy is found.</li>
              <li>Theme pages connect papers across decades, methods, and margins of labor supply.</li>
            </ul>
          </div>
        </section>
        <section class="section">
          <div class="section-head">
            <h2>Start Here: Chetty Around 2010</h2>
            <p>The first shelf is meant to orient the whole wiki.</p>
          </div>
          <div class="card-grid">
            {start_here_cards}
          </div>
        </section>
        <section class="section">
          <div class="section-head">
            <h2>Foundations: 1970s and 1980s</h2>
            <p>These papers give the basic language for life-cycle, family, tax, and elasticity questions.</p>
          </div>
          <div class="card-grid">
            {foundation_cards}
          </div>
        </section>
        <section class="section">
          <div class="section-head">
            <h2>Recent Work</h2>
            <p>These pages show how the literature keeps moving on incentives, cross-country policy, and elasticity measurement.</p>
          </div>
          <div class="card-grid">
            {recent_cards}
          </div>
        </section>
        <section class="section">
          <div class="section-head">
            <h2>Theme Pages</h2>
            <p>Use these when you want connections instead of isolated summaries.</p>
          </div>
          <div class="card-grid">
            {theme_cards}
          </div>
        </section>
        <section class="section note-callout">
          <div>
            <p class="eyebrow">Your notes</p>
            <h2>Free-flow thoughts from Google Docs can come into the wiki cleanly.</h2>
            <p>There is a ready staging file in <code>notes/inbox/google-doc-notes.md</code>. When you tell me to integrate your notes, I can turn that raw dump into article-side notes, theme synthesis, or a new page.</p>
          </div>
          <a class="button" href="./add-your-thoughts.html">See the workflow</a>
        </section>
        """,
    )
    write_page(OUTPUT_DIR / "index.html", home)

    articles_index = base_layout(
        title="Articles | Labor Supply Wiki",
        description="Browse article summaries, local PDFs, and BibTeX for the labor supply wiki.",
        root_prefix="..",
        body_class="listing-body",
        main_content=f"""
        <section class="listing-header">
          <p class="eyebrow">Articles</p>
          <h1>Article summaries</h1>
          <p>Search by author, theme, method, or keyword.</p>
          <label class="search-box">
            <span>Search</span>
            <input type="search" placeholder="Try 'Chetty', 'family', or 'Frisch'" data-filter-input>
          </label>
        </section>
        <section class="card-grid" data-filter-target>
          {''.join(article_card(article, '..') for article in articles)}
        </section>
        """,
    )
    write_page(OUTPUT_DIR / "articles" / "index.html", articles_index)

    themes_index = base_layout(
        title="Themes | Labor Supply Wiki",
        description="Browse cross-cutting theme pages for the labor supply wiki.",
        root_prefix="..",
        body_class="listing-body",
        main_content=f"""
        <section class="listing-header">
          <p class="eyebrow">Themes</p>
          <h1>Cross-paper idea pages</h1>
          <p>These pages connect articles that speak to the same question from different decades or methods.</p>
        </section>
        <section class="card-grid">
          {''.join(theme_card(theme, '..') for theme in themes)}
        </section>
        """,
    )
    write_page(OUTPUT_DIR / "themes" / "index.html", themes_index)

    for article in articles:
        page = base_layout(
            title=f"{article['title']} | Labor Supply Wiki",
            description=str(article.get("deck", "")),
            root_prefix="..",
            body_class="article-body",
            main_content=f"""
            <section class="article-header">
              <p class="eyebrow">{html.escape(str(article.get('journal', '')))} - {html.escape(str(article.get('year', '')))}</p>
              <h1>{html.escape(str(article.get('title', '')))}</h1>
              <p class="lead">{html.escape(str(article.get('deck', '')))}</p>
            </section>
            <section class="article-layout">
              {article_meta(article, '..')}
              <article class="prose">
                {article['html']}
              </article>
            </section>
            """,
        )
        write_page(OUTPUT_DIR / "articles" / f"{article['slug']}.html", page)

    for theme in themes:
        page = base_layout(
            title=f"{theme['title']} | Labor Supply Wiki",
            description=str(theme.get("deck", "")),
            root_prefix="..",
            body_class="theme-body",
            main_content=f"""
            <section class="article-header">
              <p class="eyebrow">Theme page</p>
              <h1>{html.escape(str(theme.get('title', '')))}</h1>
              <p class="lead">{html.escape(str(theme.get('deck', '')))}</p>
            </section>
            <section class="article-layout single-column">
              <article class="prose">
                {theme['html']}
              </article>
            </section>
            <section class="section linked-section">
              <div class="section-head">
                <h2>Linked articles</h2>
                <p>These are the pages currently carrying this theme.</p>
              </div>
              <div class="card-grid">
                {theme_article_links(theme, articles_by_slug)}
              </div>
            </section>
            """,
        )
        write_page(OUTPUT_DIR / "themes" / f"{theme['slug']}.html", page)

    for page_entry in pages:
        page = base_layout(
            title=f"{page_entry['title']} | Labor Supply Wiki",
            description=str(page_entry.get("deck", "")),
            root_prefix=".",
            body_class="page-body",
            main_content=f"""
            <section class="article-header">
              <p class="eyebrow">Workflow</p>
              <h1>{html.escape(str(page_entry.get('title', '')))}</h1>
              <p class="lead">{html.escape(str(page_entry.get('deck', '')))}</p>
            </section>
            <section class="article-layout single-column">
              <article class="prose">
                {page_entry['html']}
              </article>
            </section>
            """,
        )
        write_page(OUTPUT_DIR / f"{page_entry['slug']}.html", page)


if __name__ == "__main__":
    build()
