"""Refresh the self-hosted font files from the official Google Fonts repository."""
from pathlib import Path
import subprocess

out = Path(__file__).resolve().parents[1] / 'assets' / 'fonts'
out.mkdir(exist_ok=True)
for family, source, name in [
    ('geist', 'Geist', 'Geist'),
    ('geistmono', 'GeistMono', 'GeistMono'),
    ('spacegrotesk', 'SpaceGrotesk', 'SpaceGrotesk'),
]:
    base = f'https://raw.githubusercontent.com/google/fonts/main/ofl/{family}'
    for remote, local in [(f'{source}%5Bwght%5D.ttf', f'{name}-Variable.ttf'), ('OFL.txt', f'{name}-OFL.txt')]:
        subprocess.run(['curl', '-L', '--fail', '--silent', '--show-error', '--max-time', '30', f'{base}/{remote}', '-o', str(out / local)], check=True)
print('Self-hosted 3 font families with licenses.')
