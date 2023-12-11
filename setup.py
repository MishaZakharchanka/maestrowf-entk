from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
	"""Post-installation for installation mode."""
	def run(self):
		install.run(self)
		import maestrowf
		from subprocess import PIPE, Popen
		maestro_pth = maestrowf.__path__[0]

		# import os
		# maestro_pth = os.path.abspath(maestrowf.__file__)
		# print(f"This is maestros path with the new way to find it: {maestro_pth}")
		cmd = f"patch {maestro_pth}/maestro.py maestro-entk/maestro_entk.patch"
		p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
		p.communicate()

		import shutil
		shutil.copy('maestro-entk/backend_entk.py', maestro_pth)

setup(
	name='maestrowf-entk',
	version='0.1',
	description='A plugin for Maestro to allow scheduling using entk',
	author=[
		'Mikhail Zakharchanka'
		'Mikhail Titov'
	],
	author_email='zakharchanka1@llnl.gov',
	license='MIT',
	python_requires='>=3.6',
	classifiers=[
		'Intended Audience :: Developers',
		'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
	],
	packages=['maestro-entk'],
	include_package_data=True,
	install_requires=[
		'maestrowf',
		'radical.entk',
	],
	cmdclass={
		'install': PostInstallCommand,
	},
)
