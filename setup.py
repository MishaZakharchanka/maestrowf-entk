from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
	"""Post-installation for installation mode."""
	def run(self):
		install.run(self)
		# PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
		import maestrowf
		from subprocess import PIPE, Popen
		maestro_pth = maestrowf.__path__[0]

		# import os
		# maestro_pth = os.path.abspath(maestrowf.__file__)
		# print(f"This is maestros path with the new way to find it: {maestro_pth}")
		cmd = f"patch {maestro_pth}/maestro.py maestro_entk_plugin/maestro_entk.patch"
		p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
		p.communicate()


		import shutil
		shutil.copy('maestro_entk_plugin/backend_entk.py', maestro_pth)

setup(
	name='maestro_entk_plugin',
	version='0.1',
	description='A plugin for Maestro to allow scheduling using entk',
	packages=['maestro_entk_plugin'],
	include_package_data=True,
	install_requires=[
		'maestrowf',
		'radical.entk',
	],
	cmdclass={
		'install': PostInstallCommand,
	},
)
