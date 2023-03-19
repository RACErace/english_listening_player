import os
import subprocess

def cmd(command):
    p=subprocess.Popen(command,shell=True)
    p.wait()

path = os.path.abspath(".")
cmd(f'setx "Path" "{path};%path%"')
cmd(f'setx "Path" "{path};%path%" /m')