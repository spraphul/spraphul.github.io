# Praphul Singh

Research portfolio: https://spraphul.github.io/

Static HTML, CSS, and JavaScript, hosted with GitHub Pages. The blog is available separately at https://spraphul.github.io/blog/.

## Updating the site

- Edit `home.template.html` for biography, news, background, and honors.
- Edit `publications.json` for publication details.
- Run `python3 scripts/build.py` to regenerate `index.html`.
- Preview with `python3 -m http.server 8765 --bind 127.0.0.1`.

## Assets

Fonts are self-hosted under `assets/fonts/` with their SIL Open Font Licenses. Publication figure source metadata is recorded in `figure_sources.json`. The figure export scripts require PyMuPDF; the page builder uses the Python standard library.

The site supports topic filters, figure enlargement, and light and dark themes.

## Analytics

The production site uses Google Analytics 4 for traffic and interaction reports. Advertising features are disabled. The analytics script does not run on local previews and respects browser privacy signals and the opt-out control on `privacy.html`.
