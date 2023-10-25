from os import rename
import subprocess

rename('backend_entk.py', '../maestrowf/backend_entk.py')
rename('maestro_entk.patch', '../maestrowf/maestro_entk.patch')

subprocess.Popen('git apply maestro_entk.patch', cwd='../maestrowf')
