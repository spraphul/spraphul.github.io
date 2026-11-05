"""Render unmodified figure regions from the author's public PDFs (PyMuPDF)."""
from pathlib import Path
import hashlib
import json
import fitz

root = Path(__file__).resolve().parents[1]
out = root / 'assets' / 'figures'
out.mkdir(exist_ok=True)
# Page numbers are 1-based. Bounds in PDF points, selected after visual inspection.
regions = {
 '2610.14643': (2, 1, [70, 87, 542, 296], 'Factorized speech privacy architecture'),
 '2609.09458': (2, 1, [91, 69, 507, 278], 'Query-conditioned procedural conformance pipeline'),
 '2608.20768': (2, 1, [106, 69, 496, 242], 'Paired model checkpoint and weight-delta audit'),
 '2510.17614': (4, 1, [69, 68, 526, 228], 'Uncertainty and reward-trend guided training curriculum'),
 '2510.14169': (3, 1, [53, 79, 287, 229], 'Training record construction for clinical order retrieval'),
 '2510.02338': (3, 1, [105, 75, 508, 203], 'Claim extraction and reinforcement learning pipeline'),
 '2505.18380': (2, 1, [91, 70, 496, 257], 'RedactOR multimodal de-identification architecture'),
 '2107.00727': (5, 5, [48, 161, 289, 288], 'Triple Distribution Matching architecture for domain adaptation'),
}
manifest = []
for pid, (number, fig, bounds, alt) in regions.items():
    path = Path('/tmp/portfolio-papers') / (pid + '.pdf')
    doc = fitz.open(path)
    pix = doc[number-1].get_pixmap(matrix=fitz.Matrix(4,4), clip=fitz.Rect(bounds), alpha=False)
    pix.save(out / (pid + '.png'))
    manifest.append(dict(id=pid,source='https://arxiv.org/pdf/'+pid,page=number,figure=fig,bounds_pt=bounds,alt=alt,pdf_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),width=pix.width,height=pix.height))
(root / 'figure_sources.json').write_text(json.dumps(manifest, indent=2)+'\n')
papers = json.loads((root / 'publications.json').read_text())
for p in papers:
    figure = next(f for f in manifest if f['id'] == p['id'])
    p.update(figure=figure['figure'],figure_alt=figure['alt'],figure_width=figure['width'],figure_height=figure['height'])
    if p['id']=='2610.14643': p['venue']='ML4H 2026'
    if p['id']=='2608.20768':
        p['venue']='Findings of EMNLP 2026'
        p['publication_url']='https://aclanthology.org/2026.findings-emnlp.1200/'
    if p['id']=='2510.17614': p['authors']='Praphul Singh, Corey Barrett, Sumana Srivasta, Irfan Bulu, Amitabh Saikia, Sri Gadde, Krishnaram Kenthapadi'
(root / 'publications.json').write_text(json.dumps(papers, indent=2, ensure_ascii=False)+'\n')
print('Exported 8 original figures with PDF provenance.')
