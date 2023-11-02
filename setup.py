from setuptools import setup

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
)
