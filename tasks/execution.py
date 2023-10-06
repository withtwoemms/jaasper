import subprocess


def run_command(command: str):
    cmd = command.split()
    return subprocess.run(cmd)
