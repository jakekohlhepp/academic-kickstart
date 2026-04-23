# Labor Supply Wiki

This workspace builds a lightweight static wiki for peer-reviewed labor supply research.

## What is here

- `content/articles/`: one markdown file per article page
- `content/themes/`: cross-paper theme pages
- `content/pages/`: workflow pages, including your-notes guidance
- `library/pdfs/`: saved local PDF copies
- `notes/inbox/google-doc-notes.md`: staging file for your raw notes
- `site/`: generated site output

## Build the site

Run:

```bash
python build.py
```

Then open:

`site/index.html`

## Source policy

- Article pages are primarily for peer-reviewed research articles, but especially relevant frontier working papers can also be included when they are directly useful for active synthesis.
- If the publisher PDF is not openly available, the saved PDF can be an open author manuscript or working-paper version tied to that peer-reviewed article.
- When a stable open PDF is not yet available, an article page may temporarily link only to the source page.
- Theme pages may connect articles across decades, methods, and policy questions.

## Notes workflow

The simplest workflow is to keep writing in Google Docs, then either:

1. Paste the latest raw text into `notes/inbox/google-doc-notes.md`, or
2. Give me a public or published Google Doc link when you want an integration pass.

When you tell me to integrate, I can sort those notes into article pages, theme pages, or a separate synthesis page.
