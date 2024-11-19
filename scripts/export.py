import subprocess

from pathlib import Path


PROJECTROOT = Path(__file__).parent.parent.absolute()

def api_dependencies():
    export_command = [
        'python', '-m',
        'poetry', 'export',
        '--with=api',
        '--without-hashes',
        '--format=requirements.txt',
    ]
    depsfile = 'requirements.api.txt'
    subprocess.run(
        args=export_command,
        stdout=Path(PROJECTROOT / depsfile).open(mode='w')
    )
