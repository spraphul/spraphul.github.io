"""Build a portable static homepage. No third-party build dependencies."""
from pathlib import Path
from html import escape
from datetime import date
import json

root = Path(__file__).resolve().parents[1]
papers = json.loads((root / 'publications.json').read_text())
groups = {}
for p in sorted(papers, key=lambda p: p['date'], reverse=True):
    year = p['date'][:4]
    authors = escape(p['authors']).replace('Praphul Singh', '<strong>Praphul Singh</strong>')
    abstract = ''
    if p.get('abstract'):
        abstract = f'<details><summary>Read summary</summary><p>{escape(p["abstract"])}</p></details>'
    published = ' published' if p['venue'] != 'Preprint' else ''
    paper_url = p.get('publication_url', 'https://arxiv.org/abs/' + p['id'])
    item = f'''<article id="paper-{p['id'].replace('.', '-')}" class="paper" data-topics="{' '.join(p['topics'])}">
      <button class="figure-trigger" type="button" aria-label="Enlarge figure for {escape(p['short'])}" data-figure="assets/figures/{p['id']}.png" data-alt="{escape(p['figure_alt'])}" data-title="{escape(p['title'])}" data-paper="{paper_url}"><img src="assets/figures/{p['id']}.png" alt="{escape(p['figure_alt'])}" width="{p['figure_width']}" height="{p['figure_height']}" loading="lazy"><span>Figure {p['figure']} · Enlarge ↗</span></button>
      <div class="paper-content">
      <div class="paper-meta"><time datetime="{p['date']}">{date.fromisoformat(p['date']).strftime('%b').upper()}</time><span>{escape(p['label'])}</span><span class="paper-status{published}">{escape(p['venue'])}</span></div>
      <h4><a href="{paper_url}">{escape(p['title'])} <span aria-hidden="true">↗</span></a></h4>
      <p class="authors">{authors}</p><p class="paper-summary">{escape(p['summary'])}</p>
      <div class="paper-links"><a href="{paper_url}">Paper ↗</a><a href="https://arxiv.org/pdf/{p['id']}">PDF ↗</a>{abstract}</div></div>
    </article>'''
    groups.setdefault(year, []).append(item)
timeline = ''.join(f'<div class="year-group"><h3 class="year">{year}</h3><div class="year-papers">{"".join(items)}</div></div>' for year, items in groups.items())
template = (root / 'home.template.html').read_text()
highlights = []
for paper_id, question in [('2609.09458', 'Did the agent follow the procedure?'), ('2608.20768', 'What changes when a model specializes?'), ('2610.14643', 'Can speech stay useful while protecting privacy?')]:
    p = next(p for p in papers if p['id'] == paper_id)
    url = p.get('publication_url', 'https://arxiv.org/abs/' + p['id'])
    highlights.append(f'''<article class="highlight">
      <p class="highlight-topic">{escape(p['label'])}</p>
      <h3>{escape(question)}</h3>
      <button class="figure-trigger" type="button" aria-label="Enlarge highlight figure for {escape(p['short'])}" data-figure="assets/figures/{p['id']}.png" data-alt="{escape(p['figure_alt'])}" data-title="{escape(p['title'])}" data-paper="{url}"><img src="assets/figures/{p['id']}.png" alt="{escape(p['figure_alt'])}" width="{p['figure_width']}" height="{p['figure_height']}" loading="lazy"><span>Explore figure ↗</span></button>
      <p class="highlight-summary">{escape(p['summary'])}</p>
      <a class="highlight-link" href="#paper-{p['id'].replace('.', '-')}">{escape(p['short'])} ↓</a><p class="highlight-venue">{escape(p['venue'])}</p>
    </article>''')
(root / 'index.html').write_text(template.replace('<!-- PUBLICATIONS -->', timeline).replace('<!-- HIGHLIGHTS -->', ''.join(highlights)))
print(f'Built index.html with {len(papers)} publications across {len(groups)} years.')
