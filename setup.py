from ez_setup import use_setuptools
use_setuptools(version='0.6c11')

from setuptools import setup, find_packages

version = '0.1'
    
setup(name='pypgbackup',
      version=version,
      description="Utility for make total or only single database postgresql backups",
      long_description="""\
Utility for make total or only single database postgresql backups""",
      classifiers=[],
      keywords='postgresql backup',
      author='Simone Dalla',
      author_email='sdalla@comune.zolapredosa.bo.it',
      url='www.comune.zolapredosa.bo.it',
      license='GPL',
      packages = find_packages('src'),
      package_dir = {'':'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'nose',
      ],
      entry_points = {
            'console_scripts' : [
                'pypgbackup = pypgbackup.application:main'
            ],
      },
      # use nose to run tests
      test_suite = 'nose.collector'
      )
