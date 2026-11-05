"""Download the public paper PDFs for figure previews, outside the deployed site."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
import subprocess

root = Path(__file__).resolve().parents[1]
out = Path('/tmp/portfolio-papers')
out.mkdir(exist_ok=True)
papers = json.loads((root / 'publications.json').read_text())
def fetch(p):
    dest = out / (p['id'] + '.pdf')
    subprocess.run(['curl', '-L', '--fail', '--silent', '--show-error', '--max-time', '90', 'https://arxiv.org/pdf/' + p['id'], '-o', str(dest)], check=True)
    return f'{p["id"]}: {dest.stat().st_size} bytes'
with ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(fetch, papers):
        print(result, flush=True)
