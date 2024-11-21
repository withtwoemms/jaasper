import subprocess
from pathlib import Path

from scripts.enums import SubProjects


PROJECTROOT = Path(__file__).parent.parent.absolute()
DEPENDENCYROOT = PROJECTROOT / 'dependencies'


def dependencies(subproject: SubProjects):
    export_command = [
        'python', '-m',
        'poetry', 'export',
        f'--with={subproject.name}',
        '--without-hashes',
        '--format=requirements.txt',
    ]
    depsfile = f'requirements.{subproject.name}.txt'
    subprocess.run(
        args=export_command,
        stdout=(DEPENDENCYROOT / depsfile).open(mode='w')
    )
